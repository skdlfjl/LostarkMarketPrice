from itertools import combinations, combinations_with_replacement, permutations, product
import operator
import numpy as np

### input data ###  >>> 예시입니당
# 각인 6개 (고대등급 O) input data
ability = ['각성', '갈증', '강령술', '강화 무기', '강화 방패', '원한']
ability_lv = [3, 3, 3, 3, 3, 2]
item_act = [10, 0, 0, 12, 12, 8]    # 333332
#-----------------------------------------------------------------------------------------

def save_item_combi(neck, ear1, ear2, rin1, rin2, necklace, possible_combin):
    necklace.append(neck)
    possible_combin.append([neck, ear1, ear2, rin1, rin2])
    #print(neck, ear1, ear2, rin1, rin2)

# 실제로 사용자가 입력하는 데이터 : ability, ability_lv, item_act
def main(ability, ability_lv, item_act):
    act_33 = [3,3]   # 유물등급
    act_43 = [4,3]
    act_53 = [5,3]
    act_63 = [6,3]   # 고대등급

    ability_lv_act = [i*5 for i in ability_lv]    # 입력받은 레벨에 *5 한 값을 저장한다
    ability_act = list(map(operator.sub, ability_lv_act, item_act))
    # ability_act = ability_lv_act - item_act (장신구로 채워야하는 활성도)

    # 만약 마이너스 값이 들어오면 자동으로 0 치환해줌
    for i in range(len(ability_act)):
        if ability_act[i] < 0:
            item_act[i] = item_act[i] - ability_act[i]  # item_act값을 마이너스값만큼 빼준다
            ability_act[i] = 0   # 마이너스값을 0으로 치환해준다


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
            # 3, 4, 5로 만들 수 없는 1, 2를 3으로 치환
            if 1 in ability_act: ability_act[ability_act.index(1)] = 3
            if 2 in ability_act: ability_act[ability_act.index(2)] = 3

        ##-------(위는 유물등급만 고려, 아래는 유물+고대 혹은 고대등급만 고려)-------
        # 일치하는 조합만 구하지 않고, 합이 원하는값 이상인 조합을 전부 구한다
        # 따라서 값을 치환해주지 않아도 된다. 값이 1, 2가 나와도 그냥 그 이상인 값이 들어갈테니!

        # 레벨의 합이 16이고, 보물+각인서 합이 35이상 39이하인 경우 53, 63 (333331)
        # 레벨의 합이 17이고, 보물+각인서 합이 40이상인 경우 53, 63 (333332) / 40일때는 63 장신구만
        # 필요한 돌과 각인서의 최소값 = 장신구 5개의 최대 능력치(63) 
        elif (sum(ability_lv) == 17 and 40 <= sum(item_act)) or (sum(ability_lv) == 16 and 35 <= sum(item_act) <= 39):
            item_act_min = sum(ability_lv_act) - sum(act_63)*5 

    # 만약 최소한으로 필요한 보물+각인서 활성값을 맞추지 못했거나
    # 각인의 개수가 4~6개 범위를 벗어난경우, item_act_min에 999값을 넣어준다
    else: item_act_min = 999


    if item_act_min <= sum(item_act):
        combi = list(permutations(act_33 + [0]*(len(ability)-2), len(ability)))  # 각인 4개면 [3, 3, 0, 0]
        combi_33 = list(set(combi))
        combi = list(permutations(act_43 + [0]*(len(ability)-2), len(ability)))
        combi_43 = list(set(combi))
        combi = list(permutations(act_53 + [0]*(len(ability)-2), len(ability)))
        combi_53 = list(set(combi))
        combi = list(permutations(act_63 + [0]*(len(ability)-2), len(ability)))
        combi_63 = list(set(combi))

        # 사용자가 입력한 돌+각인서 활성도 값 합이 [ 필요 활성도 합 - (5+3)*5 ] 와 같을 경우
        # 53 장신구로만 조합이 나오도록! (53장신구로만 조합해야 가능하기때문)  
        if sum(item_act) == sum(ability_lv_act) - sum(act_53)*5:       
            all_combi = combi_53
            print('53장신구로만 조합가능 (장신구 활성도 합 40)')    
        elif len(ability) == 6 and sum(item_act) == sum(ability_lv_act) - sum(act_63)*5: 
            # 고대등급으로만 조합하는건 각인 6개부터!
            all_combi = combi_63
            print('63장신구로만 조합가능 (장신구 활성도 합 45)')  

        else:  # 만약 전부 아닐경우, 기존의 방식대로 작동하도록!!
            # 각인이 4~5개인 경우 33, 43, 53
            if 4 <= len(ability) <= 5:
                all_combi = combi_33 + combi_43 + combi_53
                print('각인이 4~5개인 경우 : 33, 43, 53')
           
            # 각인이 6개인데, 
            elif len(ability) == 6:
                # 레벨의 합이 16보다 작은경우 (333321이 최대) 43, 53
                # 레벨의 합이 16이고, 보물+각인서 합이 40 이상인 경우 43, 53 (333331)
                if sum(ability_lv) < 16 or (sum(ability_lv) == 16 and 40 <= sum(item_act)):
                    all_combi = combi_43 + combi_53
                    print('각인 6개 (최대 333321 or 333331 + item_act 40이상) : 43, 53')

                # 유물 + 고대
                # 레벨의 합이 16이고, 보물+각인서 합이 35이상 39이하인 경우 53, 63 (333331)
                # 레벨의 합이 17이고, 보물+각인서 합이 40이상인 경우 63 (333332)
                elif (sum(ability_lv) <= 16 and 35 <= sum(item_act) <= 39) or (sum(ability_lv) == 17 and 40 < sum(item_act)):
                    all_combi = combi_53 + combi_63
                    if sum(ability_lv) == 16: print('각인 6개 / 333331 / 35 <= (보물+각인서) <= 39 : 53, 63(고대)')
                    elif sum(ability_lv) == 17: print('각인 6개 / 333332 / 40 < (보물+각인서) : 53, 63(고대)')

        ## all_combi : 
        #       사용자가 원하는 활성도를 위해, 적용 가능한 각인의 활성도의 모든 조합
        #       예를들어 고대등급만 가능하다면 [(6,3,0,0,0,0), (0,6,3,0,0,0), ...]

        all_combi_index = []
        for i in range(len(all_combi)):
            all_combi_index.append(i)
        #############################################################################################################################
        #shuffle_index = list(permutations(all_combi_index, 4)) # 인덱스를 섞어준다
        # 기존 코드

        print('all_combi :', all_combi)
        s = list(combinations_with_replacement(all_combi_index, 2))
        shuffle_index = []
        for i in s:
            for j in s:
                shuffle_index.append(i + j)

        # (0, 1, 2, 3) >> all_combi 리스트 안 0번째, 1번째, 2번째, 3번째 튜플의 인덱스
        # 인덱스는 무조건 4개가 나와야한다 (그래야 아래 코드에서 목걸이까지 추가해 장신구 5개의 조합을 맞추기 때문)
        #############################################################################################################################

        necklace = []
        possible_combin = []
        for neck in all_combi:
            for a, b, c, d in shuffle_index:
                if len(ability) == 4:
                    if neck[0] + all_combi[a][0] + all_combi[b][0] + all_combi[c][0] + all_combi[d][0] == ability_act[0]:
                        if neck[1] + all_combi[a][1] + all_combi[b][1] + all_combi[c][1] + all_combi[d][1] == ability_act[1]:
                            if neck[2] + all_combi[a][2] + all_combi[b][2] + all_combi[c][2] + all_combi[d][2] == ability_act[2]:
                                if neck[3] + all_combi[a][3] + all_combi[b][3] + all_combi[c][3] + all_combi[d][3] == ability_act[3]:
                                    save_item_combi(neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d], necklace, possible_combin)
                            else: continue
                        else: continue
                    else: continue

                elif len(ability) == 5:
                    if neck[0] + all_combi[a][0] + all_combi[b][0] + all_combi[c][0] + all_combi[d][0] == ability_act[0]:
                        if neck[1] + all_combi[a][1] + all_combi[b][1] + all_combi[c][1] + all_combi[d][1] == ability_act[1]:
                            if neck[2] + all_combi[a][2] + all_combi[b][2] + all_combi[c][2] + all_combi[d][2] == ability_act[2]:
                                if neck[3] + all_combi[a][3] + all_combi[b][3] + all_combi[c][3] + all_combi[d][3] == ability_act[3]:
                                    if neck[4] + all_combi[a][4] + all_combi[b][4] + all_combi[c][4] + all_combi[d][4] == ability_act[4]:
                                        save_item_combi(neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d], necklace, possible_combin)
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
                                            save_item_combi(neck, all_combi[a], all_combi[b], all_combi[c], all_combi[d], necklace, possible_combin)
                                    else: continue
                                else: continue
                            else: continue
                        else: continue
                    else: continue


        # 우선 목걸이의 유니크 조합 구하기 >> 크롤링 할 것 뽑아내기
        result_necklace = list(set(necklace))
        print('possible_combin :', len(possible_combin))
        print('result_necklace :', result_necklace)
        return result_necklace, possible_combin



    else: print('돌과 각인서의 활성도가 부족하거나 각인의 개수가 4~6개가 아닙니다.')
