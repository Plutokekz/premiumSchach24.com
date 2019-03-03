from src.Objects.GameObjects import Board
board = Board()
board.setup()

for coord, selection in [[(4, 1), (4, 3)], [(5, 1), (5, 3)], [(6, 1), (6, 3)], [(7, 1), (7, 3)], [(5, 0), (6, 1)], [(7, 3), (7, 4)], [(6, 0), (7, 2)]]:
    pawn = board.select(coord[0], coord[1])
    print(f'try to move {pawn}')
    selection = board.select(selection[0], selection[1])
    board.move(pawn, selection)


rock = board.select(4, 0)
board.update()
print('Knight')
print(board.allowed_moves(rock))
selection = board.select(7, 0)
board.move(rock, selection)
#print('Pawn')
#print(pawn.possible_moves(white=board.coord_white, black=board.coord_black))
print(board)
