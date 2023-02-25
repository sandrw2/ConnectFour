#Sandra Wang 14772372
import connectfour

def _ask_columns_rows():
    '''
    Asks the player what number or rows and columns they want the game to be and then
    returns their input as a list [columns, rows]
    '''
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
            
def creating_new_game()-> ('GameState', 'columns', 'rows'):
    '''
    Creates a new game using the columns and rows the user specified
    If the user inputed values that are not integers they will be prompted to do so again
    If the user inputs values that is less than 1 or greater than 20, they will be prompted to
    input values in the range of 1-20
    '''
    #Local and network file
    game = None
    while game == None:
        try:
            dimensions = _ask_columns_rows()
            if dimensions[0].isdigit() and dimensions[1].isdigit():
                columns = int(dimensions[0])
                rows= int(dimensions[1])
                game = connectfour.new_game(columns, rows)
                return game, columns, rows
            else:
                print('Columns and rows must be integer values')
        except ValueError:
            print('Maximum column numbers is 20 and minimum is 1')
            

def _check_action(move_list:[str]) -> bool:
    '''
    Checks if actions provided by the user exists
    Moves must be pop or drop to return true, otherwise
    this function returns false
    '''
    #local
    action = move_list[0].lower()
    if action == 'drop' or action== 'pop':
        return True
    else:
        print('Moves must either be drop or pop')
        return False
    
def _check_column(move_list:[str]) -> bool:
    #local
    '''
    Checks if the column number the player wants to act on is a digit.
    If it is, function returns true
    otherwise, returns false
    '''
    num = move_list[1]
    if num.isdigit():
        return True
    else:
        print('Column numbers must be a digit')
        return False
   
def valid_move(game: 'GameState' , move_list:[str])-> bool:
    '''
    uses _check_column and _check_action
    to check if player inputted a valid move [action column]
    Then it further tests if the move is valid by trying to use the values
    in the drop or pop function. If a valueError exception or InvalidMoveError
    occurs the function will return false. If the function doesn't even pass
    _check_column and _check_action, it will also return false
    '''
    #Local and network function
    if _check_column(move_list) and _check_action(move_list):
        try:
            action = move_list[0].lower()
            if action == 'drop':
                x = connectfour.drop(game, int(move_list[1])-1)
                return True
            if action == 'pop':
                y = connectfour.pop(game, int(move_list[1])-1)
                return True
                
        except ValueError:
            print('Column cannot be used.')
            return False
        except connectfour.InvalidMoveError:
            print('Move is invalid.')
            return False

def moves(game: 'GameState', move_list: [str]) -> 'GameState':
    '''
    performs specified move on GameState 
    '''
    #Local and network file
    action = move_list[0].lower()
    column = int(move_list[1])-1
        
    if action == 'pop':
        return connectfour.pop(game,column)
    if action == 'drop': 
        return connectfour.drop(game,column)


def print_winner(game:'Gamestate') -> None:
    '''
    prints winner of the game
    '''
    #Local and Network 
    if connectfour.winner(game)==connectfour.RED:
        print('RED WINS')
    elif connectfour.winner(game)==connectfour.YELLOW:
        print('YELLOW WINS')
    else:
        pass

def _print_top(columns: int) -> None:
    '''
    Prints top lables of the gameboard
    '''
    #local file
    string =''
    for num in range(columns):
        if num+1 < 9:
            string= string + str(num+1) + '  '
        else:
            string = string+ str(num+1) + ' '
    print(string.strip())

def print_board(game: 'GameState') -> None:
    '''
    Given the GameState, functions prints current game board
    '''
    #Local and Network file
    _print_top(connectfour.columns(game))
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

def board_filled(game: 'GameState')-> bool:
    '''
    Function identifies stalemates where no one is the winner
    If the board is filled and the person whose turn it is can not pop,
    function returns true. 
    '''
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
    '''
     Prints breif rules of the game
    '''
    #local and network
    print("This is a turned base game. Whose turn it is, is specified before each prompt." )
    print(" A gentle reminder: \n " )
    print(" 1) You will be prompted to specify the columns and rows of the connectfour game" )
    print(" 2) The columns and rows must not exceed 20 or be below 1")
    print(" 3) Follow the format: COLUMNS[space]ROWS")
    print(" 4) Each turn you will be prompted to specify a move. You can either pop or drop")
    print(" 5) You can choose a column only within the range of 1 to the number of columns in the game)")
    print(" 6) Each move should follow the format MOVE[space]COLUMN" )
    print(" 7) R stands for RED and Y stands for YELLOW")

def ask_next_move(game: 'GameState')-> [str,int]:
    '''
    asks player their next move
    if player does not specify their move in the correct format
    it prompts them to do so again
    '''
    #Local and Network file
    while True:
        next_move = input(f'What is your next move? ').strip()
        move_list= next_move.split()
        if len(move_list) ==2:
            if _check_action(move_list) and _check_column(move_list):
                return move_list
                break
        else:
            print('Please enter moves in the correct format')


