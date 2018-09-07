import Deck

def create_deck():
    deck_name = raw_input("What is the name of the deck?\n")
    d = Deck.Deck(deck_name)
    d.save()
    edit_deck(d)

def save_deck(d, parts):
    d.main_deck = parts[0]
    d.side_deck = parts[1]
    d.extra_deck = parts[2]
    d.deck_name = parts[3]
    d.combo_folder = parts[4]
    d.save()

def edit_deck(d):
    states =  ['main', 'side', 'extra', 'name', 'combo', 'none', 'done']
    actions = ['add', 'remove', 'print', 'none', 'done']
    action = 'none'
    repeat = 0
    parts = [d.main_deck, d.side_deck, d.extra_deck, d.deck_name, d.combo_folder]

    d.print_deck()
    state = raw_input("What part of the deck do you want to work on?\n")

    while state != 'done':

        while state not in states:
            print 'Error ' + state + ' is not a valid part of the deck'
            print 'main, side, and extra are the valid parts of the deck'
            state = raw_input("What part of the deck do you want to work on?\n")

        if state in states[0:3]:
            part = parts[states.index(state)]
        elif state == 'combo':
            parts[4]  = raw_input("What would you like to change the combo folder to?\n")
            save_deck(d, parts)
        elif state == 'name':
            print 'Name is: ' + d.deck_name
            d.delete_deck()
            parts[3] = raw_input("What would you like to change it to?\n")
            save_deck(d, parts)

        while action != 'done':

            if state == 'done' or state == 'combo' or state == 'name':
                action = 'done'

            if action == 'none':
                action = raw_input("Would you like to add or remove cards from the " + state + " deck?\n")

            if action == 'print':
                save_deck(d, parts)
                d.print_deck()
                action = 'none'

            while action == 'add':
                if not repeat:
                    card = raw_input("What card would you like to add?\n")

                if card in actions:
                    action = card
                    break

                if card in part:
                    print 'There are currently ' + str(part[card]) + ' copies of ' + card + ' already in the deck'

                num = int(raw_input("How many copies of " + card + " do you want to add?\n"))

                if num > 3:
                    print 'You can only have 3 copies of a card in your deck'
                    repeat = 1
                elif card in part.keys():
                    if (part[card] + num) > 3:
                        print 'You can only have 3 copies of a card in your deck'
                        repeat = 1
                    else:
                        repeat = 0
                        d.add_card(part, card, num)
                        print 'Added ' + card
                        save_deck(d, parts)
                else:
                    repeat = 0
                    d.add_card(part, card, num)
                    print 'Added ' + card
                    save_deck(d, parts)

            while action == 'remove':
                if not repeat:
                    card = raw_input("What card would you like to remove?\n")

                if card in actions:
                    action = card
                    break

                if card in part.keys():
                    print 'There are ' + str(part[card]) + ' copies of ' + card

                    num = int(raw_input("How many copies of " + card + " do you want to remove?\n"))
                    if num > part[card]:
                        print 'Error, you are trying to remove more copies than exist'
                        repeat = 1
                    else:
                        repeat = 0
                        d.remove_card(part, card, num)
                        save_deck(d, parts)
                else:
                    print card + ' is not in the ' + state + ' deck'

            if action not in actions:
                print 'Error: invalid action entered: ' + action
                print 'Valid actions are:'
                action = 'none'
                for element in actions:
                    print element

        action = 'none'
        state = raw_input("What part of the deck do you want to work on?\n")

    save_deck(d, parts)
