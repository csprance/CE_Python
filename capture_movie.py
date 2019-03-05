import sys
import general
import trackview


def main():
    mode = sys.argv[1]

    if mode == "start":
        print("starting")
        general.set_cvar("capture_frames", 1)
        # if we have a trackview selected play it
        try:
            trackview.play_sequence()
        except Exception:
            pass
    if mode == "stop":
        print("stopping")
        general.set_cvar("capture_frames", 0)
        # if we have a trackview playing stop it
        try:
            trackview.stop_sequence()
        except Exception:
            pass


if __name__ == "__main__":
    main()
