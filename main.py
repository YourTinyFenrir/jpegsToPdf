import os
import time
from sys import argv
from PIL import Image, ImageChops, ImageEnhance
import pygetwindow as gw
import pyautogui as ag
import numpy as np
import cv2

if __name__ == '__main__':

    # Размеры области задаются для А3 на мониторе 1920х1080
    argX = 1370
    argY = 970

    # Поменять размеры области таким образом, чтобы захватывался весь экран, кроме рамок окна

    try:
        # Выводим список всех открытых окон
        windows = gw.getAllWindows()
        for w in windows:
            print(w.title)
        print("--------------------")

        # Выбираем 4ое в списке (первый - Пуск, второе - пустое, третье - консоль,
        # как последнее активированное (окно, которое необходимо скринить, должно быть
        # последним активным перед открытием командной строки
        win = gw.getWindowsWithTitle(windows[3].title)[0]
        print(win.title)
        print("--------------------")

        # Раскрываем на весь экран и переключаем фокус
        win.maximize()
        win.activate()

        # Определяем центр окна и объявляем счетчик страниц
        ctr = win.center
        pageCount = 0

        result = 12
        while result is not None:
            print("Page " + str(pageCount))
            time.sleep(0.5)  # Чтобы страница успела перелистнуться

            # Делаем и сохраняем скриншот заданной области
            # Скриншот с размерами argX, argY и центром посередине экрана
            img = ag.screenshot(region=(ctr.x - argX / 2, ctr.y - argY / 2, argX, argY))
            frame = np.array(img)
            screenshot = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
            cv2.imwrite(str(pageCount) + ".png", frame)

            # Сравниваем изображения (если они идентичны, то завершаем цикл)
            if pageCount > 0:
                img1 = Image.open(str(pageCount - 1) + ".png")
                img2 = Image.open(str(pageCount) + ".png")
                result = ImageChops.difference(img1, img2).getbbox()
                print("Pixel's diff: " + str(result))

            # Переходим к следующему изображению
            ag.keyDown('Down')
            pageCount = pageCount + 1

        print("--------------------")

        # Формируем список изображений
        image_list = []
        for i in range(0, pageCount - 1):
            image = Image.open(str(i) + ".png")
            # im = image.convert('RGB')

            # Увеличиваем яркость, тем самым избавляемся от надписи серым цветом по центру изображения
            im = ImageEnhance.Brightness(image)
            im.enhance(1.3).show()

            image_list.append(im)

        # Сохраняем изображения в ПДФ файл
        img = image_list[0]
        image_list.remove(img)

        fileName = win.title.replace('/', '')

        img.save(fileName + '.pdf', save_all=True, append_images=image_list)

        # Удаляем изображения
        for i in range(0, pageCount):
            os.remove(str(i) + ".png")

    except IndexError:
        print("no such window")