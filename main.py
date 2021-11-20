import dict_x_path as dic
import crawling as cr
import time
import csv 
import numpy as np

import all_combin as com
import crawling as cr
import dict_x_path as dic 


### input data ###  >>> 예시입니당
# 각인 6개 (고대등급 O) input data
ability = ['기습의 대가', '잔재된 기운', '원한', '슈퍼 차지', '예리한 둔기', '아드레날린']
ability_lv = [3, 3, 3, 3, 3, 2]
#item_act = [12, 12, 10, 0, 0, 7] 
item_act = [12, 12, 9, 0, 0, 7]    
character = ['치명', '특화']    # [특성1, 특성2] 
character_act = [450, 1450]    # 원하는 특성값 
#-----------------------------------------------------------------------------------------
### input data ###  >>> 예시입니당
# 각인 5개 (고대등급 X) input data
'''ability = ['기습의 대가', '잔재된 기운', '원한', '슈퍼 차지', '예리한 둔기']
ability_lv = [3, 3, 3, 3, 3]
item_act = [7, 7, 12, 9, 0]    # 33333
#item_act = [7, 5, 12, 12, 0]   
character = ['치명', '특화']    # [특성1, 특성2] 
character_act = [1500, 500]    # 원하는 특성값 '''
#-----------------------------------------------------------------------------------------
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다


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

def effect_list(tu):
    eff_list = []
    for i in range(len(tu)):
        if tu[i] > 0:
            eff_list.append([ability[i], tu[i]])
    return eff_list

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

def item2_data(result_item1, crawling_item1, result_item2, item1_data, possible_combin, driver, item, cha, k):
    result = []
    item2_data = []
    combin = []
    for tu in result_item2:
        if tu in crawling_item1:  # 만약 tu가 이미 크롤링 되어있다면
            # 일단 해당 possible_combin에서 해당 튜플이 존재하는 모든 조합들만 combin에 저장해둔다
            for i in range(len(possible_combin)):
                if possible_combin[i][k] == tu:
                    combin.append(possible_combin[i])
            # 그리고 데이터는 따로 item2_data에 저장해둔다 (나중에 리턴할것임)
            a = effect_list(tu)  # [['원한', 6], ['안정된 상태', 3]]
            for item1 in item1_data:
                try:
                    if item1[1][a[0][0].replace(' ', '')] == a[0][1] and item1[1][a[1][0].replace(' ', '')] == a[1][1]:
                        item2_data.append(item1)
                except:
                    pass
        # crawling_item1에 들어있지 않지만 result_item1에 들어있는 조합은 크롤링 되지 않은 조합이기때문에 그냥 pass
        elif tu in result_item1:
            pass        
        # 둘 다 속하지 않는다면 새로운 조합이므로 result 리스트에 추가하여 새로 크롤링 할 수 있도록 한다
        else:
            result.append(tu)

    # 만약 result 리스트가 비어있지 않다면 새로운 크롤링이 필요하다는것! 
    if len(result) != 0: 
        item2_list = []
        x_path(result, item2_list)

        item2_data_ = []
        combin_ = crawling(driver, item2_list, item, cha, possible_combin, result_item2, item2_data_, k)
        item2_data += sum(item2_data_, [])
        combin += combin_  

    return item2_data, combin


def save_csv(name, item_data):
    with open('{}.csv'.format(name), 'w', newline='', encoding='utf-8') as f: 
        writer = csv.writer(f) 
        for row in item_data:
            writer.writerow(row) 

#-----------------------------------------------------------------------------------------
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
    # 사용자가 입력한 돌+각인서 활성도 값 합이 [ 필요 활성도 합 - (6+3)*5 ] 와 같을 경우
    # 63 고대 장신구로만 조합이 나오도록! (63 장신구로만 조합해야 가능하기때문)  
    if len(ability) == 6 and sum(item_act) == sum(ability_lv_act) - (6+3)*5:
        print('고대 장신구')
        grade = 8 # 고대 : 8
    else:
        print('유물 장신구 + 고대 장신구')
        grade = 1 # 전체 : 1
else:
    print('유물 장신구')
    grade = 7 # 유물 : 7

driver = cr.enter()   # 경매장 접속 + return값으로 driver 받기
cr.item_select(driver, item, grade, cha)  # 상세옵션에서 목걸이 + 장신구 등급 + 특성 선택 


necklace_data = []    # 크롤링한 목걸이 데이터들을 해당 리스트에 저장
possible_combin = crawling(driver, necklace_list, item, cha, possible_combin, result_necklace, necklace_data, 0)
necklace_data = sum(necklace_data, [])

#save_csv('necklace', necklace_data)   # 파일로 저장
print('목걸이 크롤링 후 possible_combin :', len(possible_combin))

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
# 목걸이1 = 0 / 귀걸이1 = 1 / 귀걸이2 = 2 / 반지1 = 3 / 반지2 = 4 (k)
earring1_data = sum(earring1_data, [])

#save_csv('earring1', earring1_data)   # 파일로 저장
print('귀걸이1 크롤링 후 possible_combin :', len(possible_combin))

# 크롤링된 귀걸이1의 유니크 조합 구하기
earring1 = []
for row in possible_combin:
    earring1.append(row[1]) 
crawling_earring1 = list(set(earring1))
print('crawling_earring1 :', crawling_earring1)

# 귀걸이2의 유니크 조합 구하기
earring_2 = []
for row in possible_combin:
    earring_2.append(row[2])    

result_earring2 = list(set(earring_2))
print('\n')
print('result_earring2 :', result_earring2) 



######### 귀걸이2 #########
earring2_data, possible_combin = item2_data(result_earring1, crawling_earring1, result_earring2, earring1_data,  possible_combin, driver, item, cha, 2)

#save_csv('earring2', earring2_data)   # 파일로 저장
print('귀걸이2 크롤링 후 possible_combin :', len(possible_combin))

# 반지1의 유니크 조합 구하기
ring_1 = []
for row in possible_combin:
    ring_1.append(row[3])    

result_ring1 = list(set(ring_1))
print('\n')
print('result_ring1 :', result_ring1) 



######### 반지1 #########
item = 13  # 장신구 (13 = 반지 (특성1개))
ring1_list = []
x_path(result_ring1, ring1_list)
# cha와 grade는 목걸이에서 썼던거 그대로 사용

cr.item_select(driver, item, grade, cha)  # 상세옵션에서 귀걸이 + 장신구 등급 + 특성 선택 

ring1_data = []
possible_combin = crawling(driver, ring1_list, item, cha, possible_combin, result_ring1, ring1_data, 3)
ring1_data = sum(ring1_data, [])

#save_csv('ring1', ring1_data)   # 파일로 저장
print('반지1 크롤링 후 possible_combin :', len(possible_combin))

# 크롤링된 반지1의 유니크 조합 구하기
ring1 = []
for row in possible_combin:
    ring1.append(row[3]) 
crawling_ring1 = list(set(ring1))
print('crawling_ring1 :', crawling_ring1)

# 반지2의 유니크 조합 구하기
ring_2 = []
for row in possible_combin:
    ring_2.append(row[4])    

result_ring2 = list(set(ring_2))
print('\n')
print('result_ring2 :', result_ring2) 



######### 반지2 #########
ring2_data, possible_combin = item2_data(result_ring1, crawling_ring1, result_ring2, ring1_data, possible_combin, driver, item, cha, 4)

#save_csv('ring2', ring2_data)   # 파일로 저장
print('반지2 크롤링 후 possible_combin :', len(possible_combin))




#### 결과내기!!! (최저가 장신구조합 뽑아내기) >> 조합 최적화 필요 / 최저가만 보여주지 말고 몇개 더 보여주기
####--------------------------------------------------------------------------------------------------------------
def item_list_(A, item_data):
    item_list_ = []
    for item in item_data:
        try:
            if item[1][A[0][0].replace(' ', '')] == A[0][1] and item[1][A[1][0].replace(' ', '')] == A[1][1]:
                item_list_.append(item)
        except:
            pass
    return item_list_

def ddd(com, necklace_data, earring1_data, earring2_data, ring1_data, ring2_data):
    N = effect_list(com[0])
    necklace = item_list_(N, necklace_data)

    E1 = effect_list(com[1])
    earring1 = item_list_(E1, earring1_data)

    E2 = effect_list(com[2])
    earring2 = item_list_(E2, earring2_data)

    R1 = effect_list(com[3])
    ring1 = item_list_(R1, ring1_data)

    R2 = effect_list(com[4])
    ring2 = item_list_(R2, ring2_data)

    return necklace, earring1, earring2, ring1, ring2

def charact(c_dic, item_list_):
    for i in item_list_:
        if len(i[1]) == 5:
            # 초기 c_dic = {'치명' : 0, '특화' : 0}
            # 목걸이의 경우 특성을 2개 가지고있음
            c_dic[character[0]] += i[1][character[0]]
            c_dic[character[1]] += i[1][character[1]]

        else:
            try:
                c_dic[character[0]] += i[1][character[0]]
            except:
                c_dic[character[1]] += i[1][character[1]]
    
    #print(c_dic)
    if c_dic[character[0]] >= character_act[0] and c_dic[character[1]] >= character_act[1]:
        return c_dic
    else:
        return 0


def debuff_act(item):
    if '공격속도감소' in item[1]:    
        de_name = '공격속도감소'
        debuff_act = item[1].get('공격속도감소')

    elif '공격력감소' in item[1]:
        de_name = '공격력감소'
        debuff_act = item[1].get('공격력감소')

    elif '이동속도감소' in item[1]:
        de_name = '이동속도감소'
        debuff_act = item[1].get('이동속도감소')

    elif '방어력감소' in item[1]:
        de_name = '방어력감소'
        debuff_act = item[1].get('방어력감소')
    
    return de_name, debuff_act

def debuff(N, E1, E2, R1, R2):
    N_name, N_debuff = debuff_act(N)
    E1_name, E1_debuff = debuff_act(E1)
    E2_name, E2_debuff = debuff_act(E2)
    R1_name, R1_debuff = debuff_act(R1)
    R2_name, R2_debuff = debuff_act(R2)

    d_dic = {'공격속도감소' : 0, '공격력감소' : 0, '이동속도감소' : 0, '방어력감소' : 0}
    d_dic[N_name] += N_debuff
    d_dic[E1_name] += E1_debuff
    d_dic[E2_name] += E2_debuff
    d_dic[R1_name] += R1_debuff
    d_dic[R2_name] += R2_debuff

    if d_dic['공격속도감소'] < 5 and d_dic['공격력감소'] < 5 and d_dic['이동속도감소'] < 5 and d_dic['방어력감소'] < 5:
        return d_dic
    else:
        return 0

#--------------------------

price_list = []
dic_list = []
#character_act = [450, 1400]    # 원하는 특성값

for com in possible_combin:
    necklace, earring1, earring2, ring1, ring2 = ddd(com, necklace_data, earring1_data, earring2_data, ring1_data, ring2_data)
    for N in necklace:
        for E1 in earring1:
            for E2 in earring2:
                # 중복되는 이름의 장비 제외
                if E1[0] == E2[0]:
                    continue
                for R1 in ring1:
                    for R2 in ring2: 
                        # 중복되는 이름의 장비 제외
                        if R1[0] == R2[0]:
                            continue

                        # 특성값의 합이 목표보다 낮은경우 제외
                        c_dic = {}
                        c_dic[character[0]] = 0
                        c_dic[character[1]] = 0
                        c_dic = charact(c_dic, [N, E1, E2, R1, R2])
                        if c_dic == 0:
                            continue

                        # 디버프 레벨이 올라가는경우 제외
                        d_dic = debuff(N, E1, E2, R1, R2)
                        if d_dic == 0:
                            continue

                        price = N[2]+E1[2]+E2[2]+R1[2]+R2[2]
                        price_list.append(price)
                        item = [N, E1, E2, R1, R2, d_dic, c_dic, price]
                        dic_list.append(item)


print('최고가 :', max(price_list))
print('최저가 :', min(price_list))

num = 0
price_list_ = price_list[:] 
pop_price_list = price_list[:] 

while num < 10:
    min_price = pop_price_list.pop(pop_price_list.index(min(pop_price_list)))
    #print(min_price)

    min_index = np.where(np.array(price_list_) == min(price_list_))[0]
    min_index = np.where(np.array(price_list_) == min_price)[0]
    #print('min_index :', min_index)

    for i in min_index:
        item_list = dic_list[i]
        print('\n')
        print('necklace :', item_list[0])
        print('earring1 :', item_list[1])
        print('earring2 :', item_list[2])
        print('ring1 :', item_list[3])
        print('ring2 :', item_list[4])
        print('debuff :', item_list[5], '\ncharacter :', item_list[6], '\nprice :', item_list[7])
        
    num += 1