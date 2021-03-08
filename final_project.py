from random import shuffle
from random import randint
import json


def start_game():
    print("\t\t****** Welcome to Card Guessing Game ******")
    print("Choose Your Option:")
    print("\t\tPlay Game    -   P/p")
    print("\t\tHigh Score   -   H/h")
    print("\t\tPlay History -   N/n")
    print("\t\tExit Game    -   X/x")
    valid_selection = False
    while valid_selection is False:
        print("\t\t-->", end=' ')
        option = input()
        if option == "P" or option == "p":
            valid_selection = True
            play_game()
        elif option == "H" or option == "h":
            valid_selection = True
            high_score()
        elif option == "N" or option == "n":
            valid_selection = True
            player_history()
        elif option == "X" or option == "x":
            valid_selection = True
            print("Exiting...")
        else:
            print("Select a valid option")


def player_history():
    print("\t\t**** Player History ****")
    sco = open("scores.json")
    data = json.load(sco)
    scores = data["Scores"]
    name = input("Enter name of Player: ")
    print("Player Name - \tScores")
    print(name, end=" - \t")
    flag = False
    for x in scores:
        if name == x["Name"]:
            flag = True
            print(x["Score"], end=" ")
    if flag is False:
        print("No history found")
    sco.close()
    start_game()


def valid_choice(words, choice):
    if words > int(choice) > 0:
        return True
    return False


def play_game():
    print("Choose Level")
    print("1 - Easy")
    print("2 - Normal")
    print("3 - Hard")
    valid_selection = False
    level = ''
    while valid_selection is False:
        print("-->", end=' ')
        option = input()

        if option == "1":
            valid_selection = True
            level = 'EASY'
        elif option == "2":
            valid_selection = True
            level = 'NORMAL'
        elif option == "3":
            valid_selection = True
            level = 'HARD'
        else:
            print("Select a valid option")
    load_level(level)


def high_score():
    print("\t\t**** High Score ****")
    sco = open("scores.json")
    data = json.load(sco)
    scores = data["Scores"]
    sorted(scores, key=lambda i: i['Score'])
    count = 1
    for x in scores:
        print(x["Name"], end=" ")
        print(x["Score"])
        if count == 3:
            break
        count = count + 1
    sco.close()
    start_game()


def load_level(level):
    file = open('names.json')
    data = json.load(file)
    random = randint(0, 2)
    stage = []
    if random == 0:
        stage = data["countries"]
    elif random == 1:
        stage = data["vegetables"]
    elif random == 2:
        stage = data["animals"]
    words = 0
    if level == "EASY":
        words = 4
    elif level == "NORMAL":
        words = 6
    elif level == "HARD":
        words = 8
    current_words_1 = []
    current_words_2 = []
    for x in range(words):
        current_words_1.append(stage[x])
        current_words_2.append(stage[x])
    shuffle(current_words_2)
    revealed = []
    print(f"Welcome to {level} Mode")
    print("Player 1 Name: ", end="")
    player1name = input()
    print("Player 2 Name: ", end="")
    player2name = input()
    if player1name == player2name:
        print("Player names cannot be same")
        load_level(level)
        return
    player1score = 0
    player2score = 0
    pturnName = player1name
    pturnScore = player1score
    while len(current_words_1) != len(revealed):
        turn(pturnName, pturnScore, current_words_1, current_words_2, revealed,
             (len(current_words_1) + words - 1))
        if pturnName == player1name:
            pturnName = player2name
            pturnScore = player2score
        elif pturnName == player2name:
            pturnName = player1name
    if player1score > player2score:
        winner = player1name
        print(winner, end=" is winner")
    if player1score < player2score:
        winner = player2name
        print(winner, end=" is winner")
    if player1score == player2score:
        print("Its a Tie")
    json_file = open('scores.json')
    data = json.load(json_file)
    temp = data['Scores']
    p1 = {
        "Name": f"{player1name}",
        "Score": player1score,
    }
    p2 = {
        "Name": f"{player2name}",
        "Score": player2score,
    }
    temp.append(p1)
    temp.append(p2)
    write_score(data)


def write_score(data, filename='scores.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def IsRevealed(choice, list, revealed):
    if list[int(choice)] in revealed:
        return True
    return False


def turn(playerName, playerscore, list1, list2, revealed, limit):
    print(f"\n{playerName}'s turn")
    print("\nChoose a card")
    print_board(list1, list2, revealed)
    temp = input()
    if int(temp) < 0 or int(temp) > limit:
        print("Invalid Selection")
        turn(playerName, playerscore, list1, list2, revealed, limit)
        return
    if int(temp) < len(list1):
        if list1[int(temp)] in revealed:
            print("Card Already Revealed")
            turn(playerName, playerscore, list1, list2, revealed, limit)
            return
    else:
        if list2[int(temp) - len(list1)] in revealed:
            print("Card Already Revealed")
            turn(playerName, playerscore, list1, list2, revealed, limit)
            return
    temp_board(list1, list2, int(temp), revealed)
    print("choose other card")
    temp1 = input()
    if temp1 == temp:
        print("Card Already Revealed")
        turn(playerName, playerscore, list1, list2, revealed, limit)
    if int(temp1) < 0 or int(temp1) > limit:
        print("Invalid Selection")
        turn(playerName, playerscore, list1, list2, revealed, limit)
    if int(temp) < len(list1) and int(temp1) < len(list1):
        print("wrong")
        for x in list1:
            if x == list1[int(temp)] or x == list1[int(
                    temp1)] or x in revealed:
                print(x, end=" ")
            else:
                print(f"---{list1.index(x)}---", end=" ")
        print()
        for y in list2:
            if y in revealed:
                print(y, end=" ")
            else:
                print(f"---{len(list1) + list2.index(y)}---", end=" ")
        return
    elif int(temp) >= len(list1) and int(temp1) >= len(list1):
        print("wrong")
        for x in list1:
            if x in revealed:
                print(x, end=" ")
            else:
                print(f"---{list1.index(x)}---", end=" ")
        print()
        for y in list2:
            if y in revealed or y == list2[
                    int(temp) - len(list1)] or y == list2[int(temp1) -
                                                          len(list1)]:
                print(y, end=" ")
            else:
                print(f"---{len(list1) + list2.index(y)}---", end=" ")
        return

    if int(temp) < len(list1):
        if list1[int(temp)] == list2[int(temp1) - len(list1)]:
            print("good work")
            playerscore = playerscore + 1
            revealed.append(list1[int(temp)])
        else:
            for x in list1:
                if list1[int(temp)] == x or x in revealed:
                    print(x, end=" ")
                else:
                    print(f"---{list1.index(x)}---", end=" ")
            print()
            for y in list2:
                if list2[int(temp1) - len(list2)] == y or y in revealed:
                    print(y, end=" ")
                else:
                    print(f"---{len(list1) + list2.index(x)}---", end=" ")
            print("\nwrong")
            return
    else:
        if list2[int(temp) - len(list2)] == list1[int(temp1)]:
            print("good work")
            playerscore = playerscore + 1
            revealed.append(list1[int(temp1)])
        else:
            for x in list1:
                if list1[int(temp1)] == x or x in revealed:
                    print(x, end=" ")
                else:
                    print(f"---{list1.index(x)}---", end=" ")
            print()
            for y in list2:
                if list2[int(temp) - len(list2)] == y or y in revealed:
                    print(y, end=" ")
                else:
                    print(f"---{len(list1) + list2.index(x)}---", end=" ")
            print("\nwrong")
            return


def temp_board(list1, list2, revealed, rev):
    if revealed < len(list1):
        for x in list1:
            if x == list1[revealed] or x in rev:
                print(x, end=" ")
            else:
                print(f"---{list1.index(x)}---", end=" ")
        print()
        for x in list2:
            if x in rev:
                print(x, end=" ")
            else:
                print(f"---{len(list1) + list2.index(x)}---", end=" ")
    else:
        for x in list1:
            if x in rev:
                print(x, end=" ")
            else:
                print(f"---{list1.index(x)}---", end=" ")
        print()
        for x in list2:
            if x == list2[revealed - len(list1)] or x in rev:
                print(x, end=" ")
            else:
                print(f"---{len(list1) + list2.index(x)}---", end=" ")
    print()


def print_board(list1, list2, revealed):
    for x in list1:
        if x in revealed:
            print(x, end=" ")
        else:
            print(f'---{list1.index(x)}---', end=" ")
    print()
    for x in list2:
        if x in revealed:
            print(x, end=" ")
        else:
            print(f'---{len(list1) + list2.index(x)}---', end=" ")
    print()


start_game()
