import subprocess
import os
import general


def main():
    cwd = os.getcwd()
    selection = general.get_names_of_selected_objects()
    file_path_list = list()

    for obj in selection:
        geom_file = general.get_entity_geometry_file(obj)
        file_path = cwd + "\\GameSDK\\" + geom_file
        file_path_list.append(file_path)

    for path in file_path_list:
        command = r'explorer /select, "%s"' % path
        print(command)
        subprocess.Popen(command)


if __name__ == "__main__":
    main()
