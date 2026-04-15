## P - белая пешка, p - черная пешка
#ХОД
#хранит информацию о ходе(фигура, начальная/конечная позиция, съеденная фигура)
class Move:
    def __init__(self, piece, start, end):
        self.piece=piece          #какая фигура совершает ход
        self.start=start          #координаты начальной клетки (x,y)
        self.end=end              #координаты конечной клетки (x,y)
        self.captured=None        #съеденная фигура (если была)


#ФИГУРЫ
class Piece:  #класс для всех фигур (коорд и цвета)
    def __init__(self, color, x, y):
        self._color = color
        self._x = x
        self._y = y

    def move(self, x, y):  #oбновляет позицию фигуры после хода
        self._x = x
        self._y = y

    def get_pos(self):   #возвращает текущие координаты фигуры
        return self._x, self._y

    def get_color(self):   #возвращает цвет фигуры
        return self._color

    def get_moves(self, board):  #возвращает список возможных ходов для фигуры
        return []

    def symbol(self):   #возвращает символ для отображения фигуры на доске
        return "?"


class Pawn(Piece): #движения пешки (ходит вперед на 1 клетку, бьет по диаг)

    def symbol(self):
        return "P" if self._color == "white" else "p"

    def get_moves(self, board):  #направл движ: -1 для белых (вверх), +1 для черных (вниз)
        moves=[]
        direction = -1 if self._color == "white" else 1

        x, y = self.get_pos()
        nx = x + direction


        #ход вперед на одну клетку (если клетка пуста)
        if board.inside(nx, y) and board.get(nx, y) is None:
            moves.append((nx, y))

        #атака по диагонали (слева и справа)
        for dy in [-1, 1]:
            ny = y + dy
            if board.inside(nx, ny):
                target = board.get(nx, ny)
                #можно съесть фигуру противника
                if target is not None and target.get_color() != self.get_color():
                    moves.append((nx, ny))

        return moves


class Rook(Piece):  # движения ладьи  ходит по горизонтали и вертикали на любое расстояние
    def symbol(self):
        return "R" if self._color == "white" else "r"

    def get_moves(self, board):
        moves = []
        x, y = self.get_pos()

        #направления движения: вверх, вниз, вправо, влево
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy

                #выход за пределы доски
                if not board.inside(nx, ny):
                    break

                target = board.get(nx, ny)

                if target is None:  #пустая клетка - можно идти 
                    moves.append((nx, ny))
                else:   #клетка занята: если фигура противника - можно съесть
                    if target.get_color() != self.get_color():
                        moves.append((nx, ny))
                    break #дальше идти нельзя (стена)
 
        return moves


class Knight(Piece):  #движения коня ходит буквой "Г" (2 клетки в одном направлении, 1 в другом) 
    def symbol(self):
        return "N" if self._color == "white" else "n"

    def get_moves(self, board):
        moves = []
        x, y = self.get_pos()

        # Все возможные ходы коня (8 вариантов)
        steps = [(2,1),(2,-1),(-2,1),(-2,-1),
                 (1,2),(1,-2),(-1,2),(-1,-2)]

        for dx, dy in steps:
            nx = x + dx
            ny = y + dy

            if board.inside(nx, ny):
                target = board.get(nx, ny)
                # Можно ходить на пустую клетку или съесть фигуру противника
                if target is None or target.get_color() != self.get_color():
                    moves.append((nx, ny))

        return moves


class King(Piece):   #движения короля  ходит на 1 клетку в любом направлении
    def symbol(self):
        return "K" if self._color == "white" else "k"

    def get_moves(self, board):
        moves = []
        x, y = self.get_pos()

        #все соседние клетки (3x3 область без центра)
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x+dx, y+dy

                if board.inside(nx, ny):
                    target = board.get(nx, ny)
                    if target is None or target.get_color() != self.get_color():
                        moves.append((nx, ny))

        return moves


#ОРИГИНАЛЬНЫЕ ФИГУРЫ

class Wizard(Piece):   #ориг фигура (маг) - ходит как конь + диагональ на 1
    def symbol(self):
        return "W" if self._color == "white" else "w"

    def get_moves(self, board):
        moves = []
        x, y = self.get_pos()


        #объединяем ходы коня (8 вариантов) и диагональные ходы на 1 клетку (4 варианта)
        steps = [(2,1),(2,-1),(-2,1),(-2,-1),   #ходы коня
                 (1,2),(1,-2),(-1,2),(-1,-2),
                 (1,1),(1,-1),(-1,1),(-1,-1)]   #диагональные ходы на 1 клетку


        for dx, dy in steps:
            nx, ny = x + dx, y + dy
            if board.inside(nx, ny):
                target = board.get(nx, ny)
                if target is None or target.get_color() != self.get_color():
                    moves.append((nx, ny))

        return moves


class Cannon(Piece):   #ориг фигура (пушка) - ходит как ладья, бьет через фигуру
    def symbol(self):
        return "C" if self._color == "white" else "c"

    def get_moves(self, board):
        moves = []
        x, y = self.get_pos()

        directions = [(1,0),(-1,0),(0,1),(0,-1)]  #направления как у ладьи (горизонталь и вертикаль)

        for dx, dy in directions:
            nx, ny = x, y
            jumped = False  #флаг: была ли фигура, через которую прыгаем

            while True:
                nx += dx
                ny += dy

                if not board.inside(nx, ny):
                    break

                target = board.get(nx, ny)

                if not jumped:
                    #еще не перепрыгнули ни одной фигуры
                    if target is None:
                        #пустая клетка - обычный ход (как ладья)
                        moves.append((nx, ny))
                    else:
                        #нашли фигуру - через нее можно выстрелить
                        jumped = True
                else:
                    #уже перепрыгнули одну фигуру - ищем цель для выстрела
                    if target is not None:
                        # Попали во вражескую фигуру - можно съесть
                        if target.get_color() != self.get_color():
                            moves.append((nx, ny))
                        break
        return moves


class Assassin(Piece):   #ориг фигура (ассасин) - ходит как король + прыжок на 2
    def symbol(self):
        return "A" if self._color == "white" else "a"

    def get_moves(self, board):
        moves = []
        x, y = self.get_pos()


        #комбинация ходов: король + прыжки на 2 клетки по вертикали/горизонтали
        steps = [
            (1,0),(-1,0),(0,1),(0,-1),          #ходы короля (по прямой)
            (1,1),(1,-1),(-1,1),(-1,-1),        #ходы короля (по диагонали)
            (2,0),(-2,0),(0,2),(0,-2)           #прыжки на 2 клетки по прямой
        ]
        
        for dx, dy in steps:
            nx, ny = x+dx, y+dy
            if board.inside(nx, ny):
                target = board.get(nx, ny)
                if target is None or target.get_color() != self.get_color():
                    moves.append((nx, ny))

        return moves


#ДОСКА 

class Board:   #управление доской (сетка 8x8, перемещение фигур, вывод)
    def __init__(self):
        #создаем сетку 8x8, изначально все клетки пустые (None)
        self._grid = [[None for _ in range(8)] for _ in range(8)]

    def inside(self, x, y):  #проверяет, находятся ли координаты в пределах доски (0-7)
        return 0<=x<8 and 0<=y<8

    def get(self, x, y):  #возвращает фигуру в указанной клетке (или None)
        return self._grid[x][y]

    def set(self, x, y, piece):  #устанавливает фигуру в указанную клетку"
        self._grid[x][y] = piece

    def move_piece(self, move):   #выполняет перемещение фигуры согласно объекту Move
        x1, y1 = move.start
        x2, y2 = move.end


        #удаляем фигуру со старой позиции
        self._grid[x1][y1] = None
        #устанавливаем фигуру на новую позицию
        self._grid[x2][y2] = move.piece
        #обновляем координаты в объекте фигуры
        move.piece.move(x2, y2)

    def all_pieces(self):   #возвращает список всех фигур на доске
        pieces = []
        for i in range(8):
            for j in range(8):
                if self._grid[i][j] is not None:
                    pieces.append(self._grid[i][j])
        return pieces

    def print_board(self):  
        for row in self._grid:
            print(" ".join(cell.symbol() if cell else "." for cell in row))
        print()


#ИГРA

class Game:  #управление игрой (очередность, история ходов, шах, угрозы, игровой цикл)
    def __init__(self):
        self.board = Board()        #игровая доска
        self.turn = "white"         #чей сейчас ход
        self.history = []           #история ходов для отката (задание 3)
        self.setup()                #начальная расстановка фигур


    def setup(self):  #расставляет фигуры на доске в начальной позиции
        #расстановка пешек
        for i in range(8):
            self.board.set(1, i, Pawn("black", 1, i))
            self.board.set(6, i, Pawn("white", 6, i))

        #расстановка ладей
        self.board.set(0, 0, Rook("black", 0, 0))
        self.board.set(0, 7, Rook("black", 0, 7))
        self.board.set(7, 0, Rook("white", 7, 0))
        self.board.set(7, 7, Rook("white", 7, 7))

        #расстановка королей
        self.board.set(7, 4, King("white", 7, 4))
        self.board.set(0, 4, King("black", 0, 4))

        # расстановка оригинальных фигур (задание 2)
        self.board.set(7, 2, Wizard("white", 7, 2))
        self.board.set(0, 2, Wizard("black", 0, 2))

        self.board.set(7, 5, Cannon("white", 7, 5))
        self.board.set(0, 5, Cannon("black", 0, 5))

        self.board.set(7, 3, Assassin("white", 7, 3))
        self.board.set(0, 3, Assassin("black", 0, 3))


    def switch_turn(self):  #Меняет игрока, который должен ходить
        self.turn = "black" if self.turn == "white" else "white"

    def get_attacked_squares(self, color):  #Возвращает список всех клеток, атакуемых фигурами указанного цвета
        attacked = []
        for piece in self.board.all_pieces():
            if piece.get_color() != color:  # Фигуры противника атакуют
                attacked.extend(piece.get_moves(self.board))
        return attacked

    def find_king(self, color):   #Находит позицию короля указанного цвета на доске
        for piece in self.board.all_pieces():
            if isinstance(piece, King) and piece.get_color() == color:
                return piece.get_pos()
        return None

    def is_check(self, color):
        """Проверяет, находится ли король указанного цвета под шахом (задание 5)"""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        # Король под шахом, если его позиция атакуется фигурами противника
        return king_pos in self.get_attacked_squares(color)
    
    def threatened_pieces(self, color):  #Возвр список фигур указанного цвета, которые находятся под боем (задание 5
        attacked = self.get_attacked_squares(color)
        return [p for p in self.board.all_pieces()
                if p.get_color() == color and p.get_pos() in attacked]

    def make_move(self, x1, y1, x2, y2):  #Выполняет ход, если он допустим
        piece = self.board.get(x1, y1)


        #проверка: есть ли фигура на выбранной клетке
        if piece is None:
            print("Нет фигуры")
            return

        #проверка: чья сейчас очередь хода
        if piece.get_color() != self.turn:
            print("Не твой ход")
            return

        #получаем список возможных ходов для выбранной фигуры (задание 4)
        moves = piece.get_moves(self.board)
        print("Возможные ходы:", moves)

        #проверка: допустим ли выбранный ход
        if (x2, y2) not in moves:
            print("Нельзя так ходить")
            return

        #создаем объект хода для истории
        move = Move(piece, (x1, y1), (x2, y2))
        move.captured = self.board.get(x2, y2)   # Запоминаем съеденную фигуру

        #сохраняем ход в историю (задание 3)
        self.history.append(move)
        # Выполняем ход на доске
        self.board.move_piece(move)

        #меняем игрока
        self.switch_turn()

        

    def undo(self):  #откатывает последний ход (задание 3)
        if not self.history:
            print("Нет ходов")
            return

         #берем последний ход из истории
        move = self.history.pop()

        x1, y1 = move.start
        x2, y2 = move.end

        #возвращаем фигуру на начальную позицию
        self.board.set(x1, y1, move.piece)
        move.piece.move(x1, y1)

        #восстанавливаем съеденную фигуру (если была)
        self.board.set(x2, y2, move.captured)

        #меняем игрока обратно
        self.switch_turn()



    def play(self):
        """Основной игровой цикл"""
        while True:
            # Отображаем доску
            self.board.print_board()
            print("Ход:", self.turn)

            # Проверяем шах (задание 5)
            if self.is_check(self.turn):
                print("ШАХ!")

            # Показываем фигуры под боем (задание 5)
            threats = self.threatened_pieces(self.turn)
            if threats:
                print("Под боем:", [p.symbol() for p in threats])

            # Обработка ввода пользователя
            cmd = input(">>> ")

            # Откат хода
            if cmd == "undo":
                self.undo()
                continue

            try:
                x1, y1, x2, y2 = map(int, cmd.split())
                self.make_move(x1, y1, x2, y2)
            except:
                print("Ошибка ввода")



#ЗАПУСК 
if __name__ == "__main__":
    game = Game()
    game.play()










class Piece:
    def __init__(self, color, is_king=False):
        self.color = color  # 'w' или 'b'
        self.is_king = is_king  # True если дамка

    def __str__(self):
        if self.is_king:
            return self.color.upper()
        return self.color


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup()

    def setup(self):
        # Расставляем белые шашки (нижние 3 ряда)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:  # Только чёрные клетки
                    self.grid[row][col] = Piece('w')

        # Расставляем чёрные шашки (верхние 3 ряда)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece('b')

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.grid):
            print(f"{i} ", end="")
            for cell in row:
                if cell:
                    print(cell, end=" ")
                else:
                    print(". ", end="")
            print()

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None

    def set_piece(self, row, col, piece):
        if 0 <= row < 8 and 0 <= col < 8:
            self.grid[row][col] = piece

    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'w'  # Белые ходят первыми

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece = self.board.get_piece(start_row, start_col)
        if not piece or piece.color != self.current_player:
            return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Проверка на корректность хода (диагональ)
        if abs(row_diff) != abs(col_diff):
            return False

        # Простые шашки могут ходить только вперёд
        if not piece.is_king and row_diff * (1 if piece.color == 'w' else -1) < 0:
            return False

        # Проверка на наличие шашки на конечной клетке
        if self.board.get_piece(end_row, end_col):
            return False

        # Проверка на взятие
        if abs(row_diff) == 2:
            mid_row = start_row + row_diff // 2
            mid_col = start_col + col_diff // 2
            mid_piece = self.board.get_piece(mid_row, mid_col)
            if not mid_piece or mid_piece.color == self.current_player:
                return False
            return True

        return True

    def make_move(self, start_row, start_col, end_row, end_col):
        if not self.is_valid_move(start_row, start_col, end_row, end_col):
            print("Неверный ход!")
            return False

        piece = self.board.get_piece(start_row, start_col)
        self.board.set_piece(start_row, start_col, None)
        self.board.set_piece(end_row, end_col, piece)

        # Обработка взятия
        if abs(end_row - start_row) == 2:
            mid_row = start_row + (end_row - start_row) // 2
            mid_col = start_col + (end_col - start_col) // 2
            self.board.set_piece(mid_row, mid_col, None)
            print(f"Взята шашка на поле {mid_row}{mid_col}!")

        # Превращение в дамку
        if (piece.color == 'w' and end_row == 7) or \
           (piece.color == 'b' and end_row == 0):
            piece.is_king = True
            print(f"Шашка стала дамкой на поле {end_row}{end_col}!")

        # Смена игрока
        self.current_player = 'b' if self.current_player == 'w' else 'w'
        return True

    def play(self):
        print("Игра в шашки. Белые (w) ходят первыми.")
        print("Формат ввода: начальная_строка начальная_колонка конечная_строка конечная_колонка")
        print("Пример: 2 3 4 5")

        while True:
            self.board.print_board()
            print(f"Ход {self.current_player}")

            try:
                start_row, start_col, end_row, end_col = map(int, input("> ").split())
                self.make_move(start_row, start_col, end_row, end_col)
            except ValueError:
                print("Ошибка ввода! Используйте формат: 2 3 4 5")
            except IndexError:
                print("Ошибка ввода! Укажите 4 числа.")


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.play()



