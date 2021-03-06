import Combo

def create_combo(combo_name):
    c = Combo.Combo(combo_name)
    c.save()
    edit_combo(c)

def save_combo(c, parts):
    c.name         = parts[0]
    c.hand         = parts[1]
    c.hand_or_deck = parts[2]
    c.deck         = parts[3]
    c.extra        = parts[4]
    c.grave        = parts[5]
    c.subcombos    = parts[6]
    c.folder       = parts[7]
    c.save()

def edit_combo(c):
    states =  ['name', 'hand', 'hand_or_deck', 'deck', 'extra', 'grave', 'subcombos', 'folder', 'none', 'done']
    actions = ['add', 'remove', 'print', 'none', 'done']
    action = 'none'
    repeat = 0
    parts = [c.name, c.hand, c.hand_or_deck, c.deck, c.extra, c.grave, c.subcombos, c.folder]

    save_combo(c, parts)
    c.print_combo()
    state = raw_input("What part of the combo do you want to work on?\n")

    while state != 'done':

        while state not in states:
            print('Error {} is not a valid part of the combo'.format(state))
            print('hand, hand_or_deck, deck, extra, subcombos, and folder are the valid parts of the combo')
            state = raw_input("What part of the combo do you want to work on?\n")

        if state in states[1:7]:
            part = parts[states.index(state)]
        elif state == 'folder':
            parts[states.index(state)] = raw_input("What would you like to change the combo folder to?\n")
            c.delete_combo()
            save_combo(c, parts)
        elif state == 'name':
            print('Name is: {}'.format(c.name))
            c.delete_combo()
            parts[states.index(state)] = raw_input("What would you like to change it to?\n")
            save_combo(c, parts)

        while action != 'done':

            if state == 'done' or state == 'folder' or state == 'name':
                action = 'done'

            if action == 'none':
                action = raw_input("Would you like to add or remove cards from the {} combo requirement?\n".format(state))

            if action == 'print':
                save_combo(c, parts)
                c.print_combo()
                action = 'none'

            while action == 'add':
                if not repeat:
                    card = raw_input("What card would you like to add?\n")

                if card in actions:
                    action = card
                    break

                if state == 'subcombos':
                    if card in part:
                        print("{} is already a subcombo of this combo".format(card))
                        repeat = 0
                    else:
                        part.append(card)
                        repeat = 0
                else:
                    if card in part:
                        print('There are currently {} copies of {} already in the combo'.format(part[card], card))

                    num = int(raw_input("How many copies of {} do you want to add?\n".format(card)))

                    if num > 3:
                        print('You can only have 3 copies of a card in your combo')
                        repeat = 1
                    elif card in part.keys():
                        if (part[card] + num) > 3:
                            print('You can only have 3 copies of a card in your combo')
                            repeat = 1
                        else:
                            repeat = 0
                            c.add_card(part, card, num)
                            print 'Added ' + card
                            save_combo(c, parts)
                    else:
                        repeat = 0
                        c.add_card(part, card, num)
                        print 'Added ' + card
                        save_combo(c, parts)

            while action == 'remove':
                if not repeat:
                    card = raw_input("What card would you like to remove?\n")

                if card in actions:
                    action = card
                    break

                if state == 'subcombos':
                    if card not in part:
                        print("{} is not a subcombo of this combo".format(card))
                        repeat = 0
                    else:
                        part.remove(card)
                        repeat = 0
                elif card in part.keys():
                    print('There are {} copies of {}'.format(part[card], card))

                    num = int(raw_input("How many copies of {} do you want to remove?\n".format(card)))
                    if num > part[card]:
                        print('Error, you are trying to remove more copies than exist')
                        repeat = 1
                    else:
                        repeat = 0
                        c.remove_card(part, card, num)
                        save_combo(c, parts)
                else:
                    print('{} is not in the {} combo'.format(card, state))

            if action not in actions:
                print('Error: invalid action entered: {}'.format(action))
                print('Valid actions are:')
                action = 'none'
                for element in actions:
                    print element

        action = 'none'
        state = raw_input("What part of the combo do you want to work on?\n")

    save_combo(c, parts)
