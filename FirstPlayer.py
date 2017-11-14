import math
import copy
from random import randint

NUMBER_OF_EACH = 40

blank_boxes_first_player = {}
blank_boxes_second_player = {}

boxes_first_player = {}
boxes_second_player = {}

def setup():
    position = ( ( ' ', ' ', ' ' ), ( ' ', ' ', ' ' ), ( ' ', ' ', ' ' ) )
    #for item in make_list_of_all_boxes_from_here(position, [ position ]):
        #print item
    for item in make_list_of_all_boxes_from_here(position, [ position ]):
        blank_boxes_first_player[item] = copy.deepcopy(list_of_marbles(item))
        blank_boxes_second_player[item] = copy.deepcopy(list_of_marbles(item))

        boxes_first_player[item] = list_of_marbles(item)
        boxes_second_player[item] = list_of_marbles(item)
    #for item in list(boxes_first_player.values()):
        #print item

def make_list_of_all_boxes_from_here(position, so_far):
    if len(so_far)%100000 == 0:
        print len(so_far)
    if there_are_three_in_a_row(position):
        return so_far
    if first_players_turn(position):
        for i in range(0, 9):
            if position[int(math.floor(i/3))][i%3] == ' ':
                new_position = create_changed_position(position, i, 'x')
                so_far += [ new_position ]
                so_far = make_list_of_all_boxes_from_here(new_position, so_far)
    else:
        for i in range(0, 9):
            if position[int(math.floor(i/3))][i%3] == ' ':
                new_position = create_changed_position(position, i, 'o')
                so_far += [ new_position ]
                so_far = make_list_of_all_boxes_from_here(new_position, so_far)
    return so_far

def first_players_turn(position):
    x_s = 0
    o_s = 0
    for i in range(0, 9):
        if position[int(math.floor(i/3))][i%3] == 'x':
            x_s += 1
        if position[int(math.floor(i/3))][i%3] == 'o':
            o_s += 1
    return x_s <= o_s

def list_of_marbles(position):
    result = [ [ 0, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ] ]
    for i in range(0, 9):
        if position[int(math.floor(i/3))][i%3] == ' ':
            result[int(math.floor(i/3))][i%3] = NUMBER_OF_EACH
    return result

def create_changed_position(position, i, char):
    tmp_list = [list(position[0]), list(position[1]), list(position[2])]
    tmp_list[int(math.floor(i/3))][i%3] = char
    return (tuple(tmp_list[0]), tuple(tmp_list[1]), tuple(tmp_list[2]))

def take_turn_first_player(position):
    if board_is_full(position):
        #print_position(position)
        return ('draw', position)
    if all_0s(boxes_first_player[position]):
        #print_position(position)
        return ('o_give_up', position)
    i = randint(0, 8)
    while boxes_first_player[position][int(math.floor(i/3))][i%3] == 0:
        i = randint(0, 8)
    if there_are_three_in_a_row(create_changed_position(position, i, 'x')):
        #print_position(create_changed_position(position, i, 'x'))
        return ('x', position)
    result_of_game = take_turn_second_player(create_changed_position(position, i, 'x'))
    if result_of_game[0][:1] == 'x':
        boxes_first_player[position][int(math.floor(i/3))][i%3] += 2
    elif result_of_game[0][:1] == 'o':
        boxes_first_player[position][int(math.floor(i/3))][i%3] -= 1
    return result_of_game

def take_turn_second_player(position):
    if board_is_full(position):
        #print_position(position)
        return ('draw', position)
    if all_0s(boxes_second_player[position]):
        #print_position(position)
        return ('x_give_up', position)
    i = randint(0, 8)
    while boxes_second_player[position][int(math.floor(i/3))][i%3] == 0:
        i = randint(0, 8)
    if there_are_three_in_a_row(create_changed_position(position, i, 'o')):
        #print_position(create_changed_position(position, i, 'o'))
        return ('o', position)
    result_of_game = take_turn_first_player(create_changed_position(position, i, 'o'))
    if result_of_game[0][:1] == 'o':
        boxes_second_player[position][int(math.floor(i/3))][i%3] += 2
    elif result_of_game[0][:1] == 'x':
        boxes_second_player[position][int(math.floor(i/3))][i%3] -= 1
    return result_of_game

def all_0s(list_of_lists):
    for i in range(0, 3):
        for j in range(0, 3):
            if list_of_lists[i][j] != 0:
                return False
    return True

def there_are_three_in_a_row(position):
    for i in range(0, 3):
        if position[i][0] == position[i][1] and position[i][1] == position[i][2] and position[i][0] != ' ':
            return True
        if position[0][i] == position[1][i] and position[1][i] == position[2][i] and position[0][i] != ' ':
            return True
    if position[0][0] == position[1][1] and position[1][1] == position[2][2] and position[0][0] != ' ':
        return True
    if position[0][2] == position[1][1] and position[1][1] == position[2][0] and position[0][2] != ' ':
        return True
    return False

def board_is_full(position):
    for i in range(0, 3):
        for j in range(0, 3):
            if position[i][j] == ' ':
                return False
    return True

def print_position(position):
    for item in position:
        print item

setup()

print "ALL BOXES HAVE BEEN POPULATED"

last_result = ('', ((' ', ' ', ' '), (' ', 'x', ' '), (' ', ' ', ' ')) )
#for j in range(0, 100):
j = 0
while last_result[1] == ((' ', ' ', ' '), (' ', 'x', ' '), (' ', ' ', ' ')):
    boxes_first_player = copy.deepcopy(blank_boxes_first_player)
    boxes_second_player = copy.deepcopy(blank_boxes_second_player)
    i = 0
    last_result = ('', ((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' ')) )
    while last_result[0][1:] != '_give_up':
        last_result = take_turn_first_player( ((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' ')) )
        #print "Game nr. " + `i`
        #print_position(last_result[1])
        #print last_result[0]
        i += 1
    print "Game nr. " + `i`
    #print_position(last_result[1])
    #print last_result[0]
    j += 1
    if j >= 1000:
        break
print "Run through nr. " + `j`
print_position(last_result[1])
print last_result[0]

#print "STARTING THE GAMES"

#for i in range(0, 100):
    #print "Game nr. " + `i`
    #print take_turn_first_player( ((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' ')) )

