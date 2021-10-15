import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
import re
import requests

### input data ###  >>> 예시입니당

item = 11                 # 장신구 (11 = 목걸이 (특성2개))
eff = [[49, 5], [3, 3]]   # [[각인1, 활성도], [각인2, 활성도]]
cha = [2, 3]              # [특성1, 특성2]
cha = 2                   # 특성

#---------------------------------------------------------
# 크롤링 한 데이터에서 text만 뽑아내는 함수 (+ 공백과 줄바꿈 없애줌) 
def crawling_text(in_list, out_list):
        for i in in_list:
            out_list.append(i.text.replace(" ","").replace("\n",""))

# {'각성' : 6, '원한' : 3, '공격속도감소' : 1, '치명' : 403, '특화' : 446} 형태로 바꿔주는 함수
def effect_dict(effect_all, item):
    for i in range(len(effect_all)):
        effect_all[i] = effect_all[i].replace('[','').replace('활성도','').split(']+')

    if item == 11:    # 목걸이
        effect_list = []
        for i in range(len(effect_all)):
            if i % 5 == 0:
                #print(effect_all[i:i+5])
                effect_list.append(effect_all[i:i+5])    
        dict_list = []
        for i in effect_list:
            dic = { i[0][0] : int(i[0][1]), i[1][0] : int(i[1][1]), i[2][0] : int(i[2][1]), i[3][0] : int(i[3][1]), i[4][0] : int(i[4][1])}
            dict_list.append(dic)

    elif item == 12 or 13:  # 귀걸이, 반지
        effect_list = []
        for i in range(len(effect_all)):
            if i % 4 == 0:
                effect_list.append(effect_all[i:i+4])  
        dict_list = []
        for i in effect_list:
            dic = { i[0][0] : int(i[0][1]), i[1][0] : int(i[1][1]), i[2][0] : int(i[2][1]), i[3][0] : int(i[3][1])}
            dict_list.append(dic)

    #print(dict_list)
    return dict_list

#---------------------------------------------------------//*[@id="selCategoryDetail"]/div[2]/label[11]

# 해당 함수 실행시 로그인하여 로스트아크 경매장 홈페이지에 들어가집니다 (최초 1번만 실행)
def enter():
    #chrome_options = Options()
    #chrome_options.add_argument('--headlss')  # headless는 직접 크롬창에서 셀레니움이 어떻게 작동되는지 굳이 창을 열지 않고 싶을 때 이용.
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(r'C:\Users\user_\chromedriver_win32\chromedriver.exe')

    driver.implicitly_wait(3)
    login_url = 'https://member.onstove.com/auth/login?redirect_url=https%3A%2F%2Flostark.game.onstove.com%2FMain'
    driver.get(login_url)
    login_x_path = '//*[@id="idLogin"]/div[3]/button'
    driver.find_element_by_name('user_id').send_keys('okc951108')
    driver.find_element_by_name('user_pwd').send_keys('fhtmxmdkzm1234')
    driver.find_element_by_xpath(login_x_path).send_keys(Keys.ENTER)

    time.sleep(1)
    auction_url = "https://lostark.game.onstove.com/Auction"
    driver.get(auction_url)

    return driver


# 상세 옵션 검색버튼 클릭 후 장신구 선택 (목걸이? 반지? 팔찌?)
def item_select(driver, item, grade, cha):
    detail_option_x_path = '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]/button[2]'
    #driver.find_element_by_xpath(detail_option_x_path).click()  # 상세 옵션 검색 클릭
    driver.find_element_by_xpath(detail_option_x_path).send_keys(Keys.ENTER)
    
    # 장신구 선택
    category_x_path = '//*[@id="selCategoryDetail"]/div[1]'
    driver.find_element_by_xpath(category_x_path).send_keys(Keys.ENTER)  # 카테고리 클릭
    driver.find_element_by_xpath('//*[@id="selCategoryDetail"]/div[2]/label[{}]'.format(item)).click()
    # //*[@id="selCategoryDetail"]/div[2]/label[11] : 목걸이
    # //*[@id="selCategoryDetail"]/div[2]/label[12] : 귀걸이
    # //*[@id="selCategoryDetail"]/div[2]/label[13] : 반지

    # 아이템 등급 선택
    class_x_path = '//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[1]'
    driver.find_element_by_xpath(class_x_path).send_keys(Keys.ENTER)  # 아이템 등급 클릭
    driver.find_element_by_xpath('//*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[2]/label[{}]'.format(grade)).click()
    # //*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[2]/label[1] : 전체
    # //*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[2]/label[7] : 유물
    # //*[@id="modal-deal-option"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/div/div[2]/label[8] : 고대

    # '각인 효과' 옵션 미리 클릭
    option1_x_path = '//*[@id="selEtc_0"]/div[1]' 
    driver.find_element_by_xpath(option1_x_path).send_keys(Keys.ENTER)  # 기타 선택1 클릭
    driver.find_element_by_xpath('//*[@id="selEtc_0"]/div[2]/label[3]').click()  # 각인 효과 클릭
    option2_x_path= '//*[@id="selEtc_1"]/div[1]'
    driver.find_element_by_xpath(option2_x_path).send_keys(Keys.ENTER)  # 기타 선택2 클릭
    driver.find_element_by_xpath('//*[@id="selEtc_1"]/div[2]/label[3]').click()  # 각인 효과 클릭

    if item == 11:    ## 목걸이
        # 특성 선택1
        option3_x_path= '//*[@id="selEtc_2"]/div[1]'
        driver.find_element_by_xpath(option3_x_path).send_keys(Keys.ENTER)  # 기타 선택3 클릭
        driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[2]/label[2]').click()  # 전투 특성 클릭
        option3Sub_x_path = '//*[@id="selEtcSub_2"]/div[1]' 
        driver.find_element_by_xpath(option3Sub_x_path).send_keys(Keys.ENTER)  # 옵션 선택 클릭
        driver.find_element_by_xpath('//*[@id="selEtcSub_2"]/div[2]/label[{}]'.format(cha[0])).click()  # 2 (치명) 특성 선택
        # 특성 선택2
        option4_x_path= '//*[@id="selEtc_3"]/div[1]'
        driver.find_element_by_xpath(option4_x_path).send_keys(Keys.ENTER)  # 기타 선택4 클릭
        driver.find_element_by_xpath('//*[@id="selEtc_3"]/div[2]/label[2]').click()  # 전투 특성 클릭
        option4Sub_x_path = '//*[@id="selEtcSub_3"]/div[1]' 
        driver.find_element_by_xpath(option4Sub_x_path).send_keys(Keys.ENTER)  # 옵션 선택 클릭
        driver.find_element_by_xpath('//*[@id="selEtcSub_3"]/div[2]/label[{}]'.format(cha[1])).click()  # 3 (특화) 특성 선택
        # label[2] = 치명 / label[3] = 특화

    elif item ==  12 or 13:    ## 귀걸이, 반지
        # 특성 선택
        option3_x_path= '//*[@id="selEtc_2"]/div[1]'
        driver.find_element_by_xpath(option3_x_path).send_keys(Keys.ENTER)  # 기타 선택3 클릭
        driver.find_element_by_xpath('//*[@id="selEtc_2"]/div[2]/label[2]').click()  # 전투 특성 클릭
        option3Sub_x_path = '//*[@id="selEtcSub_2"]/div[1]' 
        driver.find_element_by_xpath(option3Sub_x_path).send_keys(Keys.ENTER)  # 옵션 선택 클릭
        driver.find_element_by_xpath('//*[@id="selEtcSub_2"]/div[2]/label[{}]'.format(cha)).click()  # 특성 선택

    search_x_path = '//*[@id="modal-deal-option"]/div/div/div[2]/button[1]'
    driver.find_element_by_xpath(search_x_path).send_keys(Keys.ENTER)   # 검색버튼 클릭


# 목걸이의 상세 옵션을 선택하여 검색 뒤, 크롤링 + 전처리 해줍니다 (input = 크롬드라이버, [각인, 활성도]*2, 특성*2)
def main(driver, eff, item):
    # 상세 옵션 검색버튼 클릭
    detail_option_x_path = '//*[@id="lostark-wrapper"]/div/main/div/div[3]/div[2]/form/fieldset/div/div[5]/button[2]'
    driver.find_element_by_xpath(detail_option_x_path).send_keys(Keys.ENTER)

    # 각인 선택1 + 활성값 입력
    option1Sub_x_path = '//*[@id="selEtcSub_0"]/div[1]' 
    driver.find_element_by_xpath(option1Sub_x_path).send_keys(Keys.ENTER)  # 옵션 선택 클릭
    driver.find_element_by_xpath('//*[@id="selEtcSub_0"]/div[2]/label[{}]'.format(eff[0][0])).click()  # 4 (강령술) 각인 선택
    driver.find_element_by_id('txtEtcMin_0').send_keys(str(eff[0][1]))  # 위 각인의 활성값이 6인것만 출력
    driver.find_element_by_id('txtEtcMax_0').send_keys(str(eff[0][1]))

    # 각인 선택2 + 활성값 입력
    option2Sub_x_path = '//*[@id="selEtcSub_1"]/div[1]' 
    driver.find_element_by_xpath(option2Sub_x_path).send_keys(Keys.ENTER)  # 옵션 선택 클릭
    driver.find_element_by_xpath('//*[@id="selEtcSub_1"]/div[2]/label[{}]'.format(eff[1][0])).click()  # 53 (원한) 각인 선택
    driver.find_element_by_id('txtEtcMin_1').send_keys(str(eff[1][1]))  # 위 각인의 활성값이 3인것만 출력
    driver.find_element_by_id('txtEtcMax_1').send_keys(str(eff[1][1]))

    # '//*[@id="selEtcSub_{0}"]/div[2]/label[{1}]'.format(0, 2) : 각성
    # '//*[@id="selEtcSub_{0}"]/div[2]/label[{1}]'.format(1, 3) : 갈증
    # dict_x_path.py dict 가져와서 format사용
    # selEtcSub_0 = 선택1 / selEtcSub_1 = 선택2
    # label[2] = 각성 / label[3] = 갈증

    search_x_path = '//*[@id="modal-deal-option"]/div/div/div[2]/button[1]'
    driver.find_element_by_xpath(search_x_path).send_keys(Keys.ENTER)   # 검색버튼 클릭


    ### 크롤링 해오기 ###
    time.sleep(1)
    html = driver.page_source # 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기
    name = soup.select('span.name')
    effect = soup.select('div.effect > ul > li')
    price = soup.select('div.price-buy')

    name_list = []
    effect_all = []  
    price_list = []        
    crawling_text(name, name_list)
    crawling_text(effect, effect_all)           # ['[각성]활성도+6', '[원한]활성도+3', '[공격속도감소]활성도+1', ... ]  >> 전처리 필요함!!
    effect_list = effect_dict(effect_all, item)  # {'각성' : 6, '원한' : 3, '공격속도감소' : 1, '치명' : 403, '특화' : 446} >> 전처리 완료
    crawling_text(price, price_list)

    item_list = []
    for i in range(len(name_list)):
        item_list.append([name_list[i], effect_list[i], price_list[i]])
    
    return item_list

    ### 페이지 넘기기 ###
    '''
    x_index = 3
    while x_index < 13:
        time.sleep(1.2)   # element is not attached to the page document 에러 해결
        driver.find_element_by_xpath(f'//*[@id="auctionList"]/div[2]/a[{x_index}]').send_keys(Keys.ENTER)
        
        # 해당 페이지 크롤링 코드 추가해야됨

        x_index += 1'''
