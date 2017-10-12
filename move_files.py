from shutil import copyfile
import readline
import os
from sys import exit
import sys

def main():
    global md_file_number
    md_file_number = 0
    print('''
    Please enter the defining parts of the file names that you would like
    to copy to a new location. (E.g. '.xml', '.docx', 'April', etc)
    ''')
    fileType = input('Portion of file name: ')
    
    path1 = get_current(fileType)
    path2 = get_new()


    for root, dirs, files in os.walk(path1):
        for filename in files:  # this looks at each files name for each item
            # if any file name ends with .xml, but not .aux.xml then...
            if filename.endswith(fileType):
                md_file_number += 1
    double_check(md_file_number, path1, path2, fileType)
    # file_list1 = []  # Can add later for more functionality
    # file_list2 = []  # Can add later for more functionality
    for root, dirs, files in os.walk(path1):
        for filename in files:  # this looks at each files name for each item
            # if any file name ends with .xml, but not .aux.xml then...
            if filename.endswith(fileType):
                # print(
                #     "Found a file that fits your parameters! {0}".format(filename))
                metadata_file1 = os.path.join(root, filename)
                # file_list1.append(metadata_file1)  # Can add later for more functionality
                # print(metadata_file1)
                metadata_file2 = os.path.join(path2, filename)
                # file_list2.append(metadata_file2)  # Can add later for more functionality
                # print(metadata_file2)
                copyfile(metadata_file1, metadata_file2)
    print("""
    ------------------------------------------------------------------------
    We found {0} files that matched your description. 
    They were found here: {1}
    And copied to here: {2}
    ------------------------------------------------------------------------
    """.format(md_file_number, path1, path2))
    
    print("Would you like to use the program again?")
    again = input('Again? (Y/N)\n> ').lower()
    if 'y' in again:
        main()
    else:
        exit(0)


    #https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python

def get_current(fileType):
    print('''
    Where are the '{0}' files located that you want moved?
    '''.format(fileType))
    path1 = input('Current location: ')
    if not os.path.isdir(path1):
        print("That does not appear to be a valid path to a directory.")
        get_current(fileType)
    else:
        return(str(path1))


def get_new():
    print('''
    Where would you like the files moved to?
    NOTE: Any files in this new location with the same names as files 
          from the old location will be overwritten.
    ''')
    path2 = input('New location: ')
    if not os.path.isdir(path2):
        print("That does not appear to be a valid path to a directory.")
        get_new()
    else:
        return(str(path2))

def double_check(md_file_number, path1, path2, fileType):

    print('''
    Found {0} files that meet your requirements. 
    Continue copying files?
    Original location: {1}
    New Location: {2}
    '''.format(md_file_number, path1, path2))
    _continue_ = input("Continue? (Y/N) \n").lower()
    if 'y' == _continue_:
        return
    elif 'n' == _continue_:
        exit(0)
    else:
        print('Please type \'y\' or \'n\'')
        double_check(md_file_number, path1, path2, fileType)


if __name__ == '__main__':
    main()
