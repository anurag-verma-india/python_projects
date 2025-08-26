# import pyautogui
# import time
# import keyboard

# # print("A")
# # print("A")
# # pyautogui.write("super")
# # print("A")

# # for key in pyautogui.KEYBOARD_KEYS:
# #     print(key)
# # print(pyautogui.KEYBOARD_KEYS)
# # ------------------
# # time.sleep(3)

# while True:
#     pyautogui.write("a;lskdjfa;lsdkfj;alsdkjf", interval=0.1)
#     # time.sleep(0.5)
#     pyautogui.hotkey("ctrl", "a")
#     pyautogui.press("backspace")

import pyautogui
import time

# Move mouse to top-left corner to trigger failsafe
pyautogui.FAILSAFE = True
print("Script started. Move mouse to top-left corner to stop.")
time.sleep(3)
try:
    while True:
        pyautogui.write("a;lskdjfa;lsdkfj;alsdkjf", interval=0.1)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")

except pyautogui.FailSafeException:
    print("Failsafe triggered. Script stopped.")
