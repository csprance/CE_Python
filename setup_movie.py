import subprocess
import general
import better_file_dialog.editor_run as bfd


def main():
    output_format = general.edit_box("Output Format [jpg | tga]")
    general.set_cvar("capture_file_format", output_format)
    [folder] = bfd.get_file_path_list(False, general.get_game_folder(), True)
    general.set_cvar("capture_folder", folder)
    general.set_cvar("r_displayInfo", 0)
    # 1 second / amount of frames 1/30 = 0.03333 =  30fps
    fps = general.edit_box("Frames Per Second")
    general.set_cvar("t_fixedstep", 1.0 / int(fps))
    general.set_cvar("r_CustomResPreview", 1)
    general.set_cvar("r_CustomResMaxSize", 4096)
    width = general.edit_box("Width")
    height = general.edit_box("Height")
    general.set_cvar("r_CustomResWidth", int(width))
    general.set_cvar("r_CustomResHeight", int(height))
    try:
        command = r'explorer "%s"' % folder
        subprocess.Popen(command)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
