# Run the script with '--help' to see more information.

class bcolors:
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def arguments():
    from argparse import ArgumentParser, RawTextHelpFormatter
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

An example of the correct format of a file name is below:
Full file name: Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4
Extracted title tag: Why Learn Python?
    ''', formatter_class=RawTextHelpFormatter)
    args = parser.parse_args()

def check_path(directory_path):
    from os import getcwd
    from os.path import isdir, join
    while True:
        input_directory = str(input(directory_path)).strip()
        if input_directory.startswith('.\\'):
            input_directory = input_directory.replace('.\\', '', 1)
        global search_directory
        search_directory = join((getcwd()), input_directory)
        if isdir(search_directory):
            break
        else:
            print(f'{bcolors.YELLOW}Invalid Directory Path: Please enter a valid directory path.{bcolors.RESET}')
            continue

def check_titles(correct_tags_dictionary, merged_tags_dictionary):
    if int(len(correct_tags_dictionary.items())) >= 1:
        print(f'{len(correct_tags_dictionary.items())} file(s) successfully tagged.')
    if int(len(merged_tags_dictionary.items())) >= 1:
        print(f'{bcolors.YELLOW}Found {len(merged_tags_dictionary.items())} file(s) with incorrect title tag{bcolors.RESET}.')
        for file_path, file_title in merged_tags_dictionary.items():
            print(f'{bcolors.YELLOW}Incorrect: Tag for "{file_path}" not successfully set.{bcolors.RESET}')

def confirm_save(confirmation):
    while True:
        answer = (str(input(confirmation)).strip()).lower()
        if answer == '' or answer.startswith('y'):
            answer = 'yes'
        elif answer.startswith('n'):
            answer = 'no'
        try:
            return {'yes':True,'no':False}[answer]
        except KeyError:
            print(f'{bcolors.YELLOW}Invalid Input: Please enter yes or no.{bcolors.RESET}')

def fetch_titles(dictionary):
    from os.path import join
    for file, root in dictionary.items():
        if ' - ' not in file:
            print(f'{bcolors.RED}Error: Video File "{join(root, file)}" is not named correctly.{bcolors.RESET}')
            print(f'{bcolors.YELLOW}Run the script with "--help" to see an example of the correct format of a file name.{bcolors.RESET}')
        else:
            valid_file_path_titles[join(root, file)] = ((file.split(' - '))[-1])[0:-((len(((file.split('.'))[-1]).strip())+1))].strip()

def handling_tags(correct_tags_dictionary, merged_tags_dictionary):
    if int(len(correct_tags_dictionary.items())) >= 1:
        print(f'Found {len(correct_tags_dictionary.items())} file(s) with correct title tag.')
    if int(len(merged_tags_dictionary.items())) >= 1:
        print(f'Found {len(merged_tags_dictionary.items())} file(s) with incorrect title tag.')
        for file_path, file_title in merged_tags_dictionary.items():
            print(f'The title for "{file_path}" would be "{file_title}".')
        return True
    elif int(len(merged_tags_dictionary.items())) == 0:
        return False

def main():
    check_path('Which directory would you like to search (recursively)? ')
    if walk_the_path(search_directory):
        fetch_titles(path_walked)
        sort_tags(valid_file_path_titles)
        if handling_tags(correct_tags, merged_empty_incorrect_tags):
            if confirm_save('Would you like to update the file(s) as shown above (Y/n)? '):
                update_title_progress(merged_empty_incorrect_tags)
                correct_tags.clear()
                incorrect_tags.clear()
                empty_tags.clear()
                merged_empty_incorrect_tags.clear()
                sort_tags(valid_file_path_titles)
                check_titles(correct_tags, merged_empty_incorrect_tags)
    else:
        print(f'{bcolors.YELLOW}No files found when searching for files ending with ".{extension_limit}".{bcolors.RESET}')
    terminate()

def sort_tags(dictionary):
    from mutagen.mp4 import MP4
    for file_path, file_title in dictionary.items():
        video_file = MP4(file_path)
        if '©nam' in video_file.keys():
            if file_title in video_file.get(key='©nam'):
                correct_tags[file_path] = file_title
            elif file_title not in video_file.get(key='©nam'):
                incorrect_tags[file_path] = file_title
        else:
            empty_tags[file_path] = file_title
    merged_empty_incorrect_tags.update(empty_tags)
    merged_empty_incorrect_tags.update(incorrect_tags)

def terminate():
    from sys import exit
    print('Exiting script.')
    exit()

def update_title(dictionary):
    from mutagen.mp4 import MP4
    for file_path, file_title in dictionary.items():
        video_file = MP4(file_path)
        video_file['©nam'] = [file_title]
        video_file.save()

def update_title_progress(dictionary):
    from progress.bar import FillingSquaresBar
    count = int(len(dictionary.items()))
    bar = FillingSquaresBar('Processing', max=count, suffix='%(index)d/%(max)d - %(percent).1f%%')
    for i in range(count):
        update_title(dictionary)
        count -= 1
        bar.next()
    bar.finish()

def valid_extension(extension):
    valid_extension_list = ['mp4']
    while True:
        global extension_limit
        extension_limit = str(input(extension)).strip()
        if extension_limit in valid_extension_list:
            break
        else:
            print(f'{bcolors.YELLOW}Invalid Input: Please enter one of the following supported extensions {valid_extension_list}.{bcolors.RESET}')
            continue

def walk_the_path(valid_directory_path):
    from os import walk
    valid_extension('What file extension would you like to use to narrow the search? ')
    for root, subdirs, files in walk(valid_directory_path):
        for file in files:
            if file.endswith(extension_limit):
                path_walked[file] = root
    if len(path_walked) == 0:
        return False
    elif len(path_walked) >= 1:
        return True

if __name__ == '__main__':
    correct_tags = {}
    empty_tags = {}
    incorrect_tags = {}
    merged_empty_incorrect_tags = {}
    path_walked = {}
    valid_file_path_titles = {}
    arguments()
    main()
