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


def draw_marker(player, x_pos, y_pos):
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
        elif board[0][0] == "o":
            return "o"

    #Check secondary diagonal
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == "x":
            return "x"
        elif board[0][2] == "o":
            return "o"


def is_move_left():
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                return True
    return False


def evaluate():
    if check_win() == "o":
        return 10
    elif check_win() == "x":
        return -10
    else:
        return 0


def minimax(depth, is_max_turn):
    score = evaluate()
    if score == 10 or score == -10:
        return score
    if not is_move_left():
        return 0
    if is_max_turn:
        best = -100
        for i in range(3):
            for j in range(3):
                if board[i][j] == "-":
                    board[i][j] = "o"
                    best = max(best, minimax(depth+1, not is_max_turn)) - depth
                    board[i][j] = "-"
        return best
    else:
        best = 100
        for i in range(3):
            for j in range(3):
                if board[i][j] == "-":
                    board[i][j] = "x"
                    best = min(best, minimax(depth+1, not is_max_turn)) + depth
                    board[i][j] = "-"
        return best

def find_best_move():
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                board[i][j] = "o"
                move_val = minimax(0, False)
                board[i][j] = "-"
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

def update_and_wait(delay):
    pygame.display.flip()
    pygame.event.pump()
    pygame.time.delay(delay * 1000)

def play_against_cpu():
    global game_over
    pygame.mixer.music.load("music.wav")
    screen.fill("cyan")
    draw_grid()
    player = "x"
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and is_move_left() and player == "x":
                x = int((event.pos[0]) / (WIDTH/3))
                y = int((event.pos[1]) / (HEIGHT/3))
                if draw_marker(player, x, y):
                    player = change_player(player)
                    update_and_wait(1)
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    start_menu()


        if check_win() == "x":
            game_over = True
            draw_text("YOU WON", 30, WIDTH/2, HEIGHT/2, "black")
            draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
        elif check_win() == "o":
            game_over = True
            draw_text("CPU WON", 30, WIDTH/2, HEIGHT/2, "black")
            draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
        elif not is_move_left():
           draw_text("DRAW", 30, WIDTH/2, HEIGHT/2, "black")
           draw_text("PRESS SPACE FOR MAIN MENU", 30, WIDTH/2, (HEIGHT/2) + 50, "black")
           game_over = True
        if player == "o" and not game_over:
            move = find_best_move()
            draw_marker(player, move[1], move[0])
            player = change_player(player)
        pygame.display.update()


def play_against_human():
    pygame.mixer.music.load("music.wav")
    global game_over
    screen.fill("cyan")
    draw_grid()
    player = "x"
    pygame.mixer.music.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and is_move_left():
                x = int((event.pos[0]) / (WIDTH/3))
                y = int((event.pos[1]) / (HEIGHT/3))
                if draw_marker(player, x, y):
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
        elif not is_move_left():
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