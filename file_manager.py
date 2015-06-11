__author__ = 'alex'
from os import listdir, remove
from os.path import isfile, getsize
import shutil, hashlib, config, database

#return a list of files/directories in a directory
def get_files(directory_path):
    file_list = []
    for(i, x) in enumerate(listdir(directory_path)):
        newFile = File(x, directory_path, sizeof(directory_path + x), 0)
        file_list.append(newFile)
    return file_list

#return the size of a file
def sizeof(directory_path):
     if(isfile(directory_path)):
         return getsize(directory_path)
     else:
         return "-"

#return the total size of a directory (excluduing subdirectories)
def get_total_size(directory_path):
    filetotal = 0
    for (i, x) in enumerate(get_files(directory_path)):
        filetotal += int(x.file_size) if x.file_size is not ("-") else 0
    return filetotal

#delete a file
def file_delete(file_path):
    if(isfile(file_path)):
        print("rm " + file_path)
        remove(file_path)

#remove an item from the database and file system
def delete_item(guid):
    absolute_path = config.storage_location + guid + '.tar.gz'
    print absolute_path
    database.delete_row(guid)
    file_delete(absolute_path)

#tar/gzip a folder and copy it to the archive directory
def archive_folder(origin_path, destination_path, archive_name):
    shutil.make_archive(archive_name, 'gztar', origin_path)
    shutil.move(archive_name + '.tar.gz', destination_path)

#object representation of a file
class File:
    def __init__(self, display_name, file_name, file_size, creation_date):
        self.display_name = display_name
        self.file_name = file_name
        self.file_size = file_size
        self.timestamp = creation_date