import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
import re
import requests

#chrome_options = Options()
#chrome_options.add_argument('--headlss')  # headless는 직접 크롬창에서 셀레니움이 어떻게 작동되는지 굳이 창을 열지 않고 싶을 때 이용.
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(r'C:\Users\user_\chromedriver_win32\chromedriver.exe')

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', str(data))

def get_crawl(URL):
    response = driver.get(URL)
    html = driver.page_source
    soup7 = BeautifulSoup(html, 'html.parser')
    ex_id_divs = soup7.find('div', {'id': 'view_content'})
    crawl_data = remove_html_tags(ex_id_divs)
    return crawl_data

driver.implicitly_wait(3)
login_url = 'https://member.onstove.com/auth/login?redirect_url=https%3A%2F%2Flostark.game.onstove.com%2FMain'
driver.get(login_url)
login_x_path = '//*[@id="idLogin"]/div[3]/button'
driver.find_element_by_name('user_id').send_keys('okc951108')
driver.find_element_by_name('user_pwd').send_keys('wlgml1489')
driver.find_element_by_xpath(login_x_path).click()
driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/section/article[2]/nav/a[2]').click()   # 비밀번호를 다음에 변경하기

auction_url = "https://lostark.game.onstove.com/Auction"
driver.get(auction_url)

# 여기까지 하면 로그인하여 로스트아크 경매장 홈페이지에 들어가집니다


# 목걸이
search_x_path = '//*[@id="btnSearch"]'
driver.find_element_by_id('txtItemName').send_keys('목걸이')
driver.find_element_by_css_selector("#selItemGrade").click()
driver.find_element_by_css_selector("#selItemGrade > div.lui-select__option > label:nth-child(8)").click()  
# label:nth-child(2) : 일반
# label:nth-child(3) : 고급
# label:nth-child(4) : 희귀
# label:nth-child(5) : 영웅
# label:nth-child(6) : 전설
# label:nth-child(7) : 유물
# label:nth-child(8) : 고대
# label:nth-child(9) : 에스더
driver.find_element_by_xpath(search_x_path).click()   # 검색버튼 클릭



### 페이지 넘기기 ###

while True:
    x_index = 3
    while x_index < 13:
        time.sleep(1.5)   # element is not attached to the page document 에러 해결
        driver.find_element_by_xpath(f'//*[@id="auctionList"]/div[2]/a[{x_index}]').click()
    
        # 해당 페이지 크롤링 코드 추가해야됨

        x_index += 1
    





# 귀걸이

# 반지