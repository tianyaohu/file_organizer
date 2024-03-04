# File Organizer 📂✨

## Overview 🌟
This script organizes files based on their categories within a specified target directory. It creates a new directory `[target_folder_name]_organized` in a more organized way.<br>
__THIS DOES NOT ALTERN the files to be sorted__
   
### Directory Details
 - First, based on filenames, send files into given manually defined bins (preset: ['core', 'cover', 'logo'), 
 ```bash
target_directory/
└── target_directory_organized/
    ├── core/
    ├── cover/
    ├── logo/
    └── other/
```
  -within `/other`, all files put into bins that share common first word. e.g `ElecEngineer.stl`, `ElecBox.stl` are put into the same dir `Elec`
**Final dir tree**
```bash

target_directory/
└── target_directory_organized/
    ├── core/
    ├── cover/
    ├── logo/
    └── other/
        ├── A/
        ├── B/
        ├── C/
        ...
```

## Simple Usage （organize all .stl)🚀
  drop this file **ONE directory above** the directory you want to sort. <br>
  run
```
cd YOUR_STL_DIRECTORY; python PATH_TO_SCRIPT/file_organizer.py
```

## Targeted Usage🎯
  drop this file **ONE directory above** the directory you want to sort. <br>
  run
```bash
python file_organizer.py -d [target_directory] -e [file_extension]
Arguments
```
### Arguments 📜
- `-d`, `--target_dir`: The path to the directory containing the files to be organized.
- `-e`, `--extension`: The file extension to organize. If not specified, all files will be organized.


### Contact 📫
Frank Hu tianyaoh@hotmail.com

