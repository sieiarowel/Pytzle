# Pytzle

# kode :

```
import pygame
import random

pygame.init()

screen_width = 1000  # Lebar layar
screen_height = 600  # Tinggi layar
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Puzzle Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

image = pygame.image.load('image/image.jpg')  # Ganti path jika perlu
piece_width = image.get_width() // 5
piece_height = image.get_height() // 4 

pieces = [image.subsurface(j * piece_width, i * piece_height, piece_width, piece_height) 
          for i in range(4) for j in range(5)]

random.shuffle(pieces)

positions = [[j * piece_width, i * piece_height] for i in range(4) for j in range(5)]

dragging = False
dragged_piece_index = None
offset_x = 0
offset_y = 0

font = pygame.font.SysFont('Arial', 30)

def check_solution():
    return all(pos == [(idx % 5) * piece_width, (idx // 5) * piece_height] 
               for idx, pos in enumerate(positions))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for idx, pos in enumerate(positions):
                x, y = pos
                if x <= mouse_x <= x + piece_width and y <= mouse_y <= y + piece_height:
                    dragging = True
                    dragged_piece_index = idx
                    offset_x = mouse_x - x
                    offset_y = mouse_y - y
                    break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            dragged_piece_index = None

        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            positions[dragged_piece_index] = [mouse_x - offset_x, mouse_y - offset_y]

    
    screen.fill(WHITE)

    
    for idx, piece in enumerate(pieces):
        x, y = positions[idx]
        screen.blit(piece, (x, y))
        
       
        num_text = font.render(str(idx+1), True, BLACK)
        text_rect = num_text.get_rect(center=(x + piece_width // 2, y + piece_height // 2))
        screen.blit(num_text, text_rect)

    if check_solution():
        win_text = font.render("Puzzle Selesai!", True, BLACK)
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2))

    pygame.display.flip()

pygame.quit()
