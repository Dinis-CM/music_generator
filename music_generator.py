import sys
from music_generator import simple_no_gui_test
from music_generator import simple_gui_test

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) > 1 and sys.argv[1] == "--test-generator":
        simple_no_gui_test()
    if len(sys.argv) > 1 and sys.argv[1] == "--test-gui":
        simple_gui_test()
    else:
        print("Usage: python run.py [--test-generator | --test-gui]")
        print("Run without arguments for full GUI mode.")
        sys.exit(1)