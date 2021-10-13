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
#-----------------------------------------------------------------------------------------

def tuple_index(tu, list_):
    eff_list = []
    for i in range(len(tu)):
        if tu[i] > 0:
            eff_list.append([ability[i], tu[i]])
    list_.append(eff_list)

def x_path_change(list_):
    list_[0][0] = dic.arousal_dict[list_[0][0]]
    list_[1][0] = dic.arousal_dict[list_[1][0]]


# 목걸이의 유니크 조합만 저장해둔 result_necklace
# 나올 수 있는 가능한 모든 조합을 저장해둔 possible_combin
result_necklace, possible_combin = com.main(ability, ability_lv, item_act)

necklace_list = []
for tu in result_necklace:
    tuple_index(tu, necklace_list)
#print(necklace_list) # [[['강령술', 6], ['원한', 3]], ... , [['갈증', 6], ['강화 무기', 3]]]

for list_ in necklace_list:
    x_path_change(list_)
#print(necklace_list[0])  # [[4, 6], [53, 3]] >> xpath에 맞춰 바꿔줌 ('강령술' == 4)


### input 고정값
item = 11       # 장신구 (11 = 목걸이 (특성2개))
cha = [2, 3]    # [특성1, 특성2]   ############ 특성도 입력받도록 수정해야합니다!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

driver = cr.enter()      # 경매장 접속 + return값으로 driver 받기

combin_ = []   
necklace_ = []
for i in range(len(necklace_list)):
    time.sleep(1)
    item_list = cr.main(driver, item, necklace_list[i], cha)
    if item_list != []:
        necklace_.append(item_list)
        for j in range(len(possible_combin)):
            if possible_combin[j][0] == result_necklace[i]:
                combin_.append(possible_combin[j])


## 결과 찍어보기
for row in combin_:
    print(row)

print('\n')

necklace_ = sum(necklace_, [])
for row in necklace_:
    print(row)


# 이제 combin_에서 귀걸이나 반지의 유니크 조합을 구하면 됨
# 추가로 크롤링 코드에서, 같은 장신구일때는 굳이 장신구를 다시한번 클릭하지 않아도 되기때문에 향후 그부분 수정하면 좋을 것 같음