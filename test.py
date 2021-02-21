import requests
from bs4 import BeautifulSoup
import sys
import pygame
import threading

X = 30
WIDTH = 400
height = 400
TEXT_SIZE = 25
WHITE = (246, 246, 246)
BLACK = (25, 25, 25)
SPACE = 30
BLUE = (0, 84, 255)
RED = (255, 0, 0)

link_list = list()
my_list = []
class Item:
    def __init__(self,title, main, sub, main_add, sub_add):
        self.title = title
        self.main = main
        self.sub = sub
        self.main_add = main_add
        self.sub_add =sub_add


def business(url, list):
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
        list.append(item)


    else:
        print(response.status_code)


# 연습



def runPad():
    global pad, clk

    txt = "waiting"
    exit = False
    tmp = 1
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
            for i in range(len(link_list)):

                thread = threading.Thread(target=business, args=(link_list[i], my_list))
                thread.start()


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
                elem = my_list.pop(0)


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
                text1 = font.render(str(before[i].title), True, WHITE)  # 텍스트가 표시된 Surface 를 만듬
                pad.blit(text1, (X, y))
                y += SPACE

                if (before[i].main_add == 0 and before[i].main == 0) or (before[i].main_add == "" and before[i].main == ""):
                    text2 = font.render("closed", True, WHITE)  # 텍스트가 표시된 Surface 를 만듬

                elif before[i].main_add[0] == "+":
                    text2 = font.render(str(before[i].main) + ' ' + str(before[i].main_add), True, BLUE)  # 텍스트가 표시된 Surface 를 만듬
                else:
                    text2 = font.render(str(before[i].main) + ' ' + str(before[i].main_add), True, RED)

                pad.blit(text2, (X, y))
                y += SPACE
                if (before[i].sub_add == 0 and before[i].sub == 0) or (before[i].sub_add == "" and before[i].sub == ""):

                    text3 = font.render("closed", True,
                                        WHITE)  # 텍스트가 표시된 Surface 를 만듬

                elif before[i].sub_add[0] == "+":
                    text3 = font.render(str(before[i].sub) + ' ' + str(before[i].sub_add), True,
                                        BLUE)  # 텍스트가 표시된 Surface 를 만듬
                else:
                    text3 = font.render(str(before[i].sub) + ' ' + str(before[i].sub_add), True, RED)
                pad.blit(text3, (X, y))

                y += 10

                text4 = font.render(line, True, WHITE)
                pad.blit(text4, (0, y))


        tmp_text = font.render(str(tmp), True, WHITE)  # 텍스트가 표시된 Surface 를 만듬
        tmp += 1
        pad.blit(tmp_text, (WIDTH-2*X,height-X))
        pygame.display.update()
        clk.tick(5)



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
                print("링크를 추가합니다.")
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




search()

initPad()



























