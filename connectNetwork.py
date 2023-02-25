import connectfourShell
import connectfour
from collections import namedtuple
import socket

SomeConnection = namedtuple('SomeConnection', ['socket', 'input', 'output'])

class ProtocolError(Exception):
    pass

def ask_username() -> str:
    #network file
    while True:
        username = input('please specify your username: ')
        if ' ' in username:
            print('Please enter a username that does NOT contain spaces')
        else:
            return username
            break

def connect() -> SomeConnection:
    #connection file
    while True:
        host = input('Specify host you would like to connect to: ').strip()
        port = input('Specify the port you would like to connnect to: ').strip()
        if port.isdigit():
            port= int(port)
            try:
                some_socket = socket.socket()
                some_socket.connect((host, port))
                some_input = some_socket.makefile('r')
                some_output = some_socket.makefile('w')
                return SomeConnection(socket = some_socket,
                                      input = some_input,
                                      output= some_output)
                break
            except socket.gaierror:
                print('This is not a valid server, please re-enter a server and port.')
            except ConnectionRefusedError:
                print('Connection refused, please try another server and port')
            except OSError:
                print('There is no route to this host, try another server and port')
            except OverflowError:
                print('Invalid port. Port must be 0-65535')

        else:
            print('Port must be an integer value')


def read_line(connection: SomeConnection) -> str:
    #connection file
    line = connection.input.readline()[:-1]
    return line

def write_line(connection: SomeConnection, line:str) -> str:
    #connection file
    connection.output.write(line + '\r\n')
    connection.output.flush()

   
def hello_protocol(connection: SomeConnection, username: str) -> bool:
    #connection file
    write_line(connection, f'I32CFSP_HELLO {username}')
    line = read_line(connection)
    if line == f'WELCOME {username}':
        return True
    else:
        raise ProtocolError
               
def disconnect(connection: SomeConnection) -> None:
    #Connection file
    connection.input.close()
    connection.output.close()
    connection.socket.close()


def send_player_move(connection: SomeConnection, action: str, column: str):
    #connection file
    action = action.upper()
    write_line(connection, f'{action} {column}')

def player_move(game: 'GameState', connection: SomeConnection,username:str):
    #network file
    while True:
        print(f'[{username}]')
        move = connectfourShell.ask_next_move(game)
        action = move[0]
        column = move[1]
        if connectfourShell.valid_move(game, [action, column]):
            game= connectfourShell.moves(game,move)
            send_player_move(connection, action, column)
            return game
        
    
def read_move(connection: SomeConnection):
    #connection file
    move = None
    for times in range(3):
        line = read_line(connection)
        if 'DROP' in line or  'POP' in line:
            move = line.split()
            break
    if move!= None:
        return move
    else:
        raise ProtocolError
        

def ai_move(game: 'GameState', connection: SomeConnection):
    #Network file
    move = read_move(connection)
    move[0] = move[0].lower()
    if connectfourShell.valid_move(game, move):
        game = connectfourShell.moves(game, move)
        print(f'[Ai {move[0]}ped {move[1]}]')
        return game
    else:
        print('The ai has made a invalid move. You will be disconnected')
        raise ProtocolError

def start_game(game: 'GameState', connection: SomeConnection, username:str):
    #Network file
    connectfourShell.print_board(game)
    x= None
    while connectfour.winner(game) == connectfour.EMPTY:
        try:
        
            game = player_move(game,connection,username)
            connectfourShell.print_board(game)

            if connectfourShell.board_filled(game)== True:
                print("It's a draw.")
                break
        
            game= ai_move(game,connection)
            connectfourShell.print_board(game)

            if connectfourShell.board_filled(game)== True:
                print("It's a draw.")
                break

        except ProtocolError:
            disconnect(connection)
            x= 'disconnected'
            break

    if connectfour.winner(game)!= connectfour.EMPTY:
        connectfourShell.print_winner(game)
    if x != 'disconnected':
        disconnect(connection)

def create_game():
    #network file
    connection= connect()
    username = ask_username()
    try:
        if hello_protocol(connection, username):
            connectfourShell.start_sequence()
            game,columns,rows = connectfourShell.creating_new_game()
            write_line(connection, f'AI_GAME {columns} {rows}')
            start_game(game, connection, username)
    except ProtocolError:
        print('This server is not the connectfour server. You will now be disconnected.')
        disconnect(connection)



if __name__ == '__main__':
    create_game()
