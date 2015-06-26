# Go through and place all objects from a folder into a scene
# Chris Sprance
# Entrada interactive

# just for pyflakes linting
import general

# glob looks through files in a smart way
import glob

import os

# get folder name from user

def return_idx(path_list):
    for idx, path in enumerate(path_list):
        if "GameSDK" in path:
            return idx+1

            
def userInput():
    # call the function that opens our file dialog
    file_path = general.open_file_box()
    # split that return value up to a list
    x = file_path.split('/')
    # remove the last value (the file)
    x.pop()
    # join them back together and return that (just the folder)
    return '/'.join(x)


# filter out all cgf, chr and cga models
def grabObjects(folder, filetype='cgf'):
    # generate a list of files in the folder
    obj_list = glob.glob(folder + '\*.' + filetype)
    cleaned_obj_list = list()
    
    for y in obj_list:
        y = os.path.normpath(y).split('\\')
        cleaned_obj_list.append("\\".join(y[return_idx(y):]))
    return cleaned_obj_list

# go through and create all of our objects


def genObjects(obj_list):
    # spawn in each of our objects found as brushes
    created_objs = list()
    print obj_list
    for idx, x in enumerate(obj_list):
        created_objs.append(general.new_object('Brush', x, x, idx * 2, 0, 0))
    return created_objs
# execute the functions here


def main():
    # get the directory we want to pull from
    general.clear_selection()
    file_path = userInput()
    # compile our list of objects from a directory
    obj_list = grabObjects(file_path)
    # create our objects from our list and select them
    general.select_objects(genObjects(obj_list))

# run the program
if __name__ == '__main__':
    main()
