def spawn_position_pawn(team):
    if team == 'white':
        y = 1
    else:
        y = 6
    for x in range(8):
        yield (x, y)


def spawn_position_rock(team):
    if team == 'white':
        y = 0
    else:
        y = 7
    return (0, y), (7, y)


def spawn_position_knight(team):
    if team == 'white':
        y = 0
    else:
        y = 7
    return (1, y), (6, y)


def spawn_position_bishop(team):
    if team == 'white':
        y = 0
    else:
        y = 7
    return (2, y), (5, y)


def spawn_position_king(team):
    if team == 'white':
        y = 0
    else:
        y = 7
    return 4, y


def spawn_position_queen(team):
    if team == 'white':
        y = 0
    else:
        y = 7
    return 3, y
