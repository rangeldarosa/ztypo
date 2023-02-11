import string
import threading
import time
from time import sleep

import cv2
from PIL import ImageGrab, Image
from pytesseract import pytesseract
import pyautogui as pag
from cv2 import cv2 as cv
from matplotlib import pyplot as plt
from numpy import array, where, ones, uint8
from string import ascii_lowercase
from threading import Thread
import enchant


DEBUG = False
TO_WRITE = []
EN_DICTIONARY = enchant.Dict('en_US')
ASCII_LETTERS_LIST = list(string.ascii_lowercase)
REVERSED_ASCII_LETTERS_LIST = list(string.ascii_lowercase)
REVERSED_ASCII_LETTERS_LIST.reverse()
RUNNING_THREADS = []


def send_to_game(w):
    pag.write(w)
    pag.press("backspace")
def writer():
    global TO_WRITE

    # while True:
    try:
        if TO_WRITE.__len__() > 0:
            for i in range(0, TO_WRITE.__len__()):
                # print(f"TO Write len: {TO_WRITE.__len__()}")
                # print(f"TO Write len: {TO_WRITE.__len__()}")
                # txt_write = TO_WRITE.pop()
                txt_write = TO_WRITE.pop()
                txt_write: str = txt_write.strip("\n")
                Thread(target=send_to_game, args=(txt_write,)).start()
                # suggested_words: list[str] = EN_DICTIONARY.suggest(txt_write)

                # print(f'Word: {txt_write}')
                # print(EN_DICTIONARY.suggst(txt_write)[0])
                # if suggested_words.__len__() > 0 and suggested_words[0].__len__() > txt_write.__len__():
                #     print(f"Swapping word: {txt_write} to {EN_DICTIONARY.suggest(txt_write)[0]}")
                #     txt_write = EN_DICTIONARY.suggest(txt_write)[0]
                # print("#"*10)


        # if TO_WRITE.__len__() > 10:

    except Exception:
        pass



def process_image(t,config):
    global TO_WRITE
    text: str = pytesseract.image_to_string(t, config=config)
    for t in text.split():
        #words = text.split()
        # print(text)
        # print(f'Found words: {text}')
        # if words.__len__() > 0 and not words[0] == "WAVE":
            # for p in text.split():
        try:
            if EN_DICTIONARY.check(t):
                TO_WRITE.append(t)
            else:
                suggestions = EN_DICTIONARY.suggest(t)
                if suggestions.__len__() > 0:
                    TO_WRITE.append(suggestions[0])
                else:
                    TO_WRITE.append(t)
        except ValueError:
            pass

def find_words_in_text_areas_focus_on_words(text_areas):
    for t in text_areas:
        # cv.imshow('idk',t)
        # cv.waitKey(0)
        tthread = Thread(target=process_image, args=(t, "--psm 8"))
        tthread.start()

    # if spawned_threads.__len__() > 0:
    #     for sp in spawned_threads:
    #         sp.join()


def grab_text_areas(img_grayscale):
    # cv.imwrite(f"output/grayscaleimg_{time.time().real}.png", img_grayscale)
    ret, threshed_image = cv.threshold(img_grayscale, 10, 255, cv.THRESH_BINARY)
    # cv.imwrite(f"output/threshedimg_{time.time().real}.png", threshed_image)
    contours, hierarchy = cv.findContours(threshed_image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # cv.imshow('idk', threshed_image)
    # cv.waitKey(1000)
    # cv.destroyAllWindows()

    text_areas = []
    for cnt in contours:
        if 31 <= cv.boundingRect(cnt)[3] < 40 < cv.boundingRect(cnt)[2]:
            x, y, w, h = cv.boundingRect(cnt)
            # thresh_held_textbox = cv.threshold(img_grayscale[y:y + h, x:x + w], 20, 255, cv.THRESH_BINARY_INV)[1]
            # cv.imwrite(f"output/threshedheldimg_{time.time().real}.png", img_grayscale[y:y + h, x:x + w])
            if DEBUG:
                print(cv.contourArea(cnt))
                # cv.imshow('idk', thresh_held_textbox)
                # cv.waitKey(0)
            text_areas.append(img_grayscale[y:y + h, x:x + w])

    print(f"Text areas len: {text_areas.__len__()}")

    return text_areas

def find_words_in_text_area_focus_on_letters(text_areas):
    for t in text_areas:
        tthread = Thread(target=process_image, args=(t,"--psm 10"))
        tthread.start()


def find_words_in_the_wild(img_grayscale):
    text: str = pytesseract.image_to_string(img_grayscale, config='--psm 11')
    words = text.split()
    print(f'Found words in the wild: {words}')
    if words.__len__() > 0 and not words[0] == "WAVE":
        for p in text.split():
            pag.write(p)
        pag.press("backspace")


def verify_if_in_danger(img_grayscale):
    ret, threshed_image = cv.threshold(img_grayscale, 20, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(threshed_image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv.contourArea(cnt) < 2500:
            print("#"*10)
            print("Danger mode on")
            print("#"*10)
            return True

    return False

def spray_and_pray():
    global TO_WRITE
    for i in range(0, ASCII_LETTERS_LIST.__len__()):
        # TO_WRITE.append(ASCII_LETTERS_LIST[i])
        TO_WRITE.append(REVERSED_ASCII_LETTERS_LIST[i])




def grab_image_and_grayscale_it():
    if DEBUG:
        print()
        # img = cv2.imread('img_6.png')
        # print("aqui")
        #
        img: Image = ImageGrab.grab(bbox=(920, 220, 1645, 1300))
        img_array = array(img)
        # cv.imshow('idk', img_array)
        # cv.waitKey(0)
    else:
        img: Image = ImageGrab.grab(bbox=(920, 220, 1645, 1300))
        img_array = array(img.convert('RGB'))

    return cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

def grab_danger_zone():
    img: Image = ImageGrab.grab(bbox=(920, 901, 1645, 1200))
    img_array = array(img.convert('RGB'))
    # cv.imshow('idk',img_array)
    # cv.waitKey(0)
    return cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)
    # ret, threshed_image = cv.threshold(img_array, 20, 255, cv.THRESH_BINARY)
    # cv.imshow('idk',threshed_image)
    # cv.waitKey(0)
    # return


def main():
    # global TO_WRITE
    # path_to_tesseract = r'C:\Users\rdrosa\AppData\Local\Tesseract-OCR\tesseract.exe'

    # pytesseract.tesseract_cmd = path_to_tesseract
    # twriter = Thread(target=writer)
    # twriter.start()
    # print("Twriter Started")

    # img: Image = ImageGrab.grab(bbox=(920, 220, 1645, 1300))
    # img_array = array(img.convert('RGB'))

    # cv.imwrite('idk3.png', grab_danger_zone())
    # img_array = img
    # img_array = img_array[:, :, ::-1].copy()  #

    ###
    # for i in range(1, 6):
    # img_array = cv.imread(f'img_{i}.png')

    while True:
        # Thread(target=process_image, args=(grab_image_and_grayscale_it(), None)).start()

        # Thread(target=spray_and_pray, args=()).start()

        # text_areas = grab_text_areas(grab_image_and_grayscale_it())
        # text_areas.reverse()
        # find_words_in_text_areas_focus_on_words(text_areas)
        # find_words_in_text_area_focus_on_letters(text_areas)

        # find_words = Thread(target=find_words_in_text_areas_focus_on_words, args=(text_areas,))
        # find_words.start()
        # find_letters = Thread(target=find_words_in_text_area_focus_on_letters, args=(text_areas,))
        # find_letters.start()

        # find_words.join()
        # find_letters.join()
    # find_words_in_the_wild(grab_image_and_grayscale_it())
    #     if verify_if_in_danger(grab_danger_zone()):
            # threading.Thread(target=enter_panic_mode)
            # threading.Thread(target=process_image, args=(grab_danger_zone(), None))
        # if TO_WRITE.__len__() < 1:
        spray_and_pray()
        # print(TO_WRITE)
        writer()
        sleep(0.03)
        # TO_WRITE = []



if __name__ == '__main__':
    for i in range(1, 4):
        print(f'Staring in: {i}')
        sleep(1)

    main()
        # sleep(2)
