from datetime import *
import time
from pynput import keyboard

pause = False

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        #global pause
        pause = True
        return False

    if key == keyboard.Key.esc:
        #global pause
        pause = True


# Collect events until released
#with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    #listener.join()

def event ():
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.esc:
                return 1
            else:
                print('Received event {}'.format(event))
    return 0

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()

liste = keyboard.Events()



while (not pause):
    print(pause)
    #if (event()) : break
    time.sleep(1)
    print("Je fais des choses")

print("Fin de programme")
