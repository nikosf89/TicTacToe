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


def draw_text(text, size, x, y, color, underline = False, bold = False):
    my_font = pygame.font.SysFont("Arial", size)
    my_font.set_underline(underline)
    my_font.set_bold(bold)
    my_font_surf = my_font.render(text, True, color)
    my_font_rect = my_font_surf.get_rect(center = (x, y))
    screen.blit(my_font_surf, my_font_rect)
    return my_font_rect


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
            return -1
        elif total == 3:
            GAME_OVER = True
            return 1

    #Check main diagonal
    total = 0
    for i in range(3):
        total += BOARD[i][i]
    if total == -3:
        GAME_OVER = True
        return -1
    elif total == 3:
        GAME_OVER = True
        return 1

    #Check secondary diagonal
    total = BOARD[0][2] + BOARD[1][1] + BOARD[2][0]
    if total == -3:
        GAME_OVER = True
        return -1
    elif total == 3:
        GAME_OVER = True
        return 1


def play_against_cpu():
    pygame.mixer.music.load("music.wav")
    screen.fill("cyan")
    draw_grid()
    player = -1
    pygame.mixer.music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.display.update()


def play_against_human():
    pygame.mixer.music.load("music.wav")
    global GAME_OVER
    screen.fill("cyan")
    draw_grid()
    player = -1
    move_count = 0
    pygame.mixer.music.play(loops=-1)
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
            if event.type == pygame.KEYDOWN and GAME_OVER:
                if event.key == pygame.K_SPACE:
                    start_menu()

        if check_win() == -1:
            draw_text("PLAYER 1 WON", 30, WIDTH/2, HEIGHT/2, "black")
            draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
        elif check_win() == 1:
            draw_text("PLAYER 2 WON", 30, WIDTH/2, HEIGHT/2, "black")
            draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
        elif move_count == 9:
           draw_text("DRAW", 30, WIDTH/2, HEIGHT/2, "black")
           draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
           GAME_OVER = True
        pygame.display.update()



def start_menu():
    global GAME_OVER, BOARD
    BOARD = [3*[0] for i in range(3)]
    GAME_OVER = False
    screen.fill("magenta")
    draw_text("MAIN MENU", 40, WIDTH/2, 50, "BLACK", True, True)
    against_player_rect = draw_text("AGAINST PLAYER", 30, WIDTH/2, 150, "black")
    against_cpu_rect = draw_text("AGAINST CPU", 30, WIDTH/2, 300, "black")
    quit_rect = draw_text("QUIT", 30, WIDTH/2, 450, "black")
    pygame.mixer.music.stop()
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
            

        pygame.display.update()



if __name__ == '__main__':
    start_menu()