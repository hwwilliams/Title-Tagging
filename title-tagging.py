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
            print('Invalid Directory Path: Please enter a valid directory path.')
            continue

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
            print('Invalid Input: Please enter yes or no.')

def fetch_titles(dictionary):
    from os.path import join
    for file, root in dictionary.items():
        file_path_titles[(join(root, file))] = ((file.split(' - '))[-1])[0:-((len(((file.split('.'))[-1]).strip())+1))].strip()

def list_files_titles(dictionary):
    for file_path, file_title in dictionary.items():
        print(f'The title for "{file_path}" would be "{file_title}".')

def main():
    file_path_titles = {}
    path_walked = {}
    check_path('Which directory would you like to search (recursively)? ')
    if walk_the_path(search_directory):
        fetch_titles(path_walked)
        list_files_titles(file_path_titles)
        if confirm_save('Would you like to update the file(s) as shown above (Y/n)? '):
            update_title_progress(file_path_titles)
    else:
        print(f'No files found when searching for files ending with ".{extension_limit}".')
    terminate()

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
            print(f'Invalid Input: Please enter one of the following supported extensions {valid_extension_list}.')
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
    main()
