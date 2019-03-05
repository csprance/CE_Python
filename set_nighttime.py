from tools_shelf_actions import *

if __name__ == "__main__":
    general.hide_layer("day_layer")
    general.unhide_layer("night_layer")
    cycleList1 = ["e_TimeOfDay 20"]
    cycleConsolValue("mode_e_TimeOfDay", cycleList1)
    general.open_pane("Time Of Day")
