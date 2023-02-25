import connectfour


def ask_columns_rows():
    #Local file
    while True:
        columns_rows = input('Please specify the number of columns and rows you want: ').strip()
        cr = columns_rows.split()
        if len(cr) == 2:
            return cr
            break
        else:
            print('Please enter the wanted number of columns and rows')
            print('in the correct format')

def creating_new_game():
    #Local and network file
    game = None
    while game == None:
        try:
            dimensions = ask_columns_rows()
            if dimensions[0].isdigit() and dimensions[1].isdigit():
                columns = int(dimensions[0])
                rows= int(dimensions[1])
                game = connectfour.new_game(columns, rows)
                return game, columns, rows
            else:
                print('Columns and rows must be integer values')
        except ValueError:
            print('Maximum column numbers is 20 and minimum is 1')
            



def moves(game: 'GameState', move_list: [str]) -> 'GameState':
    #Local and network file
    action = move_list[0]
    column = int(move_list[1])-1
        
    if action == 'pop':
        return connectfour.pop(game,column)
    if action == 'drop': 
        return connectfour.drop(game,column)
    
def check_action(move_list:[str]) -> bool:
    #local
     if move_list[0] == 'drop' or move_list[0]== 'pop':
         return True
     else:
         print('Moves must either be drop or pop')
         return False
    
def check_column(move_list:[str]) -> bool:
    #local
    if move_list[1].isdigit():
        return True
    else:
        print('Column numbers must be a digit')
        return False

def valid_move(game: 'GameState' , move_list:[str]):
    #Local and network function
    if check_column(move_list) and check_action(move_list):
        try:
            if move_list[0] == 'drop':
                x = connectfour.drop(game, int(move_list[1])-1)
                return True
            if move_list[0]== 'pop':
                y = connectfour.pop(game, int(move_list[1])-1)
                return True
                
        except ValueError:
            print('Column cannot be used.')
            return False
        except connectfour.InvalidMoveError:
            print('Move is invalid.')
            return False

def print_top(columns: int) -> None:
    #local file
    string =''
    for num in range(columns):
        if num+1 < 9:
            string= string + str(num+1) + '  '
        else:
            string = string+ str(num+1) + ' '
    print(string.strip())
        
def print_winner(game:'Gamestate'):
    #Local and Network 
    if connectfour.winner(game)==connectfour.RED:
        print('RED WINS')
    elif connectfour.winner(game)==connectfour.YELLOW:
        print('YELLOW WINS')
    else:
        pass

def print_board(game: 'GameState') -> None:
    #Local and Network file
    print_top(connectfour.columns(game))
    for index in range(connectfour.rows(game)):
        string = ''
        for row in game.board:
            if row[index]== connectfour.RED:
                string = string + 'R  '
            elif row[index]== connectfour.YELLOW:
                string = string + 'Y  '
            else:
                string = string + '.  '
        print(string.strip())


def whos_turn(game: 'GameState')-> str:
    #local
     if game.turn == connectfour.RED:
         return '[RED]'
     else:
         return '[YELLOW]'

def board_filled(game: 'GameState')-> bool:
    #local and network
    rows =connectfour.rows(game)
    columns = connectfour.columns(game)
    total_spaces= rows*columns
    n =0
    Y=0
    R=0
    for rows in game.board:
        for element in rows:
            if element == connectfour.RED or element == connectfour.YELLOW:
                n+=1

    if game.turn == connectfour.RED:
        for lists in game.board:
            last = len(lists)-1
            if lists[last] == connectfour.YELLOW:
                Y+=1
    
    if game.turn == connectfour.YELLOW:
        for lists in game.board:
            last = len(lists)-1
            if lists[last] == connectfour.RED:
                R+=1
    
        
    if n == total_spaces and (Y == columns or R == columns):
        return True
    else:
        return False
    
    
def start_sequence()-> None:
    #local and network
    print("This is a turned base game. Whose turn it is, is specified before" +
          "each prompt. A gentle reminder:" +
          " 1) Answer every prompt in ONLY lower case" +
          " 2) Valid columns are from 1 to what you specified for rows" +
          " 3) R represents RED, Y represents YELLOW, and . represents EMPTY"
          " 4) Game ends once someone connects 4 of their letters" +
          " 5) each move must be specified in the format: move followed by a space and number")

def ask_next_move(game: 'GameState')-> [str,int]:
    #Local and Network file
    while True:
        next_move = input(f'What is your next move? ').strip()
        move_list= next_move.split()
        if len(move_list) ==2:
            if check_action(move_list) and check_column(move_list):
                return move_list
                break
        else:
            print('Please enter moves in the correct format')

def start() -> None:
    #Local file
    start_sequence()
    game = creating_new_game()[0]
    print_board(game)
    while connectfour.winner(game) == connectfour.EMPTY:
        if board_filled(game) == True:
            print("It's a draw.")
            break

        who = whos_turn(game)
        print(who)
        move_list = ask_next_move(game)

        if valid_move(game, move_list):
            game= moves(game, move_list)
            print_board(game)
            

    
    if connectfour.winner(game)!= connectfour.EMPTY:
        print_winner(game)
    print('GAME OVER.')

if __name__ == '__main__':
    start()
