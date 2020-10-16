class User():
    def __init__(self, sid):
        self.__sid = sid
        # self.name = name
        self.__position = None
        self.__total_moves = []
        self.__rows_matrix = [[], [], []]

    def set_position(self, position):
        self.__position = position

    def set_total_moves(self, row, column):
        self.__total_moves.append([row, column])

    def set_rows_matrix(self, row, column):
        self.__rows_matrix[row - 1].append(column)

    def get_player_position(self):
        return self.__position

    def get_player_dictionary(self):
        return {
            "id": self.__sid,
            "moves_matrix": self.__rows_matrix,
            "total_moves": self.__total_moves,
            "position": self.__position
        }
