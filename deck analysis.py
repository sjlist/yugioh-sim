import random
import time
import deck_functionality.py

def play_hand(deck):
    hand_size = 6
    banish = []
    hand = []
    
    draw_num(hand_size, deck, hand)
    
    while (('Resonator Call' in hand)
     and  (('Flare Resonator' in deck)
       or  ('Creation Resonator' in deck)
       or  ('Synkron Resonator' in deck))):
        
        hand.remove('Resonator Call')
        if (('Creation Resonator' not in hand)
       and  ('Creation Resonator' in deck)):
            add_card('Creation Resonator', deck, hand)
        elif (('Flare Resonator' not in hand)
         and  ('Flare Resonator' in deck)):
            add_card('Flare Resonator', deck, hand)
        elif (('Synkron Resonator' not in hand)
         and  ('Synkron Resonator' in deck)):
            add_card('Synkron Resonator', deck, hand)

        elif ('Creation Resonator' in deck):
            add_card('Creation Resonator', deck, hand)
        elif ('Flare Resonator' in deck):
            add_card('Flare Resonator', deck, hand)
        elif ('Synkron Resonator' in deck):

            add_card('Synkron Resonator', deck, hand)
          
    if 'Upstart' in hand:
        hand.remove('Upstart')
        draw_num(1, deck, hand)
    
    if 'Pot of Desires' in hand:
        hand.remove('Pot of Desires')
        banish_rand(10, deck)
        draw_num(2,deck, hand)

    while (('Resonator Call' in hand)
     and  (('Flare Resonator' in deck)
       or  ('Creation Resonator' in deck)
       or  ('Synkron Resonator' in deck))):
        
        hand.remove('Resonator Call')
        if (('Creation Resonator' not in hand)
       and  ('Creation Resonator' in deck)):
            add_card('Creation Resonator', deck, hand)
        elif (('Flare Resonator' not in hand)
         and  ('Flare Resonator' in deck)):
            add_card('Flare Resonator', deck, hand)
        elif (('Synkron Resonator' not in hand)
         and  ('Synkron Resonator' in deck)):
            add_card('Synkron Resonator', deck, hand)

        elif ('Creation Resonator' in deck):
            add_card('Creation Resonator', deck, hand)
        elif ('Flare Resonator' in deck):
            add_card('Flare Resonator', deck, hand)
        elif ('Synkron Resonator' in deck):
            add_card('Synkron Resonator', deck, hand)

    if 'Upstart' in hand:
        hand.remove('Upstart')
        draw_num(1, deck, hand)
        
    return hand

#Legend for test_hand
#0: brick, cant make a synchro
#1: can make 1 lvl 6 sync
#2: can make 1 lvl 7 sync
#3: can make 1 lvl 8 sync
#4: can make 1 lvl 9 sync
#5: can make 1 lvl 10 sync
#6: can make 1 lvl 12 sync
#7: can make 1 lvl 8 sync and 1 lvl 9 sync
#8: can make 1 lvl 9 sync and 1 lvl 9 sync
#9: can make 1 lvl 8 sync and 1 lvl 12 sync
#10: can make 1 lvl 9 sync and 1 lvl 12 sync
     
def test_hand(hand):
    
    handDict = {'Flare Resonator' : 0,
                'Creation Resonator' : 0,
                'Synkron Resonator' : 0,
                'Level 5' : 0,
                'Return of the Dragon Lords' : 0,
                'Pot of Desires' : 0,
                'Resonator Call' : 0,
                'Card' : 0}

    for element in hand:
        handDict[element] +=  1

    if (handDict['Level 5'] >= 1
    and handDict['Creation Resonator'] >= 1
    and (handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 2
    and handDict['Synkron Resonator'] >= 2
    and handDict['Return of the Dragon Lords'] >= 1):
        return 10
    
    if (handDict['Level 5'] >= 1
    and handDict['Creation Resonator'] >= 1
    and (handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 2
    and handDict['Synkron Resonator'] >= 1
    and handDict['Return of the Dragon Lords'] >= 1):
        return 9
    
    if (handDict['Level 5'] >= 1
    and (handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 1
    and handDict['Synkron Resonator'] >= 2
    and handDict['Return of the Dragon Lords'] >= 1):
        return 8

    if (handDict['Level 5'] >= 1
    and (handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 1
    and handDict['Synkron Resonator'] >= 1
    and handDict['Return of the Dragon Lords'] >= 1):
        return 7

    if (handDict['Level 5'] >= 1
    and handDict['Creation Resonator'] >= 1        
    and (handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 2
    and handDict['Synkron Resonator'] >= 1):
        return 6

    if (handDict['Level 5'] >= 1       
    and (handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 1
    and handDict['Synkron Resonator'] >= 2):
        return 5

    if (handDict['Level 5'] >= 1       
    and (handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 1
    and handDict['Synkron Resonator'] >= 1):
        return 4

    if (handDict['Level 5'] >= 1       
    and ((handDict['Flare Resonator'] + handDict['Creation Resonator']) >= 1)):
        return 3

    if (handDict['Level 5'] >= 1       
    and handDict['Synkron Resonator'] >= 2):
        return 2

    if (handDict['Level 5'] >= 1       
    and handDict['Synkron Resonator'] >= 1):
        return 1
    
    return 0
        
def chance_to_brick(number_of_hands):
    start_time = time.time()
    tries = 0
    fails = 0
    successes = 0
    resultDict = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0}        

    while tries < number_of_hands:
        deck = make_deck()
        hand = play_hand(deck)
        result  = test_hand(hand)

        resultDict[result] += 1
        
        tries += 1

    stop_time = time.time()

    fails = resultDict[0]
    successes = tries - fails

    tries = float(tries)
    success_rate = successes/tries*100
    fail_rate = fails/tries*100
    calc_time = stop_time - start_time

    print('Success Rate:    ' + str(success_rate))
    print('Fail Rate:       ' + str(fail_rate))
    print('Calcultion time: ' + str(calc_time))
    print('In Depth Plays')
    print('Chance to brick:                               ' + str(resultDict[0]/tries*100))
    print('Chance to make 1 lvl 6 sync:                   ' + str(resultDict[1]/tries*100))
    print('Chance to make 1 lvl 7 sync:                   ' + str(resultDict[2]/tries*100))
    print('Chance to make 1 lvl 8 sync:                   ' + str(resultDict[3]/tries*100))
    print('Chance to make 1 lvl 9 sync:                   ' + str(resultDict[4]/tries*100))
    print('Chance to make 1 lvl 10 sync:                  ' + str(resultDict[5]/tries*100))
    print('Chance to make 1 lvl 12 sync:                  ' + str(resultDict[6]/tries*100))
    print('Chance to make 1 lvl 8 sync and 1 lvl 9 sync:  ' + str(resultDict[7]/tries*100))
    print('Chance to make 1 lvl 9 sync and 1 lvl 9 sync:  ' + str(resultDict[8]/tries*100))
    print('Chance to make 1 lvl 8 sync and 1 lvl 12 sync: ' + str(resultDict[9]/tries*100))
    print('Chance to make 1 lvl 9 sync and 1 lvl 12 sync: ' + str(resultDict[10]/tries*100))

