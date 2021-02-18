import requests
from bs4 import BeautifulSoup
import datetime
import time

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
        print(x, y, z, w)


    else:
        print(response.status_code)






while True:
    my_list = []

    time.sleep(3)
    for i in range(len(link_list)):
        business(link_list[i], my_list)
    # print("\n\n\n\n\n\n\n")

    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    print(nowDatetime)
    # for i in range(len(my_list)):
    #     print(my_list[i].title)
    #     print(my_list[i].main, my_list[i].main_add)
    #     print(my_list[i].sub, my_list[i].sub_add)




























