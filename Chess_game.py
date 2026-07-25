import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = 75

pygame.display.set_caption("Chess Engine")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BlackRook = pygame.image.load("images/bR.png")
BlackRook = pygame.transform.scale(BlackRook, (75, 75))
BlackKnight = pygame.image.load("images/bN.png")
BlackKnight = pygame.transform.scale(BlackKnight, (75, 75))
BlackBishop = pygame.image.load("images/bB.png")
BlackBishop = pygame.transform.scale(BlackBishop, (75, 75))
BlackQueen = pygame.image.load("images/bQ.png")
BlackQueen = pygame.transform.scale(BlackQueen, (75, 75))
BlackKing = pygame.image.load("images/bK.png")
BlackKing = pygame.transform.scale(BlackKing, (75, 75))
BlackPawn = pygame.image.load("images/bP.png")
BlackPawn = pygame.transform.scale(BlackPawn, (75, 75))

WhiteRook = pygame.image.load("images/wR.png")
WhiteRook = pygame.transform.scale(WhiteRook, (75, 75))
WhiteKnight = pygame.image.load("images/wN.png")
WhiteKnight = pygame.transform.scale(WhiteKnight, (75, 75))
WhiteBishop = pygame.image.load("images/wB.png")
WhiteBishop = pygame.transform.scale(WhiteBishop, (75, 75))
WhiteQueen = pygame.image.load("images/wQ.png")
WhiteQueen = pygame.transform.scale(WhiteQueen, (75, 75))
WhiteKing = pygame.image.load("images/wK.png")
WhiteKing = pygame.transform.scale(WhiteKing, (75, 75))
WhitePawn = pygame.image.load("images/wP.png")
WhitePawn = pygame.transform.scale(WhitePawn, (75, 75))

br = "Black Rook"
bn = "Black Knight"
bb = "Black Bishop"
bq = "Black Queen"
bk = "Black King"
bp = "Black Pawn"

wr = "White Rook"
wn = "White Knight"
wb = "White Bishop"
wq = "White Queen"
wk = "White King"
wp = "White Pawn"

starting_board = [
    [br, bn, bb, bq, bk, bb, bn, br],
    [bp, bp, bp, bp, bp, bp, bp, bp],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [wp, wp, wp, wp, wp, wp, wp, wp],
    [wr, wn, wb, wq, wk, wb, wn, wr]
]

board = []
selected_piece = None
selected_row = None
selected_column = None
valid_moves = []
current_turn = "white"
game_over = False
winner = None
game_result = None

piece_values = {
    wp: 1, bp: 1,
    wn: 3, bn: 3,
    wb: 3, bb: 3,
    wr: 5, br: 5,
    wq: 9, bq: 9,
    wk: 100, bk: 100
}

def reset_game():
    global board, selected_piece, selected_row, selected_column
    global valid_moves, current_turn, game_over, winner, game_result

    board = []

    for row in starting_board:
        new_row = []
        for piece in row:
            new_row.append(piece)
        board.append(new_row)

    selected_piece = None
    selected_row = None
    selected_column = None
    valid_moves = []
    current_turn = "white"
    game_over = False
    winner = None
    game_result = None

reset_game()

def get_piece_colour(piece):
    if piece == None:
        return None

    if piece.startswith("White"):
        return "white"

    if piece.startswith("Black"):
        return "black"

def draw_board():
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                colour = "light grey"
            else:
                colour = "grey"

            pygame.draw.rect(screen, colour, [column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE])

    if selected_piece != None:
        pygame.draw.rect(screen, "yellow", [selected_column * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE], 4)

    for move in valid_moves:
        move_row = move[0]
        move_column = move[1]
        pygame.draw.circle(screen, "green", [move_column * SQUARE_SIZE + 37, move_row * SQUARE_SIZE + 37], 8)

def draw_pieces():
    for row in range(8):
        for column in range(8):
            piece = board[row][column]

            if piece == br:
                screen.blit(BlackRook, (column * 75, row * 75))
            elif piece == bn:
                screen.blit(BlackKnight, (column * 75, row * 75))
            elif piece == bb:
                screen.blit(BlackBishop, (column * 75, row * 75))
            elif piece == bq:
                screen.blit(BlackQueen, (column * 75, row * 75))
            elif piece == bk:
                screen.blit(BlackKing, (column * 75, row * 75))
            elif piece == bp:
                screen.blit(BlackPawn, (column * 75, row * 75))
            elif piece == wr:
                screen.blit(WhiteRook, (column * 75, row * 75))
            elif piece == wn:
                screen.blit(WhiteKnight, (column * 75, row * 75))
            elif piece == wb:
                screen.blit(WhiteBishop, (column * 75, row * 75))
            elif piece == wq:
                screen.blit(WhiteQueen, (column * 75, row * 75))
            elif piece == wk:
                screen.blit(WhiteKing, (column * 75, row * 75))
            elif piece == wp:
                screen.blit(WhitePawn, (column * 75, row * 75))

def check_pawn_moves(row, column, piece):
    moves = []
    colour = get_piece_colour(piece)

    if colour == "white":
        direction = -1
        new_row = row + direction

        if 0 <= new_row < 8:
            if board[new_row][column] == None:
                moves.append((new_row, column))

                if row == 6:
                    new_row = row + (direction * 2)

                    if board[new_row][column] == None:
                        moves.append((new_row, column))

        new_row = row + direction

        if 0 <= new_row < 8:
            if column - 1 >= 0:
                target = board[new_row][column - 1]

                if target != None:
                    if get_piece_colour(target) == "black":
                        moves.append((new_row, column - 1))

            if column + 1 < 8:
                target = board[new_row][column + 1]

                if target != None:
                    if get_piece_colour(target) == "black":
                        moves.append((new_row, column + 1))

    else:
        direction = 1
        new_row = row + direction

        if 0 <= new_row < 8:
            if board[new_row][column] == None:
                moves.append((new_row, column))

                if row == 1:
                    new_row = row + (direction * 2)

                    if board[new_row][column] == None:
                        moves.append((new_row, column))

        new_row = row + direction

        if 0 <= new_row < 8:
            if column - 1 >= 0:
                target = board[new_row][column - 1]

                if target != None:
                    if get_piece_colour(target) == "white":
                        moves.append((new_row, column - 1))

            if column + 1 < 8:
                target = board[new_row][column + 1]

                if target != None:
                    if get_piece_colour(target) == "white":
                        moves.append((new_row, column + 1))

    return moves

def check_knight_moves(row, column, piece):
    moves = []
    colour = get_piece_colour(piece)

    targets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    for target in targets:
        new_row = row + target[0]
        new_column = column + target[1]

        if 0 <= new_row < 8 and 0 <= new_column < 8:
            target_piece = board[new_row][new_column]

            if target_piece == None:
                moves.append((new_row, new_column))
            elif get_piece_colour(target_piece) != colour:
                moves.append((new_row, new_column))

    return moves

def check_rook_moves(row, column, piece):
    moves = []
    colour = get_piece_colour(piece)

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for direction in directions:
        new_row = row + direction[0]
        new_column = column + direction[1]

        while 0 <= new_row < 8 and 0 <= new_column < 8:
            target_piece = board[new_row][new_column]

            if target_piece == None:
                moves.append((new_row, new_column))
            else:
                if get_piece_colour(target_piece) != colour:
                    moves.append((new_row, new_column))
                break

            new_row += direction[0]
            new_column += direction[1]

    return moves

def check_bishop_moves(row, column, piece):
    moves = []
    colour = get_piece_colour(piece)

    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for direction in directions:
        new_row = row + direction[0]
        new_column = column + direction[1]

        while 0 <= new_row < 8 and 0 <= new_column < 8:
            target_piece = board[new_row][new_column]

            if target_piece == None:
                moves.append((new_row, new_column))
            else:
                if get_piece_colour(target_piece) != colour:
                    moves.append((new_row, new_column))
                break

            new_row += direction[0]
            new_column += direction[1]

    return moves

def check_queen_moves(row, column, piece):
    moves = []
    rook_moves = check_rook_moves(row, column, piece)
    bishop_moves = check_bishop_moves(row, column, piece)

    moves.extend(rook_moves)
    moves.extend(bishop_moves)

    return moves

def check_king_moves(row, column, piece):
    moves = []
    colour = get_piece_colour(piece)

    targets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for target in targets:
        new_row = row + target[0]
        new_column = column + target[1]

        if 0 <= new_row < 8 and 0 <= new_column < 8:
            target_piece = board[new_row][new_column]

            if target_piece == None:
                moves.append((new_row, new_column))
            elif get_piece_colour(target_piece) != colour:
                moves.append((new_row, new_column))

    return moves

def get_basic_moves(row, column):
    piece = board[row][column]

    if piece == None:
        return []

    if piece == wp or piece == bp:
        return check_pawn_moves(row, column, piece)

    elif piece == wr or piece == br:
        return check_rook_moves(row, column, piece)

    elif piece == wn or piece == bn:
        return check_knight_moves(row, column, piece)

    elif piece == wb or piece == bb:
        return check_bishop_moves(row, column, piece)

    elif piece == wq or piece == bq:
        return check_queen_moves(row, column, piece)

    elif piece == wk or piece == bk:
        return check_king_moves(row, column, piece)

    return []

def find_king(colour):
    if colour == "white":
        king = wk
    else:
        king = bk

    for row in range(8):
        for column in range(8):
            if board[row][column] == king:
                return row, column

    return None

def is_in_check(colour):
    king_position = find_king(colour)

    if king_position == None:
        return True

    king_row = king_position[0]
    king_column = king_position[1]

    if colour == "white":
        enemy_colour = "black"
    else:
        enemy_colour = "white"

    for row in range(8):
        for column in range(8):
            piece = board[row][column]

            if piece != None:
                if get_piece_colour(piece) == enemy_colour:
                    enemy_moves = get_basic_moves(row, column)

                    if (king_row, king_column) in enemy_moves:
                        return True

    return False

def move_leaves_king_in_check(start_row, start_column, end_row, end_column):
    moving_piece = board[start_row][start_column]
    captured_piece = board[end_row][end_column]

    board[end_row][end_column] = moving_piece
    board[start_row][start_column] = None

    colour = get_piece_colour(moving_piece)
    result = is_in_check(colour)

    board[start_row][start_column] = moving_piece
    board[end_row][end_column] = captured_piece

    return result

def get_legal_moves(row, column):
    legal_moves = []
    basic_moves = get_basic_moves(row, column)

    for move in basic_moves:
        new_row = move[0]
        new_column = move[1]

        if not move_leaves_king_in_check(row, column, new_row, new_column):
            legal_moves.append(move)

    return legal_moves

def get_all_legal_moves(colour):
    all_moves = []

    for row in range(8):
        for column in range(8):
            piece = board[row][column]

            if piece != None:
                if get_piece_colour(piece) == colour:
                    legal_moves = get_legal_moves(row, column)

                    for move in legal_moves:
                        move_data = (row, column, move[0], move[1])
                        all_moves.append(move_data)

    return all_moves

def has_legal_moves(colour):
    moves = get_all_legal_moves(colour)

    if len(moves) > 0:
        return True

    return False

def check_game_result():
    global game_over, winner, game_result

    legal_moves = get_all_legal_moves(current_turn)

    if len(legal_moves) == 0:
        game_over = True

        if is_in_check(current_turn):
            if current_turn == "white":
                winner = "black"
            else:
                winner = "white"

            game_result = "checkmate"

        else:
            winner = None
            game_result = "stalemate"

def promote_pawn(row, column):
    piece = board[row][column]

    if piece == wp:
        if row == 0:
            board[row][column] = wq

    elif piece == bp:
        if row == 7:
            board[row][column] = bq

def make_move(move):
    start_row = move[0]
    start_column = move[1]
    end_row = move[2]
    end_column = move[3]

    moving_piece = board[start_row][start_column]

    board[end_row][end_column] = moving_piece
    board[start_row][start_column] = None

    promote_pawn(end_row, end_column)

def undo_move(move, captured_piece, original_piece):
    start_row = move[0]
    start_column = move[1]
    end_row = move[2]
    end_column = move[3]

    board[start_row][start_column] = original_piece
    board[end_row][end_column] = captured_piece

def evaluate_board():
    score = 0

    for row in range(8):
        for column in range(8):
            piece = board[row][column]

            if piece != None:
                value = piece_values[piece]

                if get_piece_colour(piece) == "black":
                    score += value
                else:
                    score -= value

    return score

def minimax(depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_board()

    if maximizing_player:
        best_score = -10000
        moves = get_all_legal_moves("black")

        if len(moves) == 0:
            if is_in_check("black"):
                return -10000

            return 0

        for move in moves:
            end_row = move[2]
            end_column = move[3]

            captured_piece = board[end_row][end_column]
            original_piece = board[move[0]][move[1]]

            make_move(move)

            score = minimax(depth - 1, alpha, beta, False)

            undo_move(move, captured_piece, original_piece)

            if score > best_score:
                best_score = score

            if best_score > alpha:
                alpha = best_score

            if beta <= alpha:
                break

        return best_score

    else:
        best_score = 10000
        moves = get_all_legal_moves("white")

        if len(moves) == 0:
            if is_in_check("white"):
                return 10000

            return 0

        for move in moves:
            end_row = move[2]
            end_column = move[3]

            captured_piece = board[end_row][end_column]
            original_piece = board[move[0]][move[1]]

            make_move(move)

            score = minimax(depth - 1, alpha, beta, True)

            undo_move(move, captured_piece, original_piece)

            if score < best_score:
                best_score = score

            if best_score < beta:
                beta = best_score

            if beta <= alpha:
                break

        return best_score

def find_best_move():
    moves = get_all_legal_moves("black")

    if len(moves) == 0:
        return None

    best_score = -10000
    best_moves = []

    for move in moves:
        end_row = move[2]
        end_column = move[3]

        captured_piece = board[end_row][end_column]
        original_piece = board[move[0]][move[1]]

        make_move(move)

        score = minimax(2, -10000, 10000, False)

        undo_move(move, captured_piece, original_piece)

        if score > best_score:
            best_score = score
            best_moves = [move]

        elif score == best_score:
            best_moves.append(move)

    if len(best_moves) > 0:
        return random.choice(best_moves)

    return None

def ai_turn():
    global current_turn

    if game_over:
        return

    print("AI is thinking...")

    best_move = find_best_move()

    if best_move != None:
        print("AI chose move:", best_move)
        make_move(best_move)

    current_turn = "white"

    check_game_result()

def draw_game_over():
    font = pygame.font.Font(None, 40)

    if game_result == "stalemate":
        message = "Stalemate!"
    elif winner == "white":
        message = "White wins!"
    else:
        message = "Black wins!"

    text = font.render(message, True, "white")
    restart_text = font.render("Press ENTER to restart", True, "white")

    pygame.draw.rect(screen, "black", [100, 250, 550, 150])

    screen.blit(text, [270, 275])
    screen.blit(restart_text, [190, 325])

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                if game_over:
                    reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over == False:

                if current_turn == "white":

                    mouse_x = event.pos[0]
                    mouse_y = event.pos[1]

                    column = mouse_x // SQUARE_SIZE
                    row = mouse_y // SQUARE_SIZE

                    if 0 <= row < 8 and 0 <= column < 8:

                        piece = board[row][column]

                        if selected_piece == None:

                            if piece != None:

                                piece_colour = get_piece_colour(piece)

                                if piece_colour == "white":

                                    selected_piece = piece
                                    selected_row = row
                                    selected_column = column
                                    valid_moves = get_legal_moves(row, column)

                        else:

                            if (row, column) in valid_moves:

                                move = (selected_row, selected_column, row, column)

                                make_move(move)

                                selected_piece = None
                                selected_row = None
                                selected_column = None
                                valid_moves = []

                                current_turn = "black"

                                check_game_result()

                                if game_over == False:
                                    ai_turn()

                            elif piece != None:

                                piece_colour = get_piece_colour(piece)

                                if piece_colour == "white":

                                    selected_piece = piece
                                    selected_row = row
                                    selected_column = column
                                    valid_moves = get_legal_moves(row, column)

                            else:

                                selected_piece = None
                                selected_row = None
                                selected_column = None
                                valid_moves = []

    draw_board()
    draw_pieces()

    if game_over:
        draw_game_over()

    pygame.display.flip()

pygame.quit()