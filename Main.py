import pprint as pp
from game import *

if __name__ == "__main__":
    game = Game(init_state=(
            {(1,1), (1,2), (1,3), (1,4), (1,5), (2,1), (2,2), (2,3), (2,4), (3,1), (3,2), (3,3), (4,1), (4,2), (5, 1)},
            {(6,10), (7,10), (8,10), (9,10), (10,10), (7,9), (8,9), (9,9), (10,9), (8, 8), (9,8), (10,8), (9,7), (10,7), (10, 6)},))
    playing = True
    while playing:
        player_turn = 1 if game.is_p1_turn else 2
        print("tablero:")
        pp.pprint(game.tablero(game.curr_node.state))

        print("Turno del jugador:", player_turn)

        if player_turn == 2:
            is_valid = False
            while not is_valid:
                try:
                    init_coord = input("Escriba que pieza quiere mover: ")
                    init_coord = tuple(int(n) for n in init_coord.split(','))
                    dest_coord = input("Ingrese la coordenada destino: ")
                    dest_coord = tuple(int(n) for n in dest_coord.split(','))
                    is_valid = game.movimiento(init_coord, dest_coord) 
                except Exception:
                    print("Error, ejemplo: 1,1 ")
        elif player_turn == 1:
            val, movimiento = game.minimax(game.curr_node, 3, -math.inf, math.inf, True)
            print("El rival ha movido la  ", movimiento[0], "a la", movimiento[1])
            is_valid = game.movimiento(movimiento[0], movimiento[1])
