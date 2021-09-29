import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

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
driver.get('https://member.onstove.com/auth/login?redirect_url=https%3A%2F%2Flostark.game.onstove.com%2FMain')
login_x_path = '//*[@id="idLogin"]/div[3]/button'
driver.find_element_by_name('user_id').send_keys('okc951108')
driver.find_element_by_name('user_pwd').send_keys('wlgml1489')
driver.find_element_by_xpath(login_x_path).click()
driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/section/article[2]/nav/a[2]').click()   # 비밀번호를 다음에 변경하기

# 여기까지 하면 로그인하여 로스트아크 공식 홈페이지에 들어가집니다
# 추가적으로 필요한 기능? : 아이디를 직접 입력할 수 있는 기능


