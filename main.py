import sys
from src import chip8
from src.gui import Gui


def main():
    args = sys.argv[1:]
    if not args:
        print("Please include a chip-8 rom")
        sys.exit(1)
    else:
        rom = args[0]  # Exclude the script name
        gui_main = Gui()
        gui_main.load_rom(rom)
        gui_main.run()

#testing
#def main():
 #   gui_main = Gui()
  #  gui_main.load_rom("test_opcode.ch8")
   # gui_main.run()

if __name__ == '__main__':
   main()

