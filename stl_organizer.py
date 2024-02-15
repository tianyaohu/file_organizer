# Copyright (c) 2024 Frank Hu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import argparse
import re

def _iterate_files(target_dir, extension):
    """Iterates over files in a directory with a specific extension.

    Args:
        target_dir (str): The path to the directory containing files to iterate over.
        extension (str): The file extension to match.

    Yields:
        str: The path to the next file with the specified extension.
        
    Raises:
        FileNotFoundError: If the target directory does not exist.
    """

    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"Target directory '{target_dir}' does not exist.")

    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(extension):
            yield file_path

#get file name lambda
get_file_name = lambda file_path: file_path[file_path.rfind("\\")+1:]

def _move_file_to_folder(file_path, dest_dir_path, is_copy = True):
    """
    Copies/Moves a file to a destination directory (will not copy, if file already exists)
    Args:
        file_path (str): The name of the file to copy.
        file_dir_path (str): The path to the directory containing the file.
        dest_dir_path (str): The path to the destination directory.
    
    """
    file_name = get_file_name(file_path)
    #check if the file already exists in the destination directory
    if os.path.exists(os.path.join(dest_dir_path, file_name)):
        #if already exists, skip
        #visualize in terminal
        print(f"File ___{file_name}___ already exists in {dest_dir_path}")
    else:
        #visualize in terminal
        print(f"Moving file ___{file_name}___ to {dest_dir_path}")
        if is_copy:
            shutil.copy(file_path, dest_dir_path)
        else:
            shutil.move(file_path, dest_dir_path)

def match_words(text, words):
    """Matches a list of words in a text using a regular expression.
    
    Args:
        text (str): The text to match.
        words (list): A list of words to match.
    
    Returns:
        str: The first match found, False otherwise.
    """

    pattern = re.compile('|'.join(re.escape(word) for word in words), re.IGNORECASE)
    #check if the pattern is found in the text
    result = pattern.search(text)
    if result:
        return result.group(0).lower()
    else:
        return False

def organize_files_via_category(origin_dir, extension = "", categories = ["core", "cover", "logo"]):
    """Organizes files in a target directory into folders based on predefined categories.

    Args:
        origin_dir (str): The path to the directory containing files to organize.
        categories (list): A list of categories. Each category should be a lowercase string.

    Raises:
        FileNotFoundError: If the target directory does not exist.
    """

    # Create the "_organized" directory
    organized_dir = os.path.join(origin_dir, origin_dir + "_organized")
    os.makedirs(organized_dir, exist_ok=True)  # Create the "_organized" directory

    #first create all the category folders
    for category in categories:
        os.makedirs(os.path.join(organized_dir, category), exist_ok=True)
        #visualize in terminal
        print(f"Try created category folder: {category}")
    
    #create other folder to store files that do not match any category
    OTHER_FOLDER = "other"
    os.makedirs(os.path.join(organized_dir, OTHER_FOLDER), exist_ok=True)
    print(f"Try create 'other' folder")

    #iterate through the files in the directory, match the category and copy the file
    for filename in _iterate_files(origin_dir, extension):
        result = match_words(filename, categories)
        #check if the file matches any category
        if result:
            _move_file_to_folder(filename, organized_dir + "\\" + result)
        #if the file does not match any category, copy it to the 'other' folder
        else:
            _move_file_to_folder(filename, organized_dir+ "\\" + OTHER_FOLDER)
    
    return organized_dir

def match_first_word_filename(filename):
  """
  Matches the first word in a filename using a regular expression.

  Args:
    filename: The filename to match.

  Returns:
    The first word of the filename if found, None otherwise.
  """

  pattern = r"^(?:[A-z][a-z]+)|(?:[A-z]+\b)"

  match = re.search(pattern, filename)
  if match:
    return match.group(0)
  else:
    return None

def organize_via_filename(origin_dir, extension):
    """Organizes files in a directory based on the first word in their filename.

    Args:
        origin_dir (str): The path to the directory to organize.
    """

    print('origin_dir:', origin_dir)

    for filename in _iterate_files(origin_dir, extension):
        first_word = match_first_word_filename(get_file_name(filename))  # Extract the first word

        # Create a destination folder based on the first word 
        dest_folder = os.path.join(origin_dir, first_word)
        os.makedirs(dest_folder, exist_ok=True)  

        # Move the file into the folder
        _move_file_to_folder(filename, dest_folder, is_copy = False)

if __name__ == "__main__":
    # Argument Parser Setup
    parser = argparse.ArgumentParser(description="Organize files into an '[target_folder_name]_organized' directory.")
    #add target directory argument
    parser.add_argument("-d", "--target_dir", help="The path to the directory containing STL files.")
    #add extension argument
    parser.add_argument("-e", "--extension", help="The file extension to organize. If not specified, all files will be organized.")
 
    #parse the arguments
    args = parser.parse_args()

    #get the target directory
    target_dir = args.target_dir if args.target_dir else "stl" #defaults to "stl" if not specified
    #get the extension
    extension = args.extension if args.extension else ".stl"

    #visualize in terminal
    print('target_dir:', target_dir)
    print('extension:', extension)

    #get the current working directory
    current_dir = os.getcwd() + "\\" + target_dir

    #bins to collect files into
    bins = ["core", "cover", "logo"]
    #iterate through the files in the directory
    organized_path = organize_files_via_category(current_dir, extension, categories=bins)

    #further organize the files in the 'other' folder
    organize_via_filename(organized_path + '\\other', extension)
