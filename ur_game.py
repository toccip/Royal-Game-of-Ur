#!/usr/bin/env python3

import pygame
import random

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
TILE_WIDTH = WINDOW_WIDTH / 10

class Tile():

    def __init__(self, rose=False):
        self.player = 0
        self.color = (255, 255, 255) if not rose else (221,160,221)
        self.xpos = 0
        self.ypos = 0
        self.rose = rose
        self.marked = False

    def set_position(self, a_xpos, a_ypos):
        self.xpos = a_xpos
        self.ypos = a_ypos

    def draw(self, a_window):
        pygame.draw.rect(a_window, (0, 0, 0), (self.xpos, self.ypos, TILE_WIDTH, TILE_WIDTH))
        pygame.draw.rect(a_window, self.color, (self.xpos + 5, self.ypos + 5, TILE_WIDTH - 10, TILE_WIDTH - 10))
        if self.marked:
            pygame.draw.circle(a_window, (0, 255, 0), (self.xpos + 40, self.ypos + 10), 5)
        if self.player != 0:
            player_color = (0, 0, 255) if self.player == 1 else (255, 0, 0)
            pygame.draw.circle(a_window, player_color, (self.xpos + 25, self.ypos + 25), 15)

class Board():

    def __init__(self):
        self.board_arr = [[Tile(True), Tile(), Tile(True)],
                          [Tile(), Tile(), Tile()],
                          [Tile(), Tile(), Tile()],
                          [Tile(), Tile(True), Tile()],
                          [None, Tile(), None],
                          [None, Tile(), None],
                          [Tile(True), Tile(), Tile(True)],
                          [Tile(), Tile(), Tile()]]
        start_x = 175
        start_y = 50
        for row in self.board_arr:
            for a_tile in row:
                if a_tile is not None:
                    a_tile.set_position(start_x, start_y)
                start_x += 45
            start_y += 45
            start_x = 175

    def draw(self, window):
        for row in self.board_arr:
            for a_tile in row:
                if a_tile is not None:
                    a_tile.draw(window)


class Game():

    def __init__(self):
        self.my_board = Board()
        self.expected = "roll"
        self.last_input = None
        self.last_roll = 0
        self.font = pygame.font.SysFont('Times New Roman', 30)
        self.turn = 1
        self.p1_pieces = [('bank', None)] * 7
        self.p2_pieces = [('bank', None)] * 7
        self.poss_moves = list()
        self.exit_mark = 0
        self.game_over = 0

    def update(self):
        if self.last_input is None:
            return
        elif self.game_over != 0:
            return
        elif self.last_input[0] == self.expected and self.expected == "roll":
            self.last_roll = self.gen_roll()
            if self.last_roll == 0:
                self.expected = 'roll'
                self.turn = 2 if self.turn == 1 else 1
            else:
                if self.turn == 1:
                    self.gen_moves(self.p1_pieces)
                else:
                    self.gen_moves(self.p2_pieces)

                if self.poss_moves != list():
                    self.expected = 'choose'
                else:
                    self.expected = 'roll'
                    self.turn = 2 if self.turn == 1 else 1
        elif self.last_input[0] == self.expected and self.expected == 'choose':
            good_choice = False
            go_again = False
            if self.last_input[1] == 'exit':
                for a_move in self.poss_moves:
                    if a_move[0] == 'exit':
                        if self.turn == 1:
                            self.p1_pieces.remove(a_move[1])
                            self.p1_pieces.append(('exit', None))
                        else:
                            self.p2_pieces.remove(a_move[1])
                            self.p2_pieces.append(('exit', None))
                        good_choice = True
                        self.exit_mark = 0
                        old_x = a_move[1][1][0]
                        old_y = a_move[1][1][1]
                        self.my_board.board_arr[old_y][old_x].player = 0
                        break
            else:
                for a_move in self.poss_moves:

                    if a_move[0] == self.last_input[1]:
                        good_choice = True
                        a_piece = a_move[1]
                        loc = a_move[0]
                        if self.turn == 1:
                            self.p1_pieces.remove(a_piece)
                            self.p1_pieces.append(('board', loc))
                        else:
                            self.p2_pieces.remove(a_piece)
                            self.p2_pieces.append(('board', loc))
                        a_tile = self.my_board.board_arr[loc[1]][loc[0]]
                        if a_tile.player != 0:
                            if a_tile.player == 1:
                                self.p1_pieces.remove(('board', loc))
                                self.p1_pieces.append(('bank', None))
                            else:
                                self.p2_pieces.remove(('board', loc))
                                self.p2_pieces.append(('bank', None))
                        self.my_board.board_arr[loc[1]][loc[0]].player = self.turn

                        if a_piece[0] == 'board':
                            old_loc = a_piece[1]
                            self.my_board.board_arr[old_loc[1]][old_loc[0]].player = 0

                        if self.my_board.board_arr[loc[1]][loc[0]].rose:
                            go_again = True
                        break
            if good_choice:
                for a_move in self.poss_moves:
                    loc = a_move[0]
                    if loc != 'exit':
                        self.my_board.board_arr[loc[1]][loc[0]].marked = False
                self.exit_mark = 0
                self.poss_moves = list()
                self.expected = 'roll'
                check_pieces = self.p1_pieces if self.turn == 1 else self.p2_pieces
                game_won = True
                for a_piece in check_pieces:
                    if a_piece[0] != 'exit':
                        game_won = False
                        break
                if game_won:
                    self.game_over = self.turn
                elif not go_again:
                    self.turn = 2 if self.turn == 1 else 1


        self.last_input = None

    def draw(self, a_window):
        self.my_board.draw(a_window)
        self.font = pygame.font.SysFont('Times New Roman', 30)
        pygame.draw.rect(a_window, (0, 0, 0), (0, WINDOW_HEIGHT - 50, 125, 50))
        dice_txt = self.font.render('Roll Dice', False, (255, 255, 255))
        a_window.blit(dice_txt, (15, WINDOW_HEIGHT - 35))

        roll_string = 'Last dice roll: ' + str(self.last_roll)
        roll_txt = self.font.render(roll_string, False, (0, 0, 0))
        a_window.blit(roll_txt, (150, WINDOW_HEIGHT - 35))

        info_string = 'Player ' + str(self.turn) + ': ' + self.expected
        info_txt = self.font.render(info_string, False, (0, 0, 0))
        a_window.blit(info_txt, (15, 15))

        self.print_player_info(a_window, "Player 1:", self.p1_pieces, 15, 250)
        self.print_player_info(a_window, "Player 2:", self.p2_pieces, 350, 250)

        if self.exit_mark != 0:
            exit_x = 200 if self.exit_mark == 1 else (200 + 45*2)
            exit_y = 75 + 45 * 5
            pygame.draw.circle(a_window, (0, 255, 0), (exit_x, exit_y), 20)

        if self.game_over != 0:
            self.font = pygame.font.SysFont('Times New Roman', 50)
            pygame.draw.rect(a_window, (0, 0, 0), (100, 200, 300, 100))
            win_txt = self.font.render('Player ' + str(self.game_over) + ' wins!', False, (255, 255, 255))
            a_window.blit(win_txt, (125, 230))

    def print_player_info(self, a_window, p_string, pieces, xstart, ystart):
        p_txt = self.font.render(p_string, False, (0, 0, 0))
        a_window.blit(p_txt, (xstart, ystart))
        ystart += 20

        p_string = "Bank -- "
        piece_cnt = 0
        for a_piece in pieces:
            if a_piece[0] == 'bank':
                piece_cnt += 1
        p_string += str(piece_cnt)
        p_txt = self.font.render(p_string, False, (0, 0, 0))
        a_window.blit(p_txt, (xstart, ystart))
        ystart += 20

        p_string = "Cleared -- "
        piece_cnt = 0
        for a_piece in pieces:
            if a_piece[0] == 'exit':
                piece_cnt += 1
        p_string += str(piece_cnt)
        p_txt = self.font.render(p_string, False, (0, 0, 0))
        a_window.blit(p_txt, (xstart, ystart))
        ystart += 20


    def mouse_pos_to_index(self, mouse_pos):
        x_index = mouse_pos[0] - 175
        y_index = mouse_pos[1] - 50

        if x_index < 0 or y_index < 0 or x_index > (45 * 3) or y_index > (45*8):
            return None
        else:
            x_index = int(x_index / 45)
            y_index = int(y_index / 45)

        if (4 <= y_index < 5) and x_index != 1:
            return None
        elif y_index == 5 and x_index != 1:
            return 'exit'
        else:
            return (x_index, y_index)

    def mouse_input(self, mouse_pos):

        if (0 <= mouse_pos[0] <= 125) and (WINDOW_HEIGHT - 50 <= mouse_pos[1] <= WINDOW_HEIGHT):
            self.last_input = ("roll", None)
        else:
            self.last_input = None
            output = self.mouse_pos_to_index(mouse_pos)
            if output is not None:
                self.last_input = ("choose", output)

    def gen_roll(self):
        roll = 0
        for i in range(4):
            val = random.random()
            if val >= 0.5:
                roll += 1
        return roll

    def gen_moves(self, pieces):
        bank_check = False
        moves_list = list()
        for a_piece in pieces:

            if a_piece[0] == 'bank' and not bank_check:
                bank_check = True
                x_val = 0 if self.turn == 1 else 2
                y_val = (self.last_roll - 4) * -1
            elif a_piece[0] == 'board':
                loc = a_piece[1]
                if (loc[0] == 0 or loc[0] == 2) and loc[1] < 4:

                    if loc[1] - self.last_roll >= 0:
                        x_val = loc[0]
                        y_val = loc[1] - self.last_roll
                    else:
                        x_val = 1
                        y_val = self.last_roll - loc[1] - 1
                elif loc[0] == 1 and (loc[1] + self.last_roll) > 7:

                    x_val = 0 if self.turn == 1 else 2
                    y_val = 7 - self.last_roll + (7 - loc[1]) + 1
                    if y_val < 5:
                        continue
                    elif y_val == 5:
                        self.exit_mark = self.turn
                        moves_list.append(('exit', a_piece))
                        continue
                elif (loc[0] == 0 or loc[0] == 2) and loc[1] > 5:

                    if loc[1] - self.last_roll == 6:
                        x_val = loc[0]
                        y_val = 6
                    elif loc[1] - self.last_roll < 6:
                        if loc[1] - self.last_roll == 5:
                            self.exit_mark = self.turn
                            moves_list.append(('exit', a_piece))
                        continue
                else:

                    x_val = loc[0]
                    y_val = loc[1] + self.last_roll
            else:
                continue

            a_tile = self.my_board.board_arr[y_val][x_val]
            if a_tile.player == 0 or (a_tile.player != self.turn and not a_tile.rose):
                a_tile.marked = True
                moves_list.append(((x_val, y_val), a_piece))
        self.poss_moves = moves_list


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Royal Game of Ur")

    the_game = Game()
    is_running = True

    while is_running:
        window.fill((255, 255, 255))
        the_game.draw(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                the_game.mouse_input(mouse_pos)

        the_game.update()
        pygame.display.update()

    pygame.quit()
