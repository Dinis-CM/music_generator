import sys
from music_generator.simple_no_gui import simple_no_gui_test

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test_generator":
        simple_no_gui_test()
    if len(sys.argv) > 1 and sys.argv[1] == "--test_gui":
        simple_gui_test()
    if len(sys.argv)==1:
        full_gui()
    else:
        print("Usage: python run.py [--test_generator | --test_gui]")
        print("Run without arguments for full GUI mode.")
        sys.exit(1)