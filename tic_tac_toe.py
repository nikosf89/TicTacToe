import pygame
from sys import exit

pygame.init()

#Dimensions of the screen
WIDTH = 600
HEIGHT = 600


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
    if player == "x" and board[y_pos][x_pos] == "-": 
        board[y_pos][x_pos] = "x"
        pygame.draw.line(screen, "red", (30 + 200*x_pos, 30 + 200*y_pos), (200*(x_pos+1) - 30, 200*(y_pos+1)-30), width=10)
        pygame.draw.line(screen, "red", (200*(x_pos+1)-30, 30 + 200*y_pos), (30 + 200*x_pos,200*(y_pos+1)-30), width=10)
        return True
    elif player == "o" and board[y_pos][x_pos] == "-":   
        pygame.draw.circle(screen, "green", (100 + x_pos*200, 100 + y_pos*200), 70, width=10)
        board[y_pos][x_pos] = "o"
        return True


def change_player(player):
    if player == "x":
        return "o"
    else:
        return "x"


def check_win():
    
    #Check horizontally
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == "x":
                return "x"
            elif board[row][0] == "o":
                return "o"
        
    #Check vertically
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == "x":
                return "x"
            elif board[0][col] == "o":
                return "o"

    #Check main diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == "x":
            return "x"
        elif board[0][0] == "x":
            return "O"

    #Check secondary diagonal
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == "x":
            return "x"
        elif board[0][2] == "o":
            return "o"


def play_against_cpu():
    pygame.mixer.music.load("music.wav")
    screen.fill("cyan")
    draw_grid()
    player = "x"
    pygame.mixer.music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.display.update()


def play_against_human():
    pygame.mixer.music.load("music.wav")
    global game_over
    screen.fill("cyan")
    draw_grid()
    player = "x"
    move_count = 0
    pygame.mixer.music.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and move_count<9:
                x = event.pos[0]
                y = event.pos[1]
                if draw_marker(player, x, y):
                    move_count += 1
                    player = change_player(player)
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    start_menu()

        if check_win() == "x":
            game_over = True
            draw_text("PLAYER X WON", 30, WIDTH/2, HEIGHT/2, "black")
            draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
        elif check_win() == "o":
            game_over = True
            draw_text("PLAYER O WON", 30, WIDTH/2, HEIGHT/2, "black")
            draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
        elif move_count == 9:
           draw_text("DRAW", 30, WIDTH/2, HEIGHT/2, "black")
           draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
           game_over = True
        pygame.display.update()



def start_menu():
    #Define the global variable game_over and board
    global game_over, board
    board = [3*["-"] for i in range(3)]
    game_over = False
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