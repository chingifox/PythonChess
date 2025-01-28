board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', ' '],
        ['p', 'p', 'p', 'p', 'p', ' ', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', ' ', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', ' ', ' ', 'R']
    ]
move_count = 0

def print_board():
    for i in range(8):
        print(f"{8-i}{board[i]}")
    print("   a    b    c    d    e    f    g    h")

def translate(position:str, destination:str):
    global initial_file, final_file, initial_rank, final_rank
    file_map = {
        'a' : 0,
        'b' : 1,
        'c' : 2,
        'd' : 3,
        'e' : 4,
        'f' : 5,    
        'g' : 6,
        'h' : 7
    }

    initial_file  = file_map[position[0]]
    final_file = file_map[destination[0]]

    initial_rank = 8 - int(position[1])
    final_rank = 8 - int(destination[1])

def current_player():
    if move_count % 2 == 0:
        return 'White'
    else: 
        return 'Black'

def valid_turn(rank, file):
    pce = board[rank][file]
    if (pce.islower() and current_player() == 'Black') or (pce.isupper() and current_player() == 'White'):
        return True
    else:
        return False 
    
def is_check():
    king_position = None
    for r in range(8):
        for f in range(8):
            p = board[r][f]
            if current_player() == 'White':
                if p == 'K':
                    king_position = (r,f)
                    break
            else:
                if p == 'k':
                    king_position = (r,f)
                    break
    opponent = 'Black' if current_player() == 'White' else 'White'
    for rank in range(8):
        for file in range(8):
            p1 = board[rank][file]
            if (p1.islower() and opponent == 'Black') or (p1.isupper() and opponent == 'White'):
                if p1.lower() != 'k' and valid_move(rank, file, king_position[0], king_position[1]):
                    return True
    return False
  
def valid_move(position_rank, position_file, destination_rank, destination_file):
    piece = board[position_rank][position_file]
    destination = board[destination_rank][destination_file]
            
    
    def destination_is_enemy():
        if (piece.isupper() and destination.islower()) or (piece.islower() and destination.isupper()):
            return True
        return False
    
    def castle():
        if piece == 'K'  and (position_rank == destination_rank) and (abs(position_file - destination_file) == 2) and not is_check():
            if destination_file == 6 and destination == ' ' and board[7][5] == ' ' and board[7][7] == 'R':
                print("Checkpoint 1")
                board[7][4] = ' '
                board[7][5] = 'K'
                print_board()
                if is_check():
                    print("Checkpoint 2")
                    board[7][4] = 'K'
                    board[7][5] = ' '
                    return False 
                else:
                    board[7][5] = 'R'
                    board[7][7] = ' '

                return True 
            else:
                return False
            
    if piece.lower() == 'p':
        if piece.isupper():
            if position_file == destination_file and destination == ' ':
                if (position_rank == 6) and (position_rank - destination_rank <= 2) and (board[position_rank - 1][position_file] == ' '):
                    return True 
                elif position_rank - destination_rank == 1:
                    return True      
            elif abs(position_file - destination_file) == 1 and (position_rank - destination_rank) == 1 and destination.islower():
                return True 
        
        elif piece.islower():
            if position_file == destination_file and destination == ' ':
                if (position_rank == 1) and (destination_rank - position_rank <= 2) and (board[position_rank + 1][position_file] == ' '):
                    return True 
                elif destination_rank - position_rank == 1:
                    return True      
            elif abs(position_file - destination_file) == 1 and (destination_rank - position_rank) == 1 and destination.isupper():
                return True 
        
    elif piece.lower() == 'n': 
        if abs(position_file-destination_file) == 1 and (destination == ' ' or destination_is_enemy()) and abs(position_rank - destination_rank) == 2:
            return True
        elif abs(position_file-destination_file) == 2 and (destination == ' ' or destination_is_enemy()) and abs(position_rank - destination_rank) == 1:
            return True

    elif piece.lower() == 'b':
        if (abs(position_rank - destination_rank) == abs(position_file - destination_file)) and (destination == ' ' or destination_is_enemy()):
            r_step = -1 if position_rank > destination_rank else 1
            c_step = -1 if position_file > destination_file else 1
            r, c = position_rank + r_step, position_file + c_step
            while r != destination_rank:
                if board[r][c] != ' ':
                    return False
                r += r_step
                c += c_step
            return True
        return False 
        
    elif piece.lower() == 'r':
        if (position_rank == destination_rank or position_file == destination_file) and (destination == ' ' or destination_is_enemy()):
            if position_rank == destination_rank:
                for f in range(min(position_file, destination_file) + 1, max(position_file, destination_file)):
                    if board[position_rank][f] != ' ':
                        return False
            elif position_file == destination_file:
                for r in range(min(position_rank, destination_rank) + 1, max(position_rank, destination_rank)):
                    print(r)
                    if board[r][destination_file] != ' ':
                        return False
            return True 
                    
    elif piece.lower() == 'q':
        if abs(position_rank - destination_rank) == abs(position_file - destination_file) and (destination == ' ' or destination_is_enemy()):
            r_step = -1 if position_rank > destination_rank else 1
            c_step = -1 if position_file > destination_file else 1
            r, c = position_rank + r_step, position_file + c_step
            while r != destination_rank:
                if board[r][c] != ' ':
                    return False
                while c < 7: 
                    r += r_step
                    c += c_step
            return True
        
        elif (position_rank == destination_rank or position_file == destination_file) and (destination == ' ' or destination_is_enemy()):
            if position_rank == destination_rank:
                for f in range(min(position_file, destination_file) + 1, max(position_file, destination_file)):
                    if board[position_rank][f] != ' ':
                        return False
            elif position_file == destination_file:
                for r in range(min(position_rank, destination_rank) + 1, max(position_rank, destination_rank)):
                    if board[r][position_file] != ' ':
                        return False
            return True 
        return False 
    
    elif piece.lower() == 'k':
        if abs(position_rank - destination_rank) <= 1 and abs(position_file - destination_file) <= 1 and (destination == ' ' or destination_is_enemy()): 
            return True 
        elif castle():
            return True
        return False 
                

def move():
    global move_count
    temp_piece = board[final_rank][final_file]
    board[final_rank][final_file] = board[initial_rank][initial_file]
    board[initial_rank][initial_file] = ' '
    
    if is_check():
        board[initial_rank][initial_file] = board[final_rank][final_file]
        board[final_rank][final_file] = temp_piece
        print("Invalid move! King is in check.")

    else:
        move_count += 1 
    

while True:
    print_board()
    print(f'{current_player()} to move')
    print(is_check()) 
    position = input("From: ")
    destination = input("To: ")
    translate(position, destination)
    if valid_turn(initial_rank, initial_file) and valid_move(initial_rank, initial_file, final_rank, final_file):
        move()
        print(is_check())
    else:
        print("Invalid move! \n")


