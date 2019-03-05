from shutil import copyfile

basic_guide_l = "D:\perforce\dev\EI\icons\guide_basic_200.png"
basic_guide_xl = "D:\perforce\dev\EI\icons\guide_basic_2048.png"
advanced_guide_l = "D:\perforce\dev\EI\icons\guide_advanced_200.png"
advanced_guide_xl = "D:\perforce\dev\EI\icons\guide_advanced_2048.png"
specialized_guide_l = "D:\perforce\dev\EI\icons\guide_specialized_200.png"
specialized_guide_xl = "D:\perforce\dev\EI\icons\guide_specialized_2048.png"


basic = [
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_medical_bandages_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_roofs_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_bridges_1_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_ramps_1_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_stairs_1_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_traps_1_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_walkways_1_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_walls_1_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_weapons_melee_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_traps_1_48.png",
]
advanced = [
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_bridges_2_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_ramps_2_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_stairs_2_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_traps_2_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_walkways_2_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_walls_2_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_traps_2_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_storage_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_tire_stacks_48.png",
]
specialized = [
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_powered_parts_1_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_curves_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_gallows_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_gatehouse_48.png",
    "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/guide_structures_wood_watchtower_48.png",
]


def remove_48_replace_with(img_path, replace_with):
    value = (img_path[:-6] + replace_with + ".png").replace(
        "d:/perforce/dev/GameSDK/Libs/UI/Inventory/item_images/",
        "D:/perforce/dev/EI/icons/",
    )
    print(value)
    return value


for file_path in basic:
    copyfile(basic_guide_l, remove_48_replace_with(file_path, "200"))
    copyfile(basic_guide_xl, remove_48_replace_with(file_path, "2048"))


for file_path in advanced:
    copyfile(advanced_guide_l, remove_48_replace_with(file_path, "200"))
    copyfile(advanced_guide_xl, remove_48_replace_with(file_path, "2048"))

for file_path in specialized:
    copyfile(specialized_guide_l, remove_48_replace_with(file_path, "200"))
    copyfile(specialized_guide_xl, remove_48_replace_with(file_path, "2048"))
