import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

options = webdriver.ChromeOptions()  # 옵션 생성
options.add_argument("headless")  # 창 숨기는 옵션 추가
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')

driver.implicitly_wait(10)

guild_url = "https://loawa.com/guild/"
url = "https://lostark.game.onstove.com/Profile/Character/"
guild = "밤잠"
name = "CP개구링"

print(os.getcwd())


def enlist(guild_name):
    driver.get(guild_url + guild_name)
    guild_soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(guild_soup)
    member_list = driver.find_elements(By.CLASS_NAME, 'text-theme-0 tfs13')
    driver.quit()

    print(member_list)
    mlist = []

    for char in member_list:
        mlist.append(char.text)

    print(mlist)


enlist(guild)
