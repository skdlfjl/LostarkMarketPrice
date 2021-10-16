import dict_x_path as dic
import crawling as cr
import time

import all_combin as com
import crawling as cr
import dict_x_path as dic 


### input data ###  >>> 예시입니당
# 각인 6개 (고대등급 O) input data  (761초 - 약 13분)
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패', '원한']
ability_lv = [3, 3, 3, 3, 3, 2]
item_act = [10, 0, 0, 12, 12, 8]    # 333332
character = ['치명', '특화']    # [특성1, 특성2] 
character_act = [1500, 500]    # 원하는 특성값   
#-----------------------------------------------------------------------------------------

def tuple_index(tu, list_):
    eff_list = []
    for i in range(len(tu)):
        if tu[i] > 0:
            eff_list.append([ability[i], tu[i]])
    list_.append(eff_list)

def arousal_x_path(list_):
    list_[0][0] = dic.arousal_dict[list_[0][0]]
    list_[1][0] = dic.arousal_dict[list_[1][0]]

def x_path(in_list, out_list):
    for tu in in_list:
        tuple_index(tu, out_list)
    # [[['강령술', 6], ['원한', 3]], ... , [['갈증', 6], ['강화 무기', 3]]]
    for list_ in out_list:
        arousal_x_path(list_)
    # [[[4, 6], [53, 3]], ... ] >> xpath에 맞춰 바꿔줌 ('강령술' == 4)

def character_x_path(character):
    cha = [0, 0]
    cha[0] = dic.character_dict[character[0]]
    cha[1] = dic.character_dict[character[1]]
    return cha

# input >> 크롬드라이버, [각인xpath, 활성도]리스트(arousal_list), 장신구xpath(item), 특성xpath(cha)
# 현재까지 가능한 모든 장신구의 조합(possible_combin), 장신구의 유니크 토큰 리스트(result_item),
# 크롤링해서 저장할 리스트(item_data), 목걸이1 = 0 / 귀걸이1 = 1 / 귀걸이2 = 2 / 반지1 = 3 / 반지2 = 4 (k)
def crawling(driver, arousal_list, item, cha, possible_combin, result_item, item_data, k):
    combin_ = []
    for i in range(len(arousal_list)):
        time.sleep(1)
        item_list = cr.main(driver, arousal_list[i], item, cha)
        if item_list != []:
            item_data.append(item_list)
            for j in range(len(possible_combin)):
                if possible_combin[j][k] == result_item[i]:
                    combin_.append(possible_combin[j])
    return combin_

# 목걸이의 유니크 조합만 저장해둔 result_necklace
# 나올 수 있는 가능한 모든 조합을 저장해둔 possible_combin
result_necklace, possible_combin = com.main(ability, ability_lv, item_act)


######### 목걸이 #########
# 필요한 변수 선언
# item : 장신구의 x_path
# cha : 특성의 x_path
# grade : 장신구 등급의 x_path
# necklace_list : [[[각인1의 x_path, 활성값], [각인2의 x_path, 활성값]], ... ] 
item = 11   # 장신구 (11 = 목걸이 (특성2개))
necklace_list = []
x_path(result_necklace, necklace_list)
cha = character_x_path(character)
if len(ability) == 6:
    # 레벨의 합이 16이고, 보물+각인서 합이 35이상 39이하인 경우 53, 63 (333331)
    if sum(ability_lv) == 16 and 35 <= sum(item_act) <= 39:
        print('유물등급 + 고대등급 고려 >> 전체 : 1')
        grade = 1
    # 레벨의 합이 17이고, 보물+각인서 합이 40이상인 경우 63 (333332)
    elif sum(ability_lv) == 17 and 40 <= sum(item_act):
        print('고대등급만 고려 >> 고대 : 8')
        grade = 8
else:
    print('유물등급만 고려 >> 유물 : 7')
    grade = 7

driver = cr.enter()   # 경매장 접속 + return값으로 driver 받기
cr.item_select(driver, item, grade, cha)  # 상세옵션에서 목걸이 + 장신구 등급 + 특성 선택 


necklace_data = []    # 크롤링한 목걸이 데이터들을 해당 리스트에 저장
possible_combin = crawling(driver, necklace_list, item, cha, possible_combin, result_necklace, necklace_data, 0)

### 결과 찍어보기
necklace_data = sum(necklace_data, [])
print('크롤링한 목걸이 데이터 :')
for row in necklace_data:
    print(row)

# 귀걸이1의 유니크 조합 구하기
earring_1 = []
for row in possible_combin:
    earring_1.append(row[1])    

result_earring1 = list(set(earring_1))
print('\n')
print('result_earring1 :', result_earring1)   



######### 귀걸이1 #########
item = 12  # 장신구 (12 = 귀걸이 (특성1개))
earring1_list = []
x_path(result_earring1, earring1_list)
# cha와 grade는 목걸이에서 썼던거 그대로 사용

cr.item_select(driver, item, grade, cha)  # 상세옵션에서 귀걸이 + 장신구 등급 + 특성 선택 

earring1_data = []
possible_combin = crawling(driver, earring1_list, item, cha, possible_combin, result_earring1, earring1_data, 1)

### 결과 찍어보기
earring1_data = sum(earring1_data, [])
print('크롤링한 귀걸이1 데이터 :')
for row in earring1_data:
    print(row)

# 귀걸이2의 유니크 조합 구하기
earring_2 = []
for row in possible_combin:
    earring_2.append(row[2])    

result_earring2 = list(set(earring_2))
print('\n')
print('result_earring2 :', result_earring2) 