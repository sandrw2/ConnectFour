#Sandra Wang 14772372
import socket
from collections import namedtuple

SomeConnection = namedtuple('SomeConnection', ['socket', 'input', 'output'])


class ProtocolError(Exception):
    pass

def connect() -> SomeConnection:
    '''
    Establishes connection between specified host and port
    If specified server is not valid
    or port number is not integer value
    or port does not lie between 1-65535
    or connection is refused
    or there is no route to host
    then, the user will be re-prompted
    '''
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


def _read_line(connection: SomeConnection) -> str:
    '''
    reads line sent from server
    '''
    
    #connection file
    line = connection.input.readline()[:-1]
    return line

def _write_line(connection: SomeConnection, line:str) -> str:
    '''
    writes lines to server
    '''
    #connection file
    connection.output.write(line + '\r\n')
    connection.output.flush()

def prompt_server_start(connection: SomeConnection, columns: int, rows: int) -> None:
    '''
    Prompts the server to start connectfour game and tells them the number
    of columns and rows the client wants
    '''
    _write_line(connection, f'AI_GAME {columns} {rows}')  

def hello_protocol(connection: SomeConnection, username: str) -> bool:
    '''
     Checks if server follows the same protocal we are looking for
    '''
    #connection file
    _write_line(connection, f'I32CFSP_HELLO {username}')
    line = _read_line(connection)
    if line == f'WELCOME {username}':
        return True
    else:
        raise ProtocolError
               

def send_player_move(connection: SomeConnection, action: str, column: str) -> None:
    '''
    Sends player's move to the server
    '''
    #connection file
    action = action.upper()
    _write_line(connection, f'{action} {column}')



def read_move(connection: SomeConnection) -> [str]:
    '''
    reads the move sent back from the server
    '''
    #connection file
    move = None
    for times in range(3):
        line = _read_line(connection)
        if 'DROP' in line or  'POP' in line:
            move = line.split()
            break
    if move!= None:
        return move
    else:
        raise ProtocolError

def disconnect(connection: SomeConnection) -> None:
    '''
    closes connection between client and server
    '''
    #Connection file
    connection.input.close()
    connection.output.close()
    connection.socket.close()
    print('You have been disconnected')

