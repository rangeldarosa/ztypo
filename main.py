from time import sleep
from PIL import ImageGrab
from pytesseract import pytesseract
import pyautogui as pag

DEFAULT_WORDS = ["Type the words to shoot!", "ENTER for EMP"]

def main():
    #Define path to tessaract.exe
    path_to_tesseract = r'C:\Users\rdrosa\AppData\Local\Tesseract-OCR\tesseract.exe'

    #Point tessaract_cmd to tessaract.exe
    pytesseract.tesseract_cmd = path_to_tesseract

    #Open image with PIL
    img = ImageGrab.grab(bbox=(920, 220, 1645, 1300))
    # img.save('idk.png', format='png')
    # img.show()

    text: str = pytesseract.image_to_string(img)
    for w in DEFAULT_WORDS:
        text.strip(w)

    for p in text.split():
        pag.write(p)


if __name__ == '__main__':
    while True:
        main()
        sleep(2)


