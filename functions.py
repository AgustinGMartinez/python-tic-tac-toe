import blueprint
import state
# modules
import msvcrt
import os

current_turn = state.current_turn
wins = state.wins
current_marks = state.current_marks
current_pointer_position = state.current_pointer_position

def clear_console(): return os.system('cls')


def draw_dashbord():
    global wins, current_turn
    print("\n", flush=True)
    print(blueprint.turn_print.format(current_turn), flush=True)
    print("\n", flush=True)
    print("Use the letters awsd to move the pointer, spacebar to submit", flush=True)
    dashboard = get_formatted_dashboard()
    for c in dashboard.splitlines():
        print(c, flush=True)
    print("\n", flush=True)
    print(blueprint.winners_state.format(wins["one"], wins["two"]), flush=True)
    print("\n", flush=True)


def get_formatted_dashboard():
    global current_turn
    dashboard = blueprint.dashboard_print
    m = transform_matrix_to_array()
    current_pointer_index_x = get_pointer_position_in_matrix("x")
    current_pointer_index_y = get_pointer_position_in_matrix("y")

    current_pointer_index = current_pointer_index_x * 3 + current_pointer_index_y

    m[current_pointer_index] = "X" if current_turn == 1 else "0"

    for index, item in enumerate(m):
        if item == 1:
            m[index] = "x"
        elif item == 2:
            m[index] = "0"
        elif item == 0:
            m[index] = " "

    return dashboard.format(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8])


def get_pointer_position_in_matrix(axis=None):
    position = str(current_pointer_position)
    if axis is None:
        return [int(position[0]) - 1, int(position[1]) - 1]
    elif axis == "x":
        return int(position[0]) - 1
    elif axis == "y":
        return int(position[1]) - 1
    else:
        raise ValueError('Invalid matrix position requested.')


def transform_matrix_to_array():
    global current_marks
    return current_marks[0] + current_marks[1] + current_marks[2]


def submit_move():
    x = get_pointer_position_in_matrix("x")
    y = get_pointer_position_in_matrix("y")

    if current_marks[x][y] != 0:
        return
    current_marks[x][y] = (1 if current_turn == 1 else 2)


def change_turn():
    global current_turn
    if current_turn == 1:
        current_turn = 2
    else:
        current_turn = 1


def handle_move():
    global current_pointer_position

    move = msvcrt.getch().decode("utf-8")

    if move in "asdwp ":
        if move == "a":
            if current_pointer_position % 10 == 1:
                return
            else:
                current_pointer_position -= 1
        elif move == "d":
            if current_pointer_position % 10 == 3:
                return
            else:
                current_pointer_position += 1
        elif move == "w":
            if current_pointer_position < 20:
                return
            else:
                current_pointer_position -= 10
        elif move == "s":
            if current_pointer_position > 29:
                return
            else:
                current_pointer_position += 10
        elif move == "p":
            print("Stop!")
            exit(0)
        elif move == " ":
            submit_move()
            change_turn()

def reset_game():
    global current_marks
    global current_turn
    global current_pointer_position

    current_marks = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    current_turn = 1
    current_pointer_position = 11

def end_game(hasWinner, player = None):
    global wins
    if hasWinner:
        player_str = "one" if player == 1 else "two"
        wins[player_str] = wins[player_str] + 1
        print("Player {} wins!!!!!!!!!!".format(player))
        print("Press spacebar to play again, anything else to exit")
        key = msvcrt.getch().decode("utf-8")
        if key == " ":
            reset_game()
        else:
            exit(0)
    else:
        print("That's a draw :/")
        print("Press spacebar to play again, anything else to exit")
        key = msvcrt.getch().decode("utf-8")
        if key == " ":
            reset_game()
        else:
            exit(0)


def check_winner():
    global end_game
    one_positions = []
    two_positions = []
    win_conditions = [[1,2,3],[1,4,7],[7,8,9],[3,6,9],[1,5,9],[3,5,7],[2,5,8],[4,5,6]]

    for index, value in enumerate(transform_matrix_to_array()):
        if value == 1:
            one_positions.append(index + 1)
        elif value == 2:
            two_positions.append(index + 1)


    for player in range(1, 3):
        p = one_positions if player == 1 else two_positions
        for condition in win_conditions:       
            asserts = 0
            for value in condition:
                if value in p:
                    asserts += 1
            if asserts == 3:
                end_game(True, player)
                
    # check for draw
    if len(one_positions) + len(two_positions) >= 9:
        end_game(False)