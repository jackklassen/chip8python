import sys
from src import chip8
from src.gui import Gui


#def main():
 #   args = sys.argv[1:]  # Exclude the script name
  #  chip8_main = chip8.Chip8(args)

#testing
def main():
    gui_main = Gui()
    gui_main.load_rom("test_opcode.ch8")
    gui_main.run()

if __name__ == '__main__':
   main()

