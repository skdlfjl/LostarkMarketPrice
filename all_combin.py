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

'''#-----------------------------------------------------------
# 각인 4개 input data
ability = ['각성', '갈증', '강령술', '강화 무기']
ability_lv = [3, 3, 3, 3]
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
ability_in_act = [???????????]
#### 원하는 특성을 받을 변수가 필요합니다
#### 원하는 특성합을 받을 변수가 필요합니다'''
#-----------------------------------------------------------
# 각인 5개 input data
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패']
ability_lv = [3, 3, 3, 3, 3]
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
ability_in_act = [7, 7, 0, 12, 9]
#### 원하는 특성을 받을 변수가 필요합니다
#### 원하는 특성합을 받을 변수가 필요합니다
#-----------------------------------------------------------
'''# 각인 6개 (고대등급 x) input data
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패' '원한']
ability_lv = [3, 3, 3, 3, 3, 1]
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
ability_in_act = [10, 10, 0, 12, 9, 0]
#### 원하는 특성을 받을 변수가 필요합니다
#### 원하는 특성합을 받을 변수가 필요합니다
#-----------------------------------------------------------
# 각인 6개 (고대등급 O) input data
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패' '원한']
ability_lv = [3, 3, 3, 3, 3, 2]
ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
ability_in_act = [10, 10, 0, 12, 12, 0]
#### 원하는 특성을 받을 변수가 필요합니다
#### 원하는 특성합을 받을 변수가 필요합니다'''
#-----------------------------------------------------------

ability_act = list(map(operator.sub, ability_lv_act, ability_in_act))
# ability_act는 ability_lv_act - ability_in_act (장신구로 채워야하는 활성도)


# 각인 개수는 2개부터 6개까지 설정 가능하도록 프로그래밍 했다
# 333332만 고대등급 장신구를 고려한다
combi = list(permutations(act_33 + [0]*(len(ability)-2), len(ability)))  # 각인 4개면 [3, 3, 0, 0]
combi_33 = list(set(combi))
combi = list(permutations(act_43 + [0]*(len(ability)-2), len(ability)))
combi_43 = list(set(combi))
combi = list(permutations(act_53 + [0]*(len(ability)-2), len(ability)))
combi_53 = list(set(combi))

if 4 <= len(ability) <= 6 and sum(ability_lv) < 17:   # 각인 4,5,6개 + 333332이 아닐경우 - 고대등급 X
    all_combi = combi_33 + combi_43 + combi_53
    print('고대등급X) 모든 조합 구하기 성공!!')

elif len(ability) == 6 and sum(ability_lv) == 17:     # 각인이 6개 + 333332인 경우 - 고대등급 O
    combi = list(permutations(act_63 + [0]*(len(ability)-2), len(ability)))
    combi_63 = list(set(combi))
    all_combi = combi_33 + combi_43 + combi_53 + combi_63   # 63까지 고려 (고대등급)
    print('고대등급O) 모든 조합 구하기 성공')

else:
    print('장신구 능력치로는 부족할경우 다시 작성하도록')

all_combi_index = []
for i in range(len(all_combi)):
    all_combi_index.append(i)

shuffle_index = list(permutations(all_combi_index, 4)) # 인덱스를 섞어준다
# (0, 1, 2, 3) >> all_combi 리스트 안 0번째, 1번째, 2번째, 3번째 튜플의 인덱스
# 인덱스는 무조건 4개가 나와야한다 (그래야 장신구 5개의 조합을 맞추기 때문)




for neck in all_combi:
    for a, b, c, d in shuffle_index:
        for i in range(len(ability)):
            if neck[i] + all_combi[a][i] + all_combi[b][i] + all_combi[c][i] + all_combi[d][i] == ability_act[i]:
                if i == len(ability)-1:
                    print(neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d])
                    necklace.append(neck)
                    earring1.append(all_combi[a])
                    earring2.append(all_combi[b])
                    ring1.append(all_combi[c])
                    ring2.append(all_combi[d])
                    a = [neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d]]
                    possible_combin.append(a)
            else: break




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
'''

combin_ = []
for i in range(len(possible_combin)):
    if possible_combin[i][0] != (0, 5, 0, 3, 0):      # i번째 조합에서 목걸이의 데이터가 (0, 5, 0, 3, 0) 아닌 것들만
        combin_.append(possible_combin[i])    # 새로 저장해라 (목걸이가 0 5 0 3 0 값을 만족시키는게 없으니까 필요없는 조합임)

for row in combin_:
    print(row)

# 여기까지 3~4분




