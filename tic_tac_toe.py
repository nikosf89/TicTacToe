import pygame
from sys import exit

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC-TAC-TOE")

def draw_grid():
    for i in range(1,3):
        pygame.draw.line(screen, "black", (i*WIDTH/3, 0), (i*WIDTH/3, HEIGHT), width=5)
        pygame.draw.line(screen, "black", (0, i*HEIGHT/3), (WIDTH, i*HEIGHT/3), width=5)

    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("cyan")  
    draw_grid()
    pygame.display.update()
