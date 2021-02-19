import requests
from bs4 import BeautifulSoup
import datetime
import sys
import time
import pygame
import threading

WIDTH = 512
HEIGHT = 512
WHITE = (255, 255, 255)
BLACK = (0 ,0, 0)

link_list = ["https://finance.yahoo.com/quote/UAVS?p=UAVS&.tsrc=fin-srch", "https://finance.yahoo.com/quote/ATNF?p=ATNF&.tsrc=fin-srch"]
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


def write_status():
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    status = nowDatetime + '\n'
    print(nowDatetime)
    for i in range(len(my_list)):
        status += my_list[i].title + '\n'
        status += my_list[i].main + ' '+ my_list[i].main_add + "\n"
        status += my_list[i].sub + ' ' + my_list[i].sub_add + "\n"
    return status

# 연습



def runPad():
    global pad, clk
    font = pygame.font.SysFont(None, 30)  # 폰트 설정
    exit = False
    tmp = 1
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quit!")
                pygame.quit()
                sys.exit()

        pad.fill(WHITE)
        # my_list = []
        threads = list()
        my_list = list()
        for i in range(len(link_list)):
            thread = threading.Thread(target=business, args=(link_list[i], my_list))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        print("Finished")

        y = 0
        for i in range(len(my_list)):
            y += 50
            text1 = font.render(my_list[i].title, True, BLACK)  # 텍스트가 표시된 Surface 를 만듬
            pad.blit(text1, (50, y))
            y += 50
            text2 = font.render(my_list[i].main + ' ' + my_list[i].main_add, True, BLACK)  # 텍스트가 표시된 Surface 를 만듬
            pad.blit(text2, (50, y))
            y += 50
            text3 = font.render(my_list[i].sub + ' ' + my_list[i].sub_add, True, BLACK)  # 텍스트가 표시된 Surface 를 만듬
            pad.blit(text3, (50, y))
        tmp_text = font.render(str(tmp), True, BLACK)  # 텍스트가 표시된 Surface 를 만듬
        tmp += 1
        pad.blit(tmp_text, (WIDTH-50,HEIGHT-50))


        pygame.display.update()
        time.sleep(3)


def initPad():
    global pad, clk
    pygame.init()
    pad = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Real-time STOCKS")
    clk = pygame.time.Clock()
    runPad()
initPad()



























