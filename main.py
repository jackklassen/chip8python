# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#check out https://tobiasvl.github.io/blog/write-a-chip-8-emulator/
# and https://austinmorlan.com/posts/chip8_emulator/
import src
from src import chip8




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    chip8 = chip8.Chip8("2-ibm-logo.ch8")
    chip8.load_rom("2-ibm-logo.ch8")
    chip8.cycle()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
