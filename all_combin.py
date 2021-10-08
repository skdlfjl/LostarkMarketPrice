from itertools import combinations, permutations, product
import operator
import numpy as np

act_33 = [3,3]   # 유물등급
act_43 = [4,3]
act_53 = [5,3]
act_63 = [6,3]   # 고대등급

necklace = []
earring1 = []
earring2 = []
ring1 = []
ring2 = []
possible_combin = []

def save_item_combi(neck, ear1, ear2, rin1, rin2):
    necklace.append(neck)
    earring1.append(ear1)
    earring2.append(ear2)
    ring1.append(rin1)
    ring2.append(rin2)
    a = [neck, ear1, ear2, rin1, rin2]
    possible_combin.append(a)
    print(neck, ear1, ear2, rin1, rin2)

'''#-----------------------------------------------------------
# 각인 4개 input data  (초 - 약 분)
ability = ['각성', '갈증', '강령술', '강화 무기']
ability_lv = [3, 3, 3, 3]
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
ability_in_act = [6, 6, 9, 9]
#### 원하는 특성을 받을 변수가 필요합니다
#### 원하는 특성합을 받을 변수가 필요합니다
#-----------------------------------------------------------
# 각인 5개 input data  (294~302초 - 약 5분)
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패']
ability_lv = [3, 3, 3, 3, 3]
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
ability_in_act = [7, 7, 0, 12, 9]
#### 원하는 특성을 받을 변수가 필요합니다
#### 원하는 특성합을 받을 변수가 필요합니다'''
#-----------------------------------------------------------
# 각인 6개 (고대등급 O) input data
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패', '원한']
ability_lv = [3, 3, 3, 3, 3, 1]
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
#item_act = [9, 0, 0, 12, 12, 7]     # 333332
#item_act = [10, 0, 0, 12, 12, 8]    # 333332
item_act = [9, 0, 7, 12, 12, 0]     # 333331 - 1493초 >> 996초
#item_act = [10, 0, 7, 12, 12, 0]    # 333331 - 986초
ability_act = list(map(operator.sub, ability_lv_act, item_act))
# ability_act는 ability_lv_act - item_act (장신구로 채워야하는 활성도)
#-----------------------------------------------------------



# 각인이 4~5개인 경우 33, 43, 53
# 필요한 돌과 각인서의 최소값 = 장신구 5개의 최대 능력치(53)
if 4 <= len(ability) <= 5:
    item_act_min = sum(ability_lv_act) - sum(act_53)*5 
    # 3, 4, 5로 만들 수 없는 1, 2를 3으로 치환
    if 1 in ability_act: ability_act[ability_act.index(1)] = 3
    if 2 in ability_act: ability_act[ability_act.index(2)] = 3

# 각인이 6개인데, 
elif len(ability) == 6:
    # 레벨의 합이 16보다 작은경우 (333321이 최대) 43, 53
    # 레벨의 합이 16이고, 보물+각인서 합이 40 이상인 경우 43, 53 (333331)
    if sum(ability_lv) < 16 or (sum(ability_lv) == 16 and 40 <= sum(item_act)):
        item_act_min = sum(ability_lv_act) - sum(act_53)*5 
        if 1 in ability_act: ability_act[ability_act.index(1)] = 3
        if 2 in ability_act: ability_act[ability_act.index(2)] = 3

    ##-------(위는 유물등급만 고려, 아래는 유물+고대 혹은 고대등급만 고려)-------
    # 일치하는 조합만 구하지 않고, 합이 원하는값 이상인 조합을 전부 구한다
    # 따라서 값을 치환해주지 않아도 된다. 값이 1, 2가 나와도 그냥 그 이상인 값이 들어갈테니!

    # 레벨의 합이 16이고, 보물+각인서 합이 35이상 39이하인 경우 53, 63 (333331)
    # 필요한 돌과 각인서의 최소값 = 장신구 5개의 최대 능력치(63) 
    elif sum(ability_lv) == 16 and 35 <= sum(item_act) <= 39:
        item_act_min = sum(ability_lv_act) - sum(act_63)*5 

    # 레벨의 합이 17이고, 보물+각인서 합이 40이상인 경우 63 (333332)
    elif sum(ability_lv) == 17 and 40 <= sum(item_act):
        item_act_min = sum(ability_lv_act) - sum(act_63)*5 

# 만약 최소한으로 필요한 보물+각인서 활성값을 맞추지 못했거나
# 각인의 개수가 4~6개 범위를 벗어난경우, item_act_min에 999값을 넣어준다
else: item_act_min = 999


print(item_act_min)
if item_act_min <= sum(item_act):
    combi = list(permutations(act_43 + [0]*(len(ability)-2), len(ability)))
    combi_43 = list(set(combi))
    combi = list(permutations(act_53 + [0]*(len(ability)-2), len(ability)))
    combi_53 = list(set(combi))
    combi = list(permutations(act_63 + [0]*(len(ability)-2), len(ability)))
    combi_63 = list(set(combi))

    # 각인이 4~5개인 경우 33, 43, 53
    if 4 <= len(ability) <= 5:
        combi = list(permutations(act_33 + [0]*(len(ability)-2), len(ability)))  # 각인 4개면 [3, 3, 0, 0]
        combi_33 = list(set(combi))
        all_combi = combi_33 + combi_43 + combi_53
        print('각인이 4~5개인 경우 : 33, 43, 53')
    
    # 각인이 6개인데, 
    elif len(ability) == 6:
        # 레벨의 합이 16보다 작은경우 (333321이 최대) 43, 53
        # 레벨의 합이 16이고, 보물+각인서 합이 40 이상인 경우 43, 53 (333331)
        if sum(ability_lv) < 16 or (sum(ability_lv) == 16 and 40 <= sum(item_act)):
            all_combi = combi_43 + combi_53
            print('각인 6개 (최대 333321 or 333331 + item_act 40이상) : 43, 53')

        # 레벨의 합이 16이고, 보물+각인서 합이 35이상 39이하인 경우 53, 63 (333331)
        elif sum(ability_lv) == 16 and 35 <= sum(item_act) <= 39:
            all_combi = combi_53 + combi_63
            print('각인 6개 / 333331 / 35 <= (보물+각인서) <= 39 : 53, 63(고대)')

        # 레벨의 합이 17이고, 보물+각인서 합이 40이상인 경우 63 (333332)
        elif sum(ability_lv) == 17 and 40 <= sum(item_act):
            all_combi = combi_63
            print('각인 6개 / 333331 / 40 <= (보물+각인서) : 63(고대)')

    ## all_combi : 
    #       사용자가 원하는 활성도를 위해, 적용 가능한 각인의 활성도의 모든 조합
    #       예를들어 고대등급만 가능하다면 [(6,3,0,0,0,0), (0,6,3,0,0,0), ...]

    all_combi_index = []
    for i in range(len(all_combi)):
        all_combi_index.append(i)
    shuffle_index = list(permutations(all_combi_index, 4)) # 인덱스를 섞어준다
    # (0, 1, 2, 3) >> all_combi 리스트 안 0번째, 1번째, 2번째, 3번째 튜플의 인덱스
    # 인덱스는 무조건 4개가 나와야한다 (그래야 장신구 5개의 조합을 맞추기 때문)


    for neck in all_combi:
        for a, b, c, d in shuffle_index:
            if len(ability) == 4:
                if neck[0] + all_combi[a][0] + all_combi[b][0] + all_combi[c][0] + all_combi[d][0] == ability_act[0]:
                    if neck[1] + all_combi[a][1] + all_combi[b][1] + all_combi[c][1] + all_combi[d][1] == ability_act[1]:
                        if neck[2] + all_combi[a][2] + all_combi[b][2] + all_combi[c][2] + all_combi[d][2] == ability_act[2]:
                            if neck[3] + all_combi[a][3] + all_combi[b][3] + all_combi[c][3] + all_combi[d][3] == ability_act[3]:
                                save_item_combi(neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d])
                        else: continue
                    else: continue
                else: continue

            elif len(ability) == 5:
                if neck[0] + all_combi[a][0] + all_combi[b][0] + all_combi[c][0] + all_combi[d][0] == ability_act[0]:
                    if neck[1] + all_combi[a][1] + all_combi[b][1] + all_combi[c][1] + all_combi[d][1] == ability_act[1]:
                        if neck[2] + all_combi[a][2] + all_combi[b][2] + all_combi[c][2] + all_combi[d][2] == ability_act[2]:
                            if neck[3] + all_combi[a][3] + all_combi[b][3] + all_combi[c][3] + all_combi[d][3] == ability_act[3]:
                                if neck[4] + all_combi[a][4] + all_combi[b][4] + all_combi[c][4] + all_combi[d][4] == ability_act[4]:
                                    save_item_combi(neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d])
                            else: continue    
                        else: continue
                    else: continue
                else: continue

            # 각인이 6개면 일치하는 조합만 구하지 않고, 활성도의 합이 원하는값 이상인 조합을 전부 구한다
            elif len(ability) == 6:
                if neck[0] + all_combi[a][0] + all_combi[b][0] + all_combi[c][0] + all_combi[d][0] >= ability_act[0]:
                    if neck[1] + all_combi[a][1] + all_combi[b][1] + all_combi[c][1] + all_combi[d][1] >= ability_act[1]:
                        if neck[2] + all_combi[a][2] + all_combi[b][2] + all_combi[c][2] + all_combi[d][2] >= ability_act[2]:
                            if neck[3] + all_combi[a][3] + all_combi[b][3] + all_combi[c][3] + all_combi[d][3] >= ability_act[3]:
                                if neck[4] + all_combi[a][4] + all_combi[b][4] + all_combi[c][4] + all_combi[d][4] >= ability_act[4]:
                                    if neck[5] + all_combi[a][5] + all_combi[b][5] + all_combi[c][5] + all_combi[d][5] >= ability_act[5]:
                                        save_item_combi(neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d])
                                else: continue
                            else: continue
                        else: continue
                    else: continue
                else: continue


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


# result_necklace, result_earring, result_ring 세가지를 이용하여 데이터를 크롤링해야 합니다.
# crawling.py를 함수화 시켜 입력값에 따라 크롤링이 가능하도록 변경해야 합니다
# 만약 크롤링 할 데이터가 없다면 해당 값이 들어있는 조합을 전부 삭제해야 합니다.

'''
예를들어 목걸이의 (0, 5, 0, 3, 0) 데이터를 크롤링 하려 합니다

0이 아닌 5와 3의 값이 들어있는 자리는 index 1, 3 이므로 목걸이의 각인은 갈증(활성도5), 강화 무기(활성도3)이 됩니다
추가로 처음 input으로 받은 특성 또한 고려해야 합니다 (특성값은 검색할 때 따로 설정하지 않습니다)

만일 각인과 각인 값, 특성을 만족하는 목걸이가 없으면 우리는 아래와 같은 방법으로 해당 조합을 전부 삭제해줘야 한다


combin_ = []
for i in range(len(possible_combin)):
    if possible_combin[i][0] != (0, 5, 0, 3, 0):      # i번째 조합에서 목걸이의 데이터가 (0, 5, 0, 3, 0) 아닌 것들만
        combin_.append(possible_combin[i])    # 새로 저장해라 (목걸이가 0 5 0 3 0 값을 만족시키는게 없으니까 필요없는 조합임)

for row in combin_:
    print(row)

'''



else: print('돌과 각인서의 활성도가 부족하거나 각인의 개수가 4~6개가 아닙니다.')
