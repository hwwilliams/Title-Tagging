from argparse import ArgumentParser, RawTextHelpFormatter
from mutagen.mp4 import MP4
from os import getcwd, walk
from os.path import isdir, join
from progress.bar import Bar
from sys import exit

# Run the script with '--help' to see more information.

def arguments():
    parser = ArgumentParser(description='''
A script to embed title tags in video files.

Dependencies: Python 3, Mutagen, and Progress
Install Mutagen by running 'pip install mutagen'
Install Mutagen by running 'pip install progress'

This script relies on files being named in fairly specific and uniform fashion.
It will attempt to extract an episode name and embed that into the file's title tag.
A valid file would look similar to 'Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4'.

The most important part of this naming scheme is the last instance of '-' plus the
period before the file extension. Whatever is between the last instance of '-' and the period will
be the episode name, minus any leading or trailing white spaces.

An example is below:
Full file name: Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4
Extracted title tag: Why Learn Python?
    ''', formatter_class=RawTextHelpFormatter)
    # parser.add_argument('-d','--directory',
    #                     help='The path to search for all files that would be updated. This path is searched recursively.')
    # parser.add_argument('-e','--extension-limit',
    #                     help='Search the directory for files ending with this extension.')
    # parser.add_argument('-s','--save', action="store_true"
    #                     help='Force save results.')
    args = parser.parse_args()

def check_path(prompt):
    while True:
        input_directory = str(input(prompt)).strip()
        if input_directory.startswith('.\\'):
            input_directory = input_directory.replace('.\\', '', 1)
        global search_directory
        search_directory = join((getcwd()), input_directory)
        if isdir(search_directory):
            break
        else:
            print('Invalid Directory Path: Please enter a valid directory path.')
            continue

def confirm_save(prompt):
    while True:
        confirm = (str(input(prompt)).strip()).lower()
        if confirm == '' or confirm.startswith('y'):
            confirm = 'yes'
        elif confirm.startswith('n'):
            confirm = 'no'
        try:
            return {'yes':True,'no':False}[confirm]
        except KeyError:
            print('Invalid Input: Please enter yes or no.')

def fetch_titles(dictionary):
    for file, root in dictionary.items():
        file_path_titles[(join(root, file))] = ((file.split(' - '))[-1])[0:-((len(((file.split('.'))[-1]).strip())+1))].strip()

def list_files_titles(dictionary):
    for file_path, file_title in dictionary.items():
        print(f'The title for "{file_path}" would be "{file_title}".')

def main():
    check_path('Which directory would you like to search (recursively)? ')
    if walk_the_path(search_directory):
        fetch_titles(path_walked)
        list_files_titles(file_path_titles)
        if confirm_save('Would you like to update the file(s) as shown above (Y/n)? '):
            progress(file_path_titles)
    else:
        print(f'No files found when searching for files ending with ".{extension_limit}".')
    terminate()

def progress(dictionary):
    bar = Bar('Processing', max=20, suffix='%(index)d/%(max)d - %(percent).1f%% - %(eta)ds')
    for i in range(20):
        update_title(dictionary)
        bar.next()
    bar.finish()

def terminate():
    print('Exiting script.')
    exit()

def update_title(dictionary):
    for file_path, file_title in dictionary.items():
        video_file = MP4(file_path)
        video_file['©nam'] = [file_title]
        video_file.save()

def valid_extension(prompt):
    valid_extension_list = ['mp4']
    while True:
        global extension_limit
        extension_limit = str(input(prompt)).strip()
        if extension_limit in valid_extension_list:
            break
        else:
            print(f'Invalid Input: Please enter one of the following supported extensions {valid_extension_list}.')
            continue

def walk_the_path(directory):
    valid_extension('What file extension would you like to use to narrow the search? ')
    for root, subdirs, files in walk(directory):
        for file in files:
            if file.endswith(extension_limit):
                path_walked[file] = root
    if len(path_walked) == 0:
        return False
    elif len(path_walked) >= 1:
        return True

if __name__ == '__main__':
    file_path_titles = {}
    mapped_title = {}
    path_walked = {}
    arguments()
    main()
