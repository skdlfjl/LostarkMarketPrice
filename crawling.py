import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import options
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



# 상세 옵션 검색버튼 클릭
detail_option_x_path = '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]/button[2]'
driver.find_element_by_xpath(detail_option_x_path).click()  # 상세 옵션 검색 클릭

# 장신구 선택
category_x_path = '//*[@id="selCategoryDetail"]/div[1]'
driver.find_element_by_xpath(category_x_path).click()  # 카테고리 클릭
driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[2]/label[10]').click()
# //*[@id="selCategoryDetail"]/div[2]/label[10] : 전체
# //*[@id="selCategoryDetail"]/div[2]/label[11] : 목걸이
# //*[@id="selCategoryDetail"]/div[2]/label[12] : 반지
# //*[@id="selCategoryDetail"]/div[2]/label[13] : 팔찌

# 아이템 등급 선택
class_x_path = '//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[1]'
driver.find_element_by_xpath(class_x_path).click()  # 아이템 등급 클릭
driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[2]/label[7]').click()
# 전체 : 1 / 일반 : 2 / 고급 : 3 / 희귀 : 4 / 영웅 : 5 / 전설 : 6
# //*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[2]/label[7] : 유물
# //*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[2]/label[8] : 고대


# 각인 선택1
option1_x_path = '//*[@id="selEtc_0"]/div[1]' 
driver.find_element_by_xpath(option1_x_path).click()  # 기타 선택1 클릭
driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[4]').click()  # 각인 효과 클릭
option1Sub_x_path = '//*[@id="selEtcSub_0"]/div[1]' 
driver.find_element_by_xpath(option1Sub_x_path).click()  # 옵션 선택 클릭
driver.find_element_by_xpath('//*[@id="selEtcSub_{0}"]/div[2]/label[{1}]'.format(0, 2)).click()  # '각성' 각인 선택
# 각인 선택2
option2_x_path= '//*[@id="selEtc_1"]/div[1]'
driver.find_element_by_xpath(option2_x_path).click()  # 기타 선택2 클릭
driver.find_element_by_xpath('//*[@id="selEtc_1"]/div[2]/label[4]').click()  # 각인 효과 클릭
option2Sub_x_path = '//*[@id="selEtcSub_1"]/div[1]' 
driver.find_element_by_xpath(option2Sub_x_path).click()  # 옵션 선택 클릭
driver.find_element_by_xpath('//*[@id="selEtcSub_{0}"]/div[2]/label[{1}]'.format(1, 3)).click()  # '갈증' 각인 선택
# '//*[@id="selEtcSub_{0}"]/div[2]/label[{1}]'.format(0, 2) : 각성
# '//*[@id="selEtcSub_{0}"]/div[2]/label[{1}]'.format(1, 3) : 갈증
# dict_x_path.py dict 가져와서 format사용
# selEtcSub_0 = 선택1 / selEtcSub_1 = 선택2
# label[2] = 각성 / label[3] = 갈증

search_x_path = '//*[@id="modal-deal-option"]/div/div/div[2]/button[1]'
driver.find_element_by_xpath(search_x_path).click()   # 검색버튼 클릭



### 페이지 넘기기 ###

x_index = 3
while x_index < 13:
    time.sleep(1.2)   # element is not attached to the page document 에러 해결
    driver.find_element_by_xpath(f'//*[@id="auctionList"]/div[2]/a[{x_index}]').click()
    
    # 해당 페이지 크롤링 코드 추가해야됨

    x_index += 1






# 귀걸이

# 반지