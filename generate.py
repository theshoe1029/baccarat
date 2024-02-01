import pandas as pd
import random

NEW_SHOE_THRESHOLD = 50
N_HANDS = 1_000_000
N_DECKS = 8

columns = (['player_card1', 'player_card2', 'player_card3',
            'banker_card1', 'banker_card2', 'banker_card3',
            'winner'] + ['n_'+str(i) for i in range(10)])
data = []
shoe_freq = [16*N_DECKS]+[4*N_DECKS]*9
shoe = [0]*16*N_DECKS+[i for i in range(1, 10)]*4*N_DECKS
random.shuffle(shoe)

for _ in range(N_HANDS):
    w = 'T'
    player = [0, 0, -1]
    banker = [0, 0, -1]

    if len(shoe) < NEW_SHOE_THRESHOLD:
        shoe_freq = [16*N_DECKS]+[4*N_DECKS]*9
        shoe = [0]*16*N_DECKS+[i for i in range(1, 10)]*4*N_DECKS
        random.shuffle(shoe)

    player = [shoe.pop(), shoe.pop(), -1]
    banker = [shoe.pop(), shoe.pop(), -1]

    shoe_freq[player[0]] -= 1
    shoe_freq[player[1]] -= 1
    shoe_freq[banker[0]] -= 1
    shoe_freq[banker[1]] -= 1

    s_p = (player[0] + player[1])%10
    s_b = (banker[0] + banker[1])%10

    natural_p = s_p == 8 or s_p == 9
    natural_b = s_b == 8 or s_b == 9

    if not natural_b and s_p < 6:
        player[2] = shoe.pop()
        shoe_freq[player[2]] -= 1
        s_p = (s_p+player[2])%10

    no_player_hit_con = player[2] == -1 and s_b < 6
    player_hit_con = player[2] >= 0 and (s_b <= 2 or (s_b == 3 and player[2] != 8)
                            or (s_b == 4 and player[2] >= 2 and player[2] <= 7)
                            or (s_b== 5 and player[2] >= 4 and player[2] <= 7)
                            or (s_b == 6 and player[2] >= 6 and player[2] <= 7))
    if not natural_p and (no_player_hit_con or player_hit_con):
        banker[2] = shoe.pop()
        shoe_freq[banker[2]] -= 1
        s_b = (s_b+banker[2])%10

    if s_p > s_b:
        w = 'P'
    elif s_p < s_b:
        w = 'B'

    data.append([player[0], player[1], player[2], banker[0], banker[1], banker[2], w] + shoe_freq)

df = pd.DataFrame(data=data, columns=columns)
f = open('hands.csv', 'w')
df.to_csv(f)