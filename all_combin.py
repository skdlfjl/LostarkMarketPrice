from itertools import combinations, permutations, product
import operator
import numpy as np


act_33 = [3,3,0,0,0]
act_43 = [4,3,0,0,0]
act_53 = [5,3,0,0,0]
act_63 = [6,3,0,0,0]

combi = list(permutations(act_33, 5))
combi_33 = list(set(combi))
combi = list(permutations(act_43, 5))
combi_43 = list(set(combi))
combi = list(permutations(act_53, 5))
combi_53 = list(set(combi))
combi = list(permutations(act_63, 5))
combi_63 = list(set(combi))

#combi = combi_33 + combi_43 + combi_53 + combi_63   # 63까지 고려 (고대등급)
all_combi = combi_33 + combi_43 + combi_53

all_combi_index = []
for i in range(len(all_combi)):
    all_combi_index.append(i)

index_4 = list(permutations(all_combi_index, 4))   # 인덱스를 추출해서 섞어준다
#print(index_4[0])     
# (0, 1, 2, 3)  >> all_combi리스트 안에 들어있는 0번째, 1번째, 2번째, 3번째 튜플의 인덱스


#--------------------------------------------------



# input : 3 3 3 3 3 / 돌 : 7 7 / 각인서 : 12 9
'''  
    1. 원하는 각인과 각인 레벨 >>       (여기서 input으로 각인 이름과 레벨을 받습니다)
    각성       >  3 Lv
    갈증       >  3 Lv
    강령술     >  3 Lv
    강화 무기  >  3 Lv
    강화 방패  >  3 Lv
    저장 변수(각인 이름과 레벨*5 저장) = ability / ability_lv


     2. 적용할 돌 / 각인서1 / 각인서2의 능력치(활성도) >>     (위에서 받은 각인 이름을 가져와 쓰기)
    각성       >  7
    갈증       >  7
    강령술     >  0
    강화 무기  >  12
    강화 방패  >  9
    저장 변수()

     3. 특성합 >>
    (나중에 고려합시다....0)

'''
# input data
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패']
ability_lv_act = [15, 15, 15, 15, 15]     # 입력받은 레벨에 *5 한 값을 저장한다
ability_act = [7, 7, 0, 12, 9]
#### 원하는 특성을 받을 변수가 필요합니다
#### 원하는 특성합을 받을 변수가 필요합니다

ability_act = list(map(operator.sub, ability_lv_act, ability_act))
# ability_act는 [8, 8, 15, 3, 6]이 된다


# 위에서 만들어둔 나올 수 있는 모든 조합을 저장한 리스트 combi에서 하나씩 가져와 
# 5개 각인의 능력치가 합쳤을 때 8 8 15 3 6 이 되는 모든 조합을 찾는다
necklace = []
earring1 = []
earring2 = []
ring1 = []
ring2 = []
possible_combin = []
for ex in all_combi:
    for a, b, c, d in index_4:
        if ex[0] + all_combi[a][0] + all_combi[b][0] + all_combi[c][0] + all_combi[d][0] == ability_act[0]:
            if ex[1] + all_combi[a][1] + all_combi[b][1] + all_combi[c][1] + all_combi[d][1] == ability_act[1]:
                if ex[2] + all_combi[a][2] + all_combi[b][2] + all_combi[c][2] + all_combi[d][2] == ability_act[2]:
                    if ex[3] + all_combi[a][3] + all_combi[b][3] + all_combi[c][3] + all_combi[d][3] == ability_act[3]:
                        if ex[4] + all_combi[a][4] + all_combi[b][4] + all_combi[c][4] + all_combi[d][4] == ability_act[4]:
                            #print(ex, all_combi[a], all_combi[b], all_combi[c], all_combi[d])
                            necklace.append(ex)
                            earring1.append(all_combi[a])
                            earring2.append(all_combi[b])
                            ring1.append(all_combi[c])
                            ring2.append(all_combi[d])

                            a = [ex, all_combi[a], all_combi[b], all_combi[c], all_combi[d]]
                            possible_combin.append(a)
                            # possible_combin == [[(0, 5, 3, 0, 0), (0, 0, 3, 3, 0), (5, 0, 3, 0, 0), (3, 0, 0, 0, 6), (0, 3, 6, 0, 0)],
                            #                     [(0, 4, 0, 0, 3), (0, 4, 0, 3, 0), (5, 0, 3, 0, 0), (0, 0, 6, 0, 3), (3, 0, 6, 0, 0)],
                            #                     [(0, 5, 3, 0, 0), (0, 0, 3, 3, 0),               ......              (3, 0, 6, 0, 0)]]
                            # 대충 이런식으로 생긴 중첩 리스트들이 나옵니다
                            #
                            # n은 조합의 총 개수
                            # 두번째 []는 장신구의 종류 (0 = 목걸이 / 1 = 귀걸이1 / 2 = 귀걸이2 / 3 = 반지1 / 4 = 반지2)
                            # 세번째 []는 각인의 종류 (0 = 각성 / 1 = 갈증 / 2 = 강령술 / 3 = 강화 무기 / 4 = 강화 방패)
                            # ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패'] 를 참고하면 됩니다 (같은 인덱스를 가집니다)
                            
                            # possible_combin[n][0][0] == 목걸이 장신구의 '각성' 활성도
                            # possible_combin[n][1][0] == 귀걸이1 장신구의 '갈증' 활성도
                    

                    else: continue
                else: continue
            else: continue
        else: continue
    else: continue
# 여기까지 한 4분 걸림~~~~


# 크롤링할 조합 구하기
result_necklace = list(set(necklace))
result_earring = list(set(earring1 + earring2))
result_ring = list(set(ring1 + ring2))

print('\n')
print(result_necklace)
print('\n')
print(result_earring)
print('\n')
print(result_ring)
print('\n')
# 

# result_necklace, result_earring, result_ring 세가지를 이용하여 데이터를 크롤링해야 합니다.
# crawling.py를 함수화 시켜 입력값에 따라 크롤링이 가능하도록 변경해야 합니다
# 만약 크롤링 할 데이터가 없다면 해당 값이 들어있는 조합을 전부 삭제해야 합니다.

'''
예를들어 목걸이의 (0, 5, 0, 3, 0) 데이터를 크롤링 하려 합니다

0이 아닌 5와 3의 값이 들어있는 자리는 index 1, 3 이므로 목걸이의 각인은 갈증(활성도5), 강화 무기(활성도3)이 됩니다
추가로 처음 input으로 받은 특성 또한 고려해야 합니다 (특성값은 검색할 때 따로 설정하지 않습니다)

만일 각인과 각인 값, 특성을 만족하는 목걸이가 없으면 우리는 아래와 같은 방법으로 해당 조합을 전부 삭제해줘야 한다
'''

combin_ = []
for i in range(len(possible_combin)):
    if possible_combin[i][0] != (0, 5, 0, 3, 0):      # i번째 조합에서 목걸이의 데이터가 (0, 5, 0, 3, 0) 아닌 것들만
        combin_.append(possible_combin[i])    # 새로 저장해라 (목걸이가 0 5 0 3 0 값을 만족시키는게 없으니까 필요없는 조합임)

for row in combin_:
    print(row)

# 여기까지 3분

