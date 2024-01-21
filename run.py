from pyboy import PyBoy, WindowEvent
import time
import requests

class PokemonEmulatorBackground:
    def __init__(self):
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

    def send_discord_message(self, webhook_url, message, image_path):
        with open(image_path, 'rb') as f:
            files = {'file': f}

            payload = {
                'content': message,
            }

            response = requests.post(webhook_url, data=payload, files=files)

            if response.status_code == 204:
                print("Message with image sent successfully!")
            else:
                print(f"Failed to send message with image. Status code: {response.status_code}, Response: {response.text}")

    def run_emulator(self):
        self.pyboy = PyBoy("./PokemonRed.gb")
        self.pyboy.set_emulation_speed(5.0)
        self.emulation_loop()

    def emulation_loop(self):
        webhook_url = 'Placeholder'
        message_content = 'Current screen:'
        image_path = './screenshot.jpg'
        with open("./pi.txt", "r") as file:
            content = file.read()
        counter = 0
        screen = 0
        lasttime = time.time()
        while True:
            if ((time.time() - lasttime) % 60 > 59):
                screen += 1
                lasttime = time.time()
            if screen == 15:
                screen = 0
                self.pyboy.screen_image().save("./screenshot.jpg")
                self.send_discord_message(webhook_url, message_content, image_path)
            currentDigit = int(content[counter])
            counter += 1

            self.pyboy.send_input(self.pressAction[currentDigit])

            for i in range(24):
                if i == 8:
                    self.pyboy.send_input(self.releaseAction[currentDigit])
                self.pyboy.tick()


if __name__ == "__main__":
    emulator = PokemonEmulatorBackground()
