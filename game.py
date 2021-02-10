import math
import pprint 
from tree import Node
from copy import deepcopy
class Game(object):
    def __init__(self, init_state):
        self.is_p1_turn = True
        self.board = self.tablero(init_state)
        self.curr_node = Node(state=init_state,parent=None,action=None,value=None)

    def tablero(self, state):
        board = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
        ]

        for pair in state[0]: 
            board[pair[1]-1][pair[0]-1] = 1

        for pair in state[1]: 
            board[pair[1]-1][pair[0]-1] = 2
        return board

    def accion(self, node:Node, player_one:bool):
        accion = []
        player = 0 if player_one else 1
        for piece in node.state[player]:
            for dest in self.movimientos_validos(node, piece, hoop=False, valid_dests=[]):
                accion.append((piece, dest))
        return accion

    def resultado(self, node:Node, action:tuple, player_one):
        player = 0 if player_one else 1
        new_state = deepcopy(node.state)
        new_state[player].remove(action[0])
        new_state[player].add(action[1])
        value = self.rec(new_state) 
        node = Node(state=new_state,parent=node,action=action,value=value)
        return node

    def movimiento(self, coord:tuple, dest_coord:tuple):
        if self.movimiento_valido(coord, dest_coord):
            self.curr_node = self.resultado(self.curr_node, (coord, dest_coord), self.is_p1_turn)
            self.board = self.tablero(self.curr_node.state)
            self.is_p1_turn = not self.is_p1_turn 
            return True
        else:
            return False

    def movimiento_valido(self, coord:tuple, dest_coord:tuple):
        player = 0 if self.is_p1_turn else 1 
        if coord in self.curr_node.state[player]: 
            movimientos_validos = self.movimientos_validos(self.curr_node, coord, valid_dests=[]) 
            if dest_coord in movimientos_validos:
                return True
        return False

    def verificar_direccion(self, coord:tuple, node:Node, delta_x:int, delta_y:int, hoop:bool=False, valid_dests:list=[]):
        board = self.tablero(node.state)
        try:
            n_x = coord[0] + delta_x
            n_y = coord[1] + delta_y
            if not self.en_tablero(n_x, n_y): 
                return
            next_pos = board[n_y-1][n_x-1]
            if (next_pos==0) and (not hoop): 
                valid_dests.append((n_x, n_y))
                return
            elif (next_pos!=0): 
                if self.en_tablero(n_x+delta_x, n_y+delta_y) and (n_x+delta_x, n_y+delta_y) not in valid_dests:
                    if board[n_y+delta_y-1][n_x+delta_x-1]==0:
                        valid_dests.append((n_x+delta_x, n_y+delta_y))
                        return self.movimientos_validos(node=node,coord=(n_x+delta_x, n_y+delta_y),hoop=True,valid_dests=valid_dests)
                return
            else:
                return
        except Exception:
            return
    def en_tablero(self, X:int, Y:int):
        if X <= 10 and X >= 1 and Y <= 10 and Y >= 1:
            return True

        return False

    def en_base(self, node:Node):
        board = self.tablero(node.state)
        is_p1_winner = True
        p1 = 5
        for j in range(0, 5):
            for i in range(p1, 0, -1):
                 is_p1_winner = is_p1_winner and board[j][i-1] == 2
            p1 -= 1
        is_p2_winner = True
        p2 = 0
        for j in range(9, 4, -1):
            for i in range(9, p2+4, -1):
                is_p2_winner = is_p2_winner and board[i][j] == 1
            p2 += 1

        return is_p2_winner or is_p1_winner

    def rec(self, state):
        heuristic = 0
        for piece in state[0]:
            heuristic += piece[0] + piece[1]
        for piece in state[1]:
            heuristic -= piece[0] + piece[1]
        return heuristic

    def minimax(self, node:Node, depth:int, alpha:float, beta:float, max_player:bool):
        if depth==0 or self.en_base(node):
            return node.value, None
        if max_player:
            v = -math.inf
            movimiento = None
            for action in self.accion(node, True): 
                v2, a2 = self.minimax(node = self.resultado(node, action, True),
                                      depth = depth-1, alpha = alpha,
                                      beta = beta, max_player = False)
                if v2 > v:
                    v, movimiento = v2, action
                    alpha = max(alpha, v)
                if beta <= alpha: 
                    break
            return v, movimiento
        else:
            v = math.inf
            movimiento = None
            for action in self.accion(node, False):
                v2, a2 = self.minimax(node = self.resultado(node, action, False),
                                      depth = depth-1, alpha = alpha,
                                      beta = beta, max_player = True)
                if v2 < v:
                    v, movimiento = v2, action
                    beta = min(beta, v)
                if beta <= alpha: 
                    break
            return v, movimiento

    def alpha_beta_search(self, node, depth):
        player = 1 if self.is_p1_turn else 0
        value, movimiento = self.max_value(node, -math.inf, math.inf, depth)
        return movimiento

    def max_value(self, node, alpha, beta, depth):
        if self.en_base(node) or depth<=0:
            return self.rec(node), None
        v = -math.inf
        for a in self.accion(node, True):
            v2, a2 = self.min_value(self.resultado(node, a, False), alpha, beta, depth-1)
            if v2 > v:
                v, movimiento = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, movimiento

    def min_value(self, node, alpha, beta, depth):
        if self.en_base(node) or depth<=0:
            return self.rec(node), None
        v = math.inf
        for a in self.accion(node, True):
            v2, a2 = self.max_value(self.resultado(node, a, True), alpha, beta, depth-1)
            if v2 < v:
                v, movimiento = v2, a
                alpha = min(alpha, v)
            if v >= beta:
                return v, movimiento
    def movimientos_validos(self, node:Node, coord:tuple, hoop:bool=False, valid_dests:list=[]):
       

        self.verificar_direccion(coord=coord, node=node, delta_x=1, 
                            delta_y=0, hoop=hoop, valid_dests=valid_dests) 
        self.verificar_direccion(coord=coord, node=node, delta_x=-1, 
                            delta_y=0, hoop=hoop, valid_dests=valid_dests) 
        self.verificar_direccion(coord=coord, node=node, delta_x=0, 
                            delta_y=1, hoop=hoop, valid_dests=valid_dests) 
        self.verificar_direccion(coord=coord, node=node, delta_x=0, 
                            delta_y=-1, hoop=hoop, valid_dests=valid_dests) 
        self.verificar_direccion(coord=coord, node=node, delta_x=1, 
                            delta_y=1, hoop=hoop, valid_dests=valid_dests) 
        self.verificar_direccion(coord=coord, node=node, delta_x=-1, 
                            delta_y=-1, hoop=hoop, valid_dests=valid_dests) 
        self.verificar_direccion(coord=coord, node=node, delta_x=1, 
                            delta_y=-1, hoop=hoop, valid_dests=valid_dests) 
        self.verificar_direccion(coord=coord, node=node, delta_x=-1, 
                            delta_y=1, hoop=hoop, valid_dests=valid_dests)

        return valid_dests