import pygame
from sys import exit

pygame.init()

WIDTH = 600
HEIGHT = 600

board = [3*[0] for i in range(3)]


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC-TAC-TOE")

def draw_grid():
    for i in range(1,3):
        pygame.draw.line(screen, "black", (i*WIDTH/3, 0), (i*WIDTH/3, HEIGHT), width=5)
        pygame.draw.line(screen, "black", (0, i*HEIGHT/3), (WIDTH, i*HEIGHT/3), width=5)



def draw_marker(player, x, y):
    x_pos = int(x / (WIDTH/3))
    y_pos = int(y / (HEIGHT/3))
    if player == 1 and board[y_pos][x_pos] == 0: 
        board[y_pos][x_pos] = 1
        pygame.draw.line(screen, "red", (30 + 200*x_pos, 30 + 200*y_pos), (200*(x_pos+1) - 30, 200*(y_pos+1)-30), width=10)
        pygame.draw.line(screen, "red", (200*(x_pos+1)-30, 30 + 200*y_pos), (30 + 200*x_pos,200*(y_pos+1)-30), width=10)
        return True
    elif player == 2 and board[y_pos][x_pos] == 0:   
        pygame.draw.circle(screen, "green", (100 + x_pos*200, 100 + y_pos*200), 70, width=10)
        board[y_pos][x_pos] = 2
        return True


def change_player(player):
    if player == 1:
        return 2
    else:
        return 1


def check_win_draw():
    pass


def play_against_cpu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.display.update()


def play_against_human():
    screen.fill("cyan")
    draw_grid()
    player = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if draw_marker(player, x, y):
                    player = change_player(player)
                
        pygame.display.update()



def start_menu():
    my_font = pygame.font.SysFont("Arial", 30, True)
    
    against_player_surface = my_font.render("AGAINST PLAYER", True, "white")
    against_player_rect = against_player_surface.get_rect(center=(WIDTH/2, 100))
    
    against_cpu_surface = my_font.render("AGAINST CPU", True, "white")
    against_cpu_rect = against_cpu_surface.get_rect(center=(WIDTH/2, 200))

    quit_surface = my_font.render("QUIT", True, "white")
    quit_rect = quit_surface.get_rect(center=(WIDTH/2, 300)) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if against_player_rect.collidepoint(x, y):
                    play_against_human()
                elif against_cpu_rect.collidepoint(x, y):
                    pass
                elif quit_rect.collidepoint(x, y):
                    exit()
            

        pygame.draw.rect(screen, "white", against_player_rect, width=4)
        pygame.draw.rect(screen, "white", against_cpu_rect, width=4)
        pygame.draw.rect(screen, "white", quit_rect, width = 4)
        
        screen.blit(against_cpu_surface, against_cpu_rect)
        screen.blit(against_player_surface, against_player_rect)
        screen.blit(quit_surface, quit_rect)
       
        pygame.display.update()


start_menu()
