from flask import Flask, make_response, request, render_template, redirect, send_from_directory
from functools import wraps
import file_manager, config, database
import sys


# Template Colors
success_green = "33db00"
warning_yellow = "e6e713"
error_red = "c30000"

app = Flask(__name__)

def check_auth(username, password):
    return username == config.app_username and password == config.app_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return make_response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="The server requires authentication, if unknown, please consult the configuration options in server.py"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def render_template_file_list(display_message = "", message_color = warning_yellow):
    files = database.get_all()
    return render_template('file_list.html',
                           files = files,
                           file_path = config.storage_location,
                           total_files = len(files),
                           total_size = file_manager.get_total_size(config.storage_location),
                           message = display_message,
                           message_color = message_color)


@app.route('/')
@requires_auth
def index():
    message = str(request.args.get('m'))
    color = str(request.args.get('c'))
    print message + " : " + color
    return render_template_file_list(message if not message == "None" else "BackupManager v0.1", color if not color == "None" else warning_yellow)

@app.route('/delete/', methods=['GET', 'POST'])
@requires_auth
def delete():
    file_guid = str(request.args.get('file')).strip()
    archive_name = database.get_file(file_guid).display_name
    file_manager.delete_item(file_guid)
    return redirect('/?m=' + "File deleted: " + archive_name + "&c=" + success_green)

@app.route('/download/', methods=['GET', 'POST'])
@requires_auth
def download():
    file_guid = str(request.args.get('file')).strip()
    filename = file_guid + '.tar.gz'
    return send_from_directory(config.storage_location, filename)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    app.run(host='0.0.0.0', port=config.app_port, debug=True)
