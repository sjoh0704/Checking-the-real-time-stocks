import requests
from bs4 import BeautifulSoup
import sys
import pygame
import threading
import os

X = 30
WIDTH = 400
height = 400
TEXT_SIZE = 25
WHITE = (246, 246, 246)
BLACK = (25, 25, 25)
SPACE = 30
BLUE = (0, 84, 255)
RED = (255, 0, 0)
DIR = 'C:/Stocks'
FILE = DIR+"/real-time-stock.txt"
link_list = list()
my_list = []

class Item:
    def __init__(self,title, main, sub, main_add, sub_add):
        self.title = title
        self.main = main
        self.sub = sub
        self.main_add = main_add
        self.sub_add =sub_add



def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


# createFolder('/Users/aaron/Desktop/test')


def write_file():
    createFolder(DIR)
    text = open(FILE, "w")

    for l in link_list:
        text.write(l + '\n')

    text.close()


def read_file():
    text = open(FILE, "r")
    stored = []
    while True:
        line = text.readline()
        if not line:
            break
        link_list.append(line.strip())
    text.close()


def check_file_exist():
    try:
        if os.path.exists(FILE):
            ans = input("저장된 항목들을 불러올까요?(y/n):")
            if ans == "y" or ans == "Y":
                read_file()
                return True
            else:
                print("파일을 불러오지 않습니다. ㅠㅠ")
        print()
        return False

    except OSError:
        print('Error: Creating directory. ' + DIR)


def business(url, list, next):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        # titles = soup.select('ul.list_basis div div div div div a[title]')
        title = soup.select_one('div div div div div div div div div div h1').get_text()

        price = soup.select('div div div div div div div div div div div div div div span[data-reactid]')

        x, y, z, w = 0, 0, 0, 0

        for p in price:
            if "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" in str(p):
                x = p.get_text()


            elif "Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)" in str(p):
                z = p.get_text()

            elif "C($primaryColor) Fz(24px) Fw(b)" in str(p):

                y = p.get_text()

            elif "Trsdu(0.3s) Mstart(4px) D(ib) Fz(24px)" in str(p):

                w = p.get_text()
        item = Item(title, x, y, z, w)
        list.append((next, item))

    else:
        print(response.status_code)


def runPad():
    tmp = 0
    start = 0
    global pad, clk

    txt = "waiting"
    exit = False

    line = "_" * 100

    font = pygame.font.SysFont(None, TEXT_SIZE)
    pygame.display.update()

    before = list()
    my_list = list()
    while not exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quit!")
                pygame.quit()
                sys.exit()

        pad.fill(BLACK)

        if threading.active_count() == 1:
            next = 0
            for i in range(len(link_list)):
                next += 1
                thread = threading.Thread(target=business, args=(link_list[i], my_list, next))
                thread.start()
            my_list.sort()

        if len(before) == 0:

            tmp_text = font.render(txt, True, WHITE)  # 텍스트가 표시된 Surface 를 만듬
            pad.blit(tmp_text, (WIDTH // 2 - 100, height // 2))
            txt += "."
            if txt == "waiting.......":
                txt = "waiting"
        y = 0
        if len(my_list) == len(link_list):
            before = list(my_list)
            for i in range(len(my_list)):
                elem = my_list.pop(0)[1]
                y += SPACE
                text1 = font.render(elem.title, True, WHITE)  # 텍스트가 표시된 Surface 를 만듬
                pad.blit(text1, (X, y))
                y += SPACE

                if (elem.main_add == 0 and elem.main == 0) or (elem.main_add == "" and elem.main == ""):
                    text2 = font.render("closed", True, WHITE)  # 텍스트가 표시된 Surface 를 만듬

                elif elem.main_add[0] == "+":
                    text2 = font.render(str(elem.main) + ' ' + str(elem.main_add), True, BLUE)  # 텍스트가 표시된 Surface 를 만듬
                else:
                    text2 = font.render(str(elem.main) + ' ' + str(elem.main_add), True, RED)
                pad.blit(text2, (X, y))
                y += SPACE

                if (elem.sub_add == 0 and elem.sub == 0) or (elem.sub_add == "" and elem.sub == ""):
                    text3 = font.render("closed", True, WHITE)  # 텍스트가 표시된 Surface 를 만듬
                elif elem.sub_add[0] == "+":
                    text3 = font.render(str(elem.sub) + ' ' + str(elem.sub_add), True,
                                        BLUE)  # 텍스트가 표시된 Surface 를 만듬
                else:
                    text3 = font.render(str(elem.sub) + ' ' + str(elem.sub_add), True, RED)
                pad.blit(text3, (X, y))
                y += 10
                text4 = font.render(line, True, WHITE)
                pad.blit(text4, (0, y))

        else:
            for i in range(len(before)):
                y += SPACE
                b = before[i][1]
                text1 = font.render(str(b.title), True, WHITE)  # 텍스트가 표시된 Surface 를 만듬
                pad.blit(text1, (X, y))
                y += SPACE
                if (b.main_add == 0 and b.main == 0) or (b.main_add == "" and b.main == ""):
                    text2 = font.render("closed", True, WHITE)  # 텍스트가 표시된 Surface 를 만듬

                elif b.main_add[0] == "+":
                    text2 = font.render(str(b.main) + ' ' + str(b.main_add), True, BLUE)  # 텍스트가 표시된 Surface 를 만듬
                else:
                    text2 = font.render(str(b.main) + ' ' + str(b.main_add), True, RED)
                pad.blit(text2, (X, y))
                y += SPACE
                if (b.sub_add == 0 and b.sub == 0) or (b.sub_add == "" and b.sub == ""):
                    text3 = font.render("closed", True,
                                        WHITE)  # 텍스트가 표시된 Surface 를 만듬
                elif b.sub_add[0] == "+":
                    text3 = font.render(str(b.sub) + ' ' + str(b.sub_add), True,
                                        BLUE)  # 텍스트가 표시된 Surface 를 만듬
                else:
                    text3 = font.render(str(b.sub) + ' ' + str(b.sub_add), True, RED)
                pad.blit(text3, (X, y))
                y += 10
                text4 = font.render(line, True, WHITE)
                pad.blit(text4, (0, y))


        string = ">"*4
        tmp_text = font.render(string, True, WHITE)  # 텍스트가 표시된 Surface 를 만듬
        start += 30
        pad.blit(tmp_text, (start,height-X))
        if start >= WIDTH:

            start = 0





        pygame.display.update()
        clk.tick(8)


def initPad():
    global height
    global pad, clk
    pygame.init()
    height = 130 * len(link_list)
    pad = pygame.display.set_mode((WIDTH, height))
    pygame.display.set_caption("Real-time STOCKS")
    clk = pygame.time.Clock()
    runPad()


def search():
    going = True
    while going:
        search = input("추가하고 싶은 항목 검색: ")
        link = "https://finance.yahoo.com/quote/" + search
        response = requests.get(link)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            # titles = soup.select('ul.list_basis div div div div div a[title]')
            try:
                print("...\n잠시만 기다려 주세요...\n...")
                title = soup.select_one('div div div div div div div div div div h1').get_text()
                print(title)
            except:
                print("잘못된 페이지 입니다.")
            else:
                print("추가합니다.")
                link_list.append(link)
            finally:
                ans = input("\n계속 추가하시겠습니까?(y/n): ")
                if ans == "y" or ans == "Y":
                    continue
                elif ans == "n" or ans == "N":
                    print("종료합니다.")
                    going = False
                else:
                    print("계속 추가합니다.")
                    continue

        else:
            print("ERROR: "+ str(response.status_code))
            print("검색을 재시도 합니다.")


get_file = check_file_exist()
if get_file:
    initPad()
else:
    search()
    write_file()
    initPad()




























