#Sandra Wang 14772372
import connectfour
import connectfour_shared


def whos_turn(game: 'GameState')-> str:
    '''
    returns whose turn it is in the game
    '''
    #local
    if game.turn == connectfour.RED:
         return '[RED]'
    else:
         return '[YELLOW]'

def start() -> None:
    '''
    Main function of Local connectfour game. It asks the players move inputs
    until someone has won or the game ends in a draw
    It then prints the winner if there is one
    '''
    #Local file
    connectfour_shared.start_sequence()
    game = connectfour_shared.creating_new_game()[0]
    connectfour_shared.print_board(game)
    while connectfour.winner(game) == connectfour.EMPTY:
        if connectfour_shared.board_filled(game) == True:
            print("It's a draw.")
            break

        who = whos_turn(game)
        print(who)
        move_list = connectfour_shared.ask_next_move(game)

        if connectfour_shared.valid_move(game, move_list):
            game= connectfour_shared.moves(game, move_list)
            connectfour_shared.print_board(game)
            
    if connectfour.winner(game)!= connectfour.EMPTY:
        connectfour_shared.print_winner(game)
    print('GAME OVER.')

if __name__ == '__main__':
    start()
