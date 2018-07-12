import argparse
import mutagen.mp4
import progress.bar
import os
import sys


# Run the script with '--help' to see more information.


class bcolors:
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'


def arguments():
    parser = argparse.ArgumentParser(description='''
A script to embed title tags in video files.

Dependencies: Python 3, Mutagen, and Progress

Install Mutagen by running 'pip install mutagen'
Install Mutagen by running 'pip install progress'

This script relies on files being named in fairly specific and
uniform fashion. It will attempt to extract an episode name and
embed that into the file's title tag. A valid file would look similar
to 'Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4'.

The most important part of this naming scheme is the last instance
of '-' plus the period before the file extension. Whatever is between
the last instance of '-' and the period will be the episode name,
minus any leading or trailing white spaces.

An example of the correct format of a file name is below:
File name: Python 3 Tutorial for Beginners - S01E01 - Why Learn Python?.mp4
Extracted title tag: Why Learn Python?
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.parse_args()


def check_path(directory_path):
    while True:
        input_directory = str(input(directory_path)).strip()
        if input_directory.startswith('.\\'):
            input_directory = input_directory.replace('.\\', '', 1)
        search_directory = os.path.join((os.getcwd()), input_directory)
        if os.path.isdir(search_directory):
            break
        else:
            print(f'{bcolors.YELLOW}Invalid Directory Path: Please enter a valid directory path.{bcolors.RESET}')
            continue
    return search_directory


def check_titles(correct_tags_dictionary, merged_tags_dictionary):
    if len(correct_tags_dictionary) >= 1:
        print(f'{len(correct_tags_dictionary)} file(s) successfully tagged.')
    if len(merged_tags_dictionary) >= 1:
        print(f'{bcolors.YELLOW}Found {len(merged_tags_dictionary)} file(s) with incorrect title tag{bcolors.RESET}.')
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
            return {'yes': True, 'no': False}[answer]
        except KeyError:
            print(f'{bcolors.YELLOW}Invalid Input: Please enter yes or no.{bcolors.RESET}')


def fetch_titles(path_walked_dictionary):
    valid_titles = {}
    for file, root in path_walked_dictionary.items():
        if ' - ' not in file:
            print(f'{bcolors.RED}Error: Video File "{os.path.join(root, file)}" is not named correctly.{bcolors.RESET}')
            print(f'{bcolors.YELLOW}Run the script with "--help" to see an example of the correct format of a file name.{bcolors.RESET}')
        else:
            valid_titles[os.path.join(root, file)] = ((file.split(' - '))[-1])[0:-((len(((file.split('.'))[-1]).strip())+1))].strip()
    return valid_titles


def handling_tags(correct_tags_dictionary, merged_tags_dictionary):
    if len(correct_tags_dictionary) >= 1:
        print(f'Found {len(correct_tags_dictionary)} file(s) with correct title tag.')
    if len(merged_tags_dictionary) >= 1:
        print(f'Found {len(merged_tags_dictionary)} file(s) with incorrect title tag.')
        for file_path, file_title in merged_tags_dictionary.items():
            print(f'The title for "{file_path}" would be "{file_title}".')
        return True
    elif len(merged_tags_dictionary) == 0:
        return False


def main():
    arguments()
    search_directory = check_path('Which directory would you like to search (recursively)? ')
    path_walked = walk_the_path(search_directory)
    valid_titles = fetch_titles(path_walked)
    correct_tags, incorrect_tags, empty_tags, merged_tags = sort_tags(valid_titles)
    if handling_tags(correct_tags, merged_tags):
        if confirm_save('Would you like to update the file(s) as shown above (Y/n)? '):
            update_title_progress(merged_tags)
            correct_tags.clear()
            incorrect_tags.clear()
            empty_tags.clear()
            merged_tags.clear()
            correct_tags, incorrect_tags, empty_tags, merged_tags = sort_tags(valid_titles)
            check_titles(correct_tags, merged_tags)
    terminate()


def sort_tags(valid_titles_dictionary):
    correct = {}
    incorrect = {}
    empty = {}
    merged = {}
    for file_path, file_title in valid_titles_dictionary.items():
        video_file = mutagen.mp4.MP4(file_path)
        if '©nam' in video_file:
            if file_title in video_file.get('©nam'):
                correct[file_path] = file_title
            else:
                incorrect[file_path] = file_title
        else:
            empty[file_path] = file_title
    merged.update(empty)
    merged.update(incorrect)
    return correct, incorrect, empty, merged


def terminate():
    print('Exiting script.')
    sys.exit()


def update_title(tags_dictionary):
    for file_path, file_title in tags_dictionary.items():
        video_file = mutagen.mp4.MP4(file_path)
        video_file['©nam'] = [file_title]
        video_file.save()


def update_title_progress(tags_dictionary):
    count = len(tags_dictionary)
    bar = progress.bar.FillingSquaresBar('Processing', max=count, suffix='%(index)d/%(max)d - %(percent).1f%%')
    for tag in range(count):
        update_title(tags_dictionary)
        count -= 1
        bar.next()
    bar.finish()


def valid_extension(extension):
    valid_extension_list = ['mp4']
    while True:
        extension_limit = (str(input(extension)).strip()).lower()
        if extension_limit in valid_extension_list:
            break
        else:
            print(f'{bcolors.YELLOW}Invalid Input: Please enter one of the following supported extensions {valid_extension_list}.{bcolors.RESET}')
            continue
    return extension_limit


def walk_the_path(valid_directory_path):
    path_walked = {}
    extension_limit = valid_extension('What file extension would you like to use to narrow the search? ')
    for root, subdirs, files in os.walk(valid_directory_path):
        for file in files:
            if file.endswith(extension_limit):
                path_walked[file] = root
    if len(path_walked) == 0:
        print(f'{bcolors.YELLOW}No files found when searching for files ending with ".{extension_limit}".{bcolors.RESET}')
        terminate()
    elif len(path_walked) >= 1:
        return path_walked


if __name__ == '__main__':
    main()
