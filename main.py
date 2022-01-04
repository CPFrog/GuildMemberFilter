import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import edgedriver_autoinstaller

guild_url = "https://loawa.com/guild/"
url = "https://loawa.com/char/"


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('로스트아크 길드 템 레벨 검사기 v1.2 by CP개구링')
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('길드명:'), 0, 0)
        grid.addWidget(QLabel('레벨 제한:'), 1, 0)
        grid.addWidget(QLabel('부캐 길드명:'), 2, 0)
        grid.addWidget(QLabel('최대 부캐 수:'), 3, 0)

        self.gname_text = QLineEdit()
        self.gname_text.returnPressed.connect(self.button_event)
        self.lvthres_text = QLineEdit()
        self.lvthres_text.returnPressed.connect(self.button_event)
        self.subg_text = QLineEdit()
        self.subg_text.returnPressed.connect(self.button_event)
        self.maxsub_text = QLineEdit()
        self.maxsub_text.returnPressed.connect(self.button_event)
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
        global subnames
        global threshold
        global maxsubs

        guild = self.gname_text.text()
        if guild != '':
            threshold_t = self.lvthres_text.text()
            if threshold_t == '':
                threshold = 1500
            else:
                threshold = int(threshold_t.strip())
            subname = self.subg_text.text()
            subnames = subname.split(',')
            maxsubs = self.maxsub_text.text().split(',')
            if len(subnames) > 1:
                if len(subnames) != len(maxsubs):
                    QMessageBox.critical(self, '오류', '부캐 길드가 2개 이상인 경우 각 길드의 허용 부캐 갯수도 각각 지정하셔야 합니다.')
                    return
            elif len(subnames) == 1:
                if maxsubs[0] == '':
                    maxsubs[0] = '1'

            enlist(guild)
            QMessageBox.information(self, '완료 알림', '모든 검색 작업이 완료 되었습니다.')

        else:
            QMessageBox.critical(self, '길드명 미입력', '본캐 길드명 입력은 필수 사항입니다.')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, e):
        QMessageBox.information(self, '프로그램 종료 알림', '프로그램이 종료됩니다.')


def enlist(guild_name):
    driver = browser_driver()
    driver.implicitly_wait(3)

    driver.get(guild_url + guild_name)
    guild_soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(guild_soup)
    member_list = guild_soup.find_all('table', {'class': 'tfs13'})
    driver.quit()

    # print(member_list)

    filter_list = []
    pass_list = []
    for i in member_list:
        cname = i.find('span', {'class': 'text-theme-0 tfs13'}).text.strip()
        clevel = float(i.find('span', {'class': 'text-grade5 tfs13'}).text)
        dif = clevel - threshold
        # print(cname, ': ', dif, end='\t')
        if dif < 0:
            filter_list.append(cname)
        else:
            pass_list.append(cname)
    global f
    f = open(f'{guild_name} 길드 정리 명단.txt', 'w')
    f.write(f'--[{guild_name}] 템 레벨 {threshold} 미만 길드원 명단--\n')
    cnt = 0
    for s in filter_list:
        f.write(f'{s}  ')
        cnt += 1
        if cnt == 5:
            f.write('\n')
            cnt = 0
    f.write('\n\n')
    f.flush()
    # print('정리 대상: ', filter_list)
    # print('레벨컷 만족: ', pass_list)

    sub_search(subnames, filter_list)
    f.write('\n')
    f.flush()
    sub_search(subnames, pass_list, has_filtered=False)

    f.close()


def sub_search(subnames, member_list, has_filtered=True):
    if (len(subnames) == 0) | (subnames[0] == ''):
        return

    driver = browser_driver()
    length = len(subnames)
    for idx in range(length):
        sub_name = subnames[idx].strip()
        max_sub = int(maxsubs[i].strip())
        if has_filtered:
            f.write(f'--[{sub_name}] 템렙 제한 미만 길드원 부캐 목록--\n')
            # print('렙제 걸린 멤버 부캐 목록')
        else:
            f.write(f'--[{sub_name}] 부캐 {max_sub}개 초과 가입 길드원 목록--\n')
            # print(f'부캐{max_sub}개 이상 가입 길드원 목록')

        f.flush()

        for i in member_list:
            driver.get(url + i)
            driver.find_element(By.XPATH,
                                '/ html / body / div[6] / div / div[2] / div / div / div[2] / div[2] / div / div[2] / div[1] / label[6]').click()
            # time.sleep(3)

            char_soup = BeautifulSoup(driver.page_source, 'html.parser')

            char_list = char_soup.find_all('table', {'class': 'tfs14'})

            target_list = []

            for j in char_list:
                gname = j.find('span', {'class': 'tfs14 text-grade2'}).text.strip()
                cname = j.find('span', {'class': 'text-theme-0 tfs14'}).text.strip()
                if gname == sub_name:
                    target_list.append(cname)

            if has_filtered:
                if len(target_list) > 0:
                    # print(i, ': ', target_list)

                    f.write(f'{i}: ')
                    for s in target_list:
                        f.write(f'{s}  ')
                    f.write('\n')
                    f.flush()
            else:
                if len(target_list) > max_sub:
                    # print(i, ': ', target_list)

                    f.write(f'{i}: ')
                    for s in target_list:
                        f.write(f'{s}  ')
                    f.write('\n')
                    f.flush()

    driver.quit()


def browser_driver():
    try:
        driver_ver = edgedriver_autoinstaller.get_edge_version().split('.')[0]  # 크롬 드라이버 버전 확인
        browser = "edge"
    except:
        driver_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        browser = "chrome"

    if browser == "edge":
        options = webdriver.EdgeOptions()  # 옵션 생성
        options.add_argument("--headless")  # 창 숨기는 옵션 추가
        try:
            driver = webdriver.Edge(f'./{driver_ver}/edgedriver', options=options)
        except:
            edgedriver_autoinstaller.install(True)
            driver = webdriver.Edge(f'./{driver_ver}/edgedriver', options=options)

    elif browser == "chrome":
        options = webdriver.ChromeOptions()  # 옵션 생성
        options.add_argument("--headless")  # 창 숨기는 옵션 추가
        try:
            driver = webdriver.Chrome(f'./{driver_ver}/chromedriver', options=options)
        except:
            chromedriver_autoinstaller.install(True)
            driver = webdriver.Chrome(f'./{driver_ver}/chromedriver', options=options)

    return driver


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
