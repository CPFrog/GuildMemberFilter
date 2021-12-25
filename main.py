import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

guild_url = "https://loawa.com/guild/"
url = "https://lostark.game.onstove.com/Profile/Character/"
pass_list = []
filter_list = []


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('로스트아크 길드원 템 레벨 검사기')
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('길드명:'), 0, 0)
        grid.addWidget(QLabel('레벨 제한:'), 1, 0)
        grid.addWidget(QLabel('부캐 길드명:'), 2, 0)
        grid.addWidget(QLabel('최대 부캐 수:'), 3, 0)

        self.gname_text = QLineEdit()
        self.lvthres_text = QLineEdit()
        self.subg_text = QLineEdit()
        self.maxsub_text = QLineEdit()
        grid.addWidget(self.gname_text, 0, 1)
        grid.addWidget(self.lvthres_text, 1, 1)
        grid.addWidget(self.subg_text, 2, 1)
        grid.addWidget(self.maxsub_text, 3, 1)

        search_btn = QPushButton('검색', self)
        search_btn.clicked.connect(self.button_event)
        grid.addWidget(search_btn, 4, 1)
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def button_event(self):
        global guild
        global subname
        global threshold
        global max_subchar

        guild = self.gname_text.text()
        threshold = int(self.lvthres_text.text())
        subname = self.subg_text.text()
        max_subchar = int(self.maxsub_text.text())

        enlist(guild)
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            self.button_event()
        elif e.key() == Qt.Key_Escape:
            self.close()


def enlist(guild_name):
    options = webdriver.ChromeOptions()  # 옵션 생성
    options.add_argument("headless")  # 창 숨기는 옵션 추가
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬 드라이버 버전 확인

    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')

    driver.implicitly_wait(10)

    driver.get(guild_url + guild_name)
    guild_soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(guild_soup)
    member_list = guild_soup.find_all('table', {'class': 'tfs13'})
    driver.quit()

    print(member_list)

    for i in member_list:
        cname = i.find('span', {'class': 'text-theme-0 tfs13'}).text.strip()
        clevel = float(i.find('span', {'class': 'text-grade5 tfs13'}).text)
        dif = clevel - threshold
        print(cname, ': ', dif, end='\t')
        if dif < 0:
            filter_list.append(cname)
        else:
            pass_list.append(cname)

    print('정리 대상: ', filter_list)
    print('레벨컷 만족: ', pass_list)


def sub_search(sub_name):
    if sub_name is None:
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

print('출력: ', guild, threshold, subname, max_subchar)
