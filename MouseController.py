import pyautogui
import time

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
        try:
            pyautogui.rightClick()
        except pyautogui.FailSafeException:
            print("Fail-safe triggered. Moving to a corner of the screen.")
            # Handle the fail-safe here
    
    def drag(self):
        try:
            # Start dragging by clicking down
            pyautogui.mouseDown()
            
            # Continuously track mouse movement
            while pyautogui.mouseInfo()[0] == 1:  # Check if left mouse button is still pressed
                x, y = pyautogui.position()  # Get current mouse position
                # Move the mouse to the new position
                pyautogui.moveTo(x, y)
                time.sleep(0.01)  # Small delay to control the drag speed

            # Stop dragging by releasing the mouse button
            pyautogui.mouseUp()
        except pyautogui.FailSafeException:
            print("Fail-safe triggered. Moving to a corner of the screen.")

    def scroll(self, clicks):
        try:
            pyautogui.scroll(clicks)
        except pyautogui.FailSafeException:
            print("Fail-safe triggered. Moving to a corner of the screen.")

    