import tkinter as tk
from pyboy import PyBoy, WindowEvent

class PokemonEmulatorGUI:
    def __init__(self, master):
        self.master = master
        self.pressAction = [
            WindowEvent.PRESS_BUTTON_A,     # 0
            WindowEvent.PRESS_BUTTON_B,     # 1
            WindowEvent.PRESS_BUTTON_SELECT,# 2
            WindowEvent.PRESS_BUTTON_START, # 3
            WindowEvent.PRESS_ARROW_UP,     # 4
            WindowEvent.PRESS_ARROW_DOWN,   # 5
            WindowEvent.PRESS_ARROW_RIGHT,  # 6
            WindowEvent.PRESS_ARROW_LEFT,   # 7
            WindowEvent.PRESS_BUTTON_A,     # 8
            WindowEvent.PRESS_BUTTON_B,     # 9
        ]
        self.releaseAction = [
            WindowEvent.RELEASE_BUTTON_A,     # 0
            WindowEvent.RELEASE_BUTTON_B,     # 1
            WindowEvent.RELEASE_BUTTON_SELECT,# 2
            WindowEvent.RELEASE_BUTTON_START, # 3
            WindowEvent.RELEASE_ARROW_UP,     # 4
            WindowEvent.RELEASE_ARROW_DOWN,   # 5
            WindowEvent.RELEASE_ARROW_RIGHT,  # 6
            WindowEvent.RELEASE_ARROW_LEFT,   # 7
            WindowEvent.RELEASE_BUTTON_A,     # 8
            WindowEvent.RELEASE_BUTTON_B,     # 9
        ]
        self.run_emulator()
        self.pack()
        self.pyboy = None


    def run_emulator(self):
        self.pyboy = PyBoy("./PokemonRed.gb")
        self.pyboy.set_emulation_speed(5.0)
        self.emulation_loop()

    def emulation_loop(self):
        with open("./pi.txt", "r") as file:
            content = file.read()
        counter = 0
        while True:
            currentDigit = int(content[counter])
            counter += 1

            self.pyboy.send_input(self.pressAction[currentDigit])

            for i in range (24):
                if i == 8:
                    self.pyboy.send_input(self.releaseAction[currentDigit])
                self.pyboy.tick()
                
                
    """ def quit_emulator(self):
        self.pyboy.stop()
        self.destroy() """


root = tk.Tk()
gui = PokemonEmulatorGUI(root)
root.mainloop()
