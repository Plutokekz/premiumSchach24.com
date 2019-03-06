

class SelectionQueue:

    def __init__(self):
        self.selection_queue_objects = []
        self.selection_queue_indexes = []
        self.add_counter = 0

    def add(self, x, y, field):
        x, y = int(x), int(y)
        self.add_counter += 1
        if len(self.selection_queue_indexes) >= 2:
            """rest selection and make a new one"""
            self.selection_queue_objects = []
            self.selection_queue_indexes = []
        selection = field[y][x]
        self.selection_queue_indexes.append((x, y))
        self.selection_queue_objects.append(selection)
        print(self.selection_queue_indexes)
        if self.add_counter == 2:
            self.add_counter = 0
            self._move_object(field)

    def _move_object(self, field):
        player = self.selection_queue_objects[0]
        if player:
            allowed_coord = player.allowed_coord(field)
            x, y = self.selection_queue_indexes[1]
            if (x, y) in allowed_coord:
                field[y][x] = player
                player.x_pos = x * 100
                player.y_pos = y * 100
                x, y = self.selection_queue_indexes[0]
                field[y][x] = None
                player.first_move = False
            else:
                print('Move not allowed')
