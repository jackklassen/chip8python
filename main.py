import sys
from src import chip8




def main():
    args = sys.argv[1:]  # Exclude the script name
    chip8_main = chip8.Chip8(args)



#testing
#def main():
 #   chip8_main = chip8.Chip8("2-ibm-logo.ch8")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()

