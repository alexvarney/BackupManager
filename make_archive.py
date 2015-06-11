__author__ = 'alex'

import file_manager, database, time, config, uuid

def make_archive():
    timestamp = int(time.time())

    backup_target = config.directory_to_backup
    destination_location = config.storage_location

    display_name = 'Archive - ' + time.strftime("%x %X")
    archive_name = str(uuid.uuid4())

    file_manager.archive_folder(config.directory_to_backup, config.storage_location, archive_name)

    archive_size = file_manager.sizeof(config.storage_location + archive_name + '.tar.gz')

    if int(archive_size) > config.max_backup_size:
        print "ALERT: The archive size exceeds the maximum specified backup size."

    database.add_file(file_manager.File(display_name, archive_name, archive_size, timestamp))

def check_max_filesize():
    backup_directory_size = file_manager.get_total_size(config.storage_location)
    print backup_directory_size
    if(backup_directory_size > config.max_backup_size):
        file = database.get_oldest()
        print "Deleting entry: " + file.display_name
        file_manager.delete_item(file.file_name)
        check_max_filesize()

#backup routine
make_archive()
check_max_filesize()





