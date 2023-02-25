#Sandra Wang 14772372
import connectfour
import connectfour_connection
import connectfour_shared


def ask_username() -> str:
    '''
    Asks player for username
    If username contains a space, it prompts them to do it again
    '''
    #network file
    while True:
        username = input('please specify your username: ')
        if ' ' in username:
            print('Please enter a username that does NOT contain spaces')
        else:
            return username
            break

def player_move(game: 'GameState', connection: 'SomeConnection',username:str) -> 'GameState':
    '''
    Asks player for their next move and checks if the move is valid before
    sending the move to server
    '''
    #network file
    while True:
        print(f'[{username}]')
        move = connectfour_shared.ask_next_move(game)
        action = move[0].lower()
        column = move[1]
        if connectfour_shared.valid_move(game, [action, column]):
            game= connectfour_shared.moves(game,move)
            connectfour_connection.send_player_move(connection, action, column)
            return game


def ai_move(game: 'GameState', connection: 'SomeConnection') -> 'GameState':
    '''
    reads the move from the server then checks if the move is valid
    if move is invalid a ProtocolError is raised and client will be disconnected
    '''
    #Network file
    move = connectfour_connection.read_move(connection)
    move[0] = move[0].lower()
    if connectfour_shared.valid_move(game, move):
        game = connectfour_shared.moves(game, move)
        print(f'[Ai {move[0]}ped {move[1]}]')
        return game
    else:
        print('The ai has made a invalid move. You will be disconnected')
        raise connectfour_connection.ProtocolError


def start_game(game: 'GameState', connection: 'SomeConnection', username:str) -> None:
    '''
    Has player make their move
    prints out the game
    Returns the move of the server and prints out the board game
    Continies to do so until someone wins or there is a stalemate
    Then prints winner if there is one
    Finally, client is disconnected and program ends
    '''
    #Network file
    connectfour_shared.print_board(game)
    x= None
    while connectfour.winner(game) == connectfour.EMPTY:
        try:
        
            game = player_move(game,connection,username)
            connectfour_shared.print_board(game)

            if connectfour_shared.board_filled(game)== True:
                print("It's a draw.")
                break
        
            game= ai_move(game,connection)
            connectfour_shared.print_board(game)

            if connectfour_shared.board_filled(game)== True:
                print("It's a draw.")
                break

        except connectfour_connection.ProtocolError:
            connectfour_connection.disconnect(connection)
            x = 'disconnected'
            break
    if connectfour.winner(game)!= connectfour.EMPTY:
        connectfour_shared.print_winner(game)

    if x != 'disconnected':
        connectfour_connection.disconnect(connection)


def create_game()-> None:
    '''
    Creates a new game between client and server after establishing a connection between
    the two
    If server does not follow protocols it will disconnect and end the program
    '''
    #network file
    try:
        connection= connectfour_connection.connect()
        username = ask_username()
        if connectfour_connection.hello_protocol(connection, username):
            connectfour_shared.start_sequence()
            print('RED is you and YELLOW is the AI')
            game,columns,rows = connectfour_shared.creating_new_game()
            connectfour_connection.prompt_server_start(connection, columns, rows)
            start_game(game, connection, username)

    except connectfour_connection.ProtocolError:
        print('This server is not the connectfour server. You will now be disconnected.')
        connectfour_connection.disconnect(connection)

                
if __name__ == '__main__':
    create_game()
