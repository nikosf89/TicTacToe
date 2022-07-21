from distutils.command import check
import pygame
from sys import exit

pygame.init()

WIDTH = 600
HEIGHT = 600

BOARD = [3*[0] for i in range(3)]
GAME_OVER = False


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC-TAC-TOE")

def draw_grid():
    for i in range(1,3):
        pygame.draw.line(screen, "black", (i*WIDTH/3, 0), (i*WIDTH/3, HEIGHT), width=5)
        pygame.draw.line(screen, "black", (0, i*HEIGHT/3), (WIDTH, i*HEIGHT/3), width=5)



def draw_marker(player, x, y):
    x_pos = int(x / (WIDTH/3))
    y_pos = int(y / (HEIGHT/3))
    if player == -1 and BOARD[y_pos][x_pos] == 0: 
        BOARD[y_pos][x_pos] = -1
        pygame.draw.line(screen, "red", (30 + 200*x_pos, 30 + 200*y_pos), (200*(x_pos+1) - 30, 200*(y_pos+1)-30), width=10)
        pygame.draw.line(screen, "red", (200*(x_pos+1)-30, 30 + 200*y_pos), (30 + 200*x_pos,200*(y_pos+1)-30), width=10)
        return True
    elif player == 1 and BOARD[y_pos][x_pos] == 0:   
        pygame.draw.circle(screen, "green", (100 + x_pos*200, 100 + y_pos*200), 70, width=10)
        BOARD[y_pos][x_pos] = 1
        return True


def change_player(player):
    if player == -1:
        return 1
    else:
        return -1


def check_win():
    global GAME_OVER
    
    #Check horizontally
    for i in range(3):
        if sum(BOARD[i]) == -3:
            GAME_OVER = True
            return -1
        elif sum(BOARD[i]) == 3:
             GAME_OVER = True
             return 1
        

    #Check vertically
    
    for i in range(3):
        total = 0
        for j in range(3):
            total += BOARD[j][i]
        if total == -3:
            GAME_OVER = True
            return 1
        elif total == 3:
            GAME_OVER = True
            return -1

    #Check main diagonal
    total = 0
    for i in range(3):
        total += BOARD[i][i]
    if total == -3:
        GAME_OVER = True
        return -1
    elif total == 3:
        GAME_OVER = True
        return -1

    #Check secondary diagonal
    total = BOARD[0][2] + BOARD[1][1] + BOARD[2][0]
    if total == -3:
        GAME_OVER = True
        return -1
    elif total == 3:
        GAME_OVER = True
        return 1


def play_against_cpu():
    screen.fill("cyan")
    draw_grid()
    player = -1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.display.update()


def play_against_human():
    screen.fill("cyan")
    draw_grid()
    player = -1
    move_count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER and move_count<9:
                x = event.pos[0]
                y = event.pos[1]
                if draw_marker(player, x, y):
                    move_count += 1
                    player = change_player(player)

        if check_win() == -1:
            print("Player 1 won")
        elif check_win() == 1:
            print("Player 2 won")
        elif move_count == 9:
            print("Draw")
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
                    play_against_cpu()
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
