import time

import pyautogui as pag
from time import sleep
import string
from threading import Thread


def send_to_game(w):
    while True:
        pag.write(w)
        pag.press("backspace")
        time.sleep(1)

def main():
    for f in string.ascii_lowercase:
        Thread(target=send_to_game, args=(f,)).start()

if __name__ == '__main__':
    for i in range(1, 4):
        print(f'Staring in: {i}')
        sleep(1)
    main()