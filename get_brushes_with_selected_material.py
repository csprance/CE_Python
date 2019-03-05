# finds any object and adds them to the map using the currently selected objects material
import os
from better_cry import Level
import general
from cry_utils.add_cgfs_to_map import add_cgfs
from chunkfile.chunk import DataReader
from chunkfile.mtl_name_chunk import MtlNameChunk
from find_dws_models import get_all_damn_cgfs
from chunkfile import load_chunk_file


def create_mtl_filepath(mtl_name, cgf_path):
    return os.path.join(os.path.dirname(os.path.abspath(cgf_path)), mtl_name + ".mtl")


def add_game_root_to_path(path):
    return os.path.join(general.get_game_folder(), path + ".mtl").lower()


def find_brushes_with_material(material):
    cgfs = get_all_damn_cgfs("D:\perforce\dev\GameSDK\Objects", "*.cgf")
    matching_cgfs = []
    for cgf in cgfs:
        loaded_chunkfile = load_chunk_file(cgf)
        for chunk, pos in loaded_chunkfile.iter_chunks():
            if type(chunk) is MtlNameChunk:
                reader = DataReader(chunk.data)
                header = chunk.read_header_802(reader)
                mtl_name = create_mtl_filepath(
                    header.find_field("name").value.split("\0")[0], cgf
                ).lower()
                if mtl_name == material:
                    matching_cgfs.append(cgf)
    return matching_cgfs


def main():
    level = Level()
    selected = level.selected
    if len(selected) == 0:
        general.message_box_ok("Please Select a mesh")
        return
    material = add_game_root_to_path(level.selected[0].material)
    brushes = find_brushes_with_material(material)
    print(add_cgfs(brushes))


if __name__ == "__main__":
    main()
