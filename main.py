import pygame
import sys
from game import OthelloGame
from display import draw_board, draw_menu, draw_difficulty_menu, draw_winner_screen
from constants import CELL_SIZE, BOARD_SIZE, SCREEN

def play_game(game_mode, difficulty='medium'):
    game = OthelloGame(game_mode, difficulty)
    game_over = False
    waiting_for_click = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if waiting_for_click and event.type == pygame.MOUSEBUTTONDOWN:
                return
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if game_mode == 'friend' or (game_mode == 'ai' and game.current_player == 'B'):
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        if game.make_move(row, col):
                            if not game.has_valid_moves():
                                game.current_player = 'W' if game.current_player == 'B' else 'B'
                                if not game.has_valid_moves():
                                    game_over = True
                                    black_score, white_score = game.count_pieces()
                                    if game_mode == 'ai':
                                        winner = "Player" if black_score > white_score else "AI" if white_score > black_score else "Tie"
                                    else:
                                        winner = "Black" if black_score > white_score else "White" if white_score > black_score else "Tie"
                                    
                                    draw_board(game)
                                    draw_winner_screen(winner, black_score, white_score)
                                    pygame.display.flip()
                                    waiting_for_click = True

        if not game_over and game_mode == 'ai' and game.current_player == 'W':
            pygame.time.wait(500)  # Add a small delay to make AI moves visible
            game.ai_move()
            if not game.has_valid_moves():
                game.current_player = 'B'
                if not game.has_valid_moves():
                    game_over = True
                    black_score, white_score = game.count_pieces()
                    winner = "Player" if black_score > white_score else "AI" if white_score > black_score else "Tie"
                    
                    draw_board(game)
                    draw_winner_screen(winner, black_score, white_score)
                    pygame.display.flip()
                    waiting_for_click = True

        if not waiting_for_click:
            draw_board(game)
            pygame.display.flip()

def main():
    while True:
       
        game_mode = draw_menu()
        
        difficulty = 'medium'
        if game_mode == 'ai':
            difficulty = draw_difficulty_menu()
        
        play_game(game_mode, difficulty)

if _name_ == "_main_":
    main()
