import pyautogui

class MouseController:
    def __init__(self):
        pass

    def move_mouse(self, x, y):
        try:
            pyautogui.moveTo(x, y)
        except pyautogui.FailSafeException:
            print("Fail-safe triggered. Moving to a corner of the screen.")
            # Handle the fail-safe here

    def click(self):
        pyautogui.click()

    def rightClick(self):
        pyautogui.rightClick()