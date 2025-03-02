import pygame
import random
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Initialize Pygame
pygame.init()

# Game settings
WINDOW_SIZE = 400
GRID_SIZE = 20
GRID_COUNT = 20
GAME_SPEED = 15

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')

def reset_game():
    return {
        'snake': [[GRID_COUNT//2, GRID_COUNT//2]],
        'direction': [1, 0],
        'food': [random.randrange(GRID_COUNT), random.randrange(GRID_COUNT)],
        'score': 0
    }

def main():
    clock = pygame.time.Clock()
    game_state = reset_game()
    game_over = False

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                    
                if not game_over:
                    if event.key == pygame.K_UP and game_state['direction'] != [0, 1]:
                        game_state['direction'] = [0, -1]
                    elif event.key == pygame.K_DOWN and game_state['direction'] != [0, -1]:
                        game_state['direction'] = [0, 1]
                    elif event.key == pygame.K_LEFT and game_state['direction'] != [1, 0]:
                        game_state['direction'] = [-1, 0]
                    elif event.key == pygame.K_RIGHT and game_state['direction'] != [-1, 0]:
                        game_state['direction'] = [1, 0]
                elif event.key == pygame.K_r:
                    game_state = reset_game()
                    game_over = False

        if not game_over:
            # Move snake
            new_head = [
                (game_state['snake'][0][0] + game_state['direction'][0]) % GRID_COUNT,
                (game_state['snake'][0][1] + game_state['direction'][1]) % GRID_COUNT
            ]
            
            # Check collision with self
            if new_head in game_state['snake']:
                game_over = True
                continue
            
            game_state['snake'].insert(0, new_head)
            
            # Check food collision
            if new_head == game_state['food']:
                game_state['score'] += 1
                while True:
                    game_state['food'] = [random.randrange(GRID_COUNT), random.randrange(GRID_COUNT)]
                    if game_state['food'] not in game_state['snake']:
                        break
            else:
                game_state['snake'].pop()

        # Draw
        screen.fill(BLACK)
        
        # Draw snake
        cell_size = WINDOW_SIZE // GRID_COUNT
        for segment in game_state['snake']:
            pygame.draw.rect(screen, GREEN,
                           (segment[0] * cell_size,
                            segment[1] * cell_size,
                            cell_size - 1, cell_size - 1))
        
        # Draw food
        pygame.draw.rect(screen, RED,
                        (game_state['food'][0] * cell_size,
                         game_state['food'][1] * cell_size,
                         cell_size - 1, cell_size - 1))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {game_state["score"]}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
