# Go through and place all objects from a folder into a scene
# Chris Sprance
# Entrada interactive

# just for pyflakes linting
import general

# glob looks through files in a smart way
import glob

# get folder name from user


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
    return obj_list

# go through and create all of our objects


def genObjects(obj_list):
    # spawn in each of our objects found as brushes
    for x in obj_list:
        general.new_object('Brush', x, x, 0, 0, 0)

# execute the functions here


def main():
    # get the directory we want to pull from
    file_path = userInput()
    # compile our list of objects from a directory
    obj_list = grabObjects(file_path)
    # create our objects from our list
    genObjects(obj_list)

# run the program
if __name__ == '__main__':
    main()
