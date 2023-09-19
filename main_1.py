# Основа игры
def play_chess(m, figures):
    # Учет хода пешки при взятии на проходе
    psh_xod = 0
    # Счетчик ходов
    xod = 1

    while True:
        # Белый/черный
        color = xod % 2
        if color == True:
            print(xod, "Ход белых:")
        else:
            print(xod, "Ход черных:")

        # Мат
        flk=0
        flb=0
        for i in range(len(m.board)):
            for j in range(len(m.board[i])):
                if m.board[i][j] == 'k':
                    flk = 1
                if m.board[i][j] == 'K':
                    flb = 1
        if flk == 0:
            print('Выиграл белые')
            break
        if flb == 0:
            print('Выиграли черные')
            break

        m.show_board()
        m.show_figures_under_fight(figures, color)
        # Проверка координат фигуры
        s1 = input("Введите координаты фигуры: ")
        try:
            x0, y0 = check_coordinates(s1)
            x0, y0 = figure_error_check(x0, y0, color, figures, m)
        except:
            print("Попробуйте снова!")
            print()
            continue
        # Проверка координат хода
        s2 = input("Введите координаты позиции: ")
        try:

            x, y = check_coordinates(s2)
            # Взятие на проходе
            for i in figures:
                if i.x0 == x0 and i.y0 == y0 and i.icon.lower() == "p":
                    if i.taking_on_pass(psh_xod, x, y, m) == False:
                        x0, y0, x, y = move_error_check(x0, y0, x, y, color, figures, m)
            if m.board[x0][y0].lower() == 'p' and abs(x0 - x) == 2:
                psh_xod = 1
            else:
                psh_xod = 0

        except:
            print("Попробуйте снова!")
            print()
            continue

        # Ход
        xod += 1
        for i in figures:
            if i.x0 == x0 and i.y0 == y0:
                m.board[x][y] = m.board[x0][y0]
                m.board[x0][y0] = '*'
                i.x0 = x
                i.y0 = y
        # Превращение пешки
        for i in range(len(figures)):
            if (figures[i].x0 == 0 and figures[i].icon == 'P') or (figures[i].x0 == 7 and figures[i].icon == 'p'):
                while True:
                    sp = input("Выберите фигуру для превращения (prnbq): ")
                    if len(sp) == 1 and sp.lower() in 'prnbq':
                        if sp.lower() == 'q':
                            figures[i] = Queen(figures[i].x0, figures[i].y0, color, m)
                        elif sp.lower() == 'm':
                            figures[i] = Bishop(figures[i].x0, figures[i].y0, color, m)
                        elif sp.lower() == 'n':
                            figures[i] = Knight(figures[i].x0, figures[i].y0, color, m)
                        elif sp.lower() == 'r':
                            figures[i] = Rook(figures[i].x0, figures[i].y0, color, m)
                        elif sp.lower() == 'p':
                            figures[i] = Pawn(figures[i].x0, figures[i].y0, color, m)
                        break
                    else:
                        print('Некорректный ввод! Повторите ввод:')
                        print()
                        continue


# Шашки
def play_checkers(m, figures):
    xod = 1

    while True:
        # Белый/черный
        color = xod % 2
        if color == True:
            print(xod, "Ходят белые")
        else:
            print(xod, "Ходят черные")

        m.show_board()

        # Проверка координат фигуры
        s1 = input("Введите координаты фигуры: ")
        try:
            x0, y0 = check_coordinates(s1)
        except:
            print("Попробуйте снова!")
            print()
            continue

        # Проверка координат хода
        while True:
            s2 = input("Введите координаты позиции: ")
            try:
                x, y = check_coordinates(s2)
                x0, y0, x, y = move_error_check(x0, y0, x, y, color, figures, m)
            except:
                print("Попробуйте снова!")
                print()
                break

            # Ход
            for i in figures:
                if i.x0 == x0 and i.y0 == y0:
                    f = i
            if abs(x - x0) == 1:
                m.board[x][y] = m.board[x0][y0]
                m.board[x0][y0] = '*'
                f.x0 = x
                f.y0 = y
                xod += 1
                break
            else:
                m.board[x][y] = m.board[x0][y0]
                m.board[x0][y0] = '*'
                m.board[int(x0 - (x0 - x) / 2)][int(y0 - (y0 - y) / 2)] = "*"
                f.x0 = x
                f.y0 = y
                x0 = x
                y0 = y
                if f.check_2(m) == False:
                    xod += 1
                    break
                m.show_board()


def play():
    x = input("1, 2, 3")
    if x == "1":
        self = Board()
        figures = Board.spawn(self)
        play_chess(self, figures)
    elif x == "2":
        self = Board()
        figures = Board.spawn_new(self)
        play_chess(self, figures)
    elif x == "3":
        self = Board()
        figures = Board.spawn_checkers(self)
        play_checkers(self, figures)
    else:
        print('Ошибка!')

# Доска
class Board():
    def __init__(self):
        self.board = []
        [self.board.append(["*"] * 8) for i in range(8)]

    def show_board(self):
        print('  A B C D E F G H')
        for i in range(8):
            print(str(8 - i), end=' ')
            [print(self.board[i][j], end=' ') for j in range(8)]
            print(str(8 - i))
        print('  A B C D E F G H')
        print()

    # Находится ли фигура под боем фигур другого цвета
    def is_figure_under_fight(self, x_p, y_p, figures, color):

        for i in range(8):
            for j in range(8):

                for r in figures:
                    if r.x0 == i and r.y0 == j:
                        if r.check(x_p, y_p, self) == True and r.color != color:
                            return True
        return False

    # Вывод игровой доски с выделением фигур под боем
    def show_figures_under_fight(self, figures, color):
        print('Фигуры под боем: ')
        print('  A B C D E F G H')

        for i in range(8):
            print(str(8 - i), end = ' ')

            # Eсли выбранная фигура под боем
            for j in range(8):
                if self.board[i][j] != "*" and self.board[i][j].isupper() == color and self.is_figure_under_fight(i, j, figures, color) == True:
                    print('#', end =' ')
                else:
                    print(self.board[i][j], end =' ')

            print(str(8 - i))

        print('  A B C D E F G H')

    # Заполнение
    def spawn(self):
        figures = [Bishop(0, 2, False, self), Bishop(0, 5, False, self), Bishop(7, 2, True, self), Bishop(7, 5, True, self), Knight(0, 1, False, self), Knight(0, 6, False, self), Knight(7, 1, True, self), Knight(7, 6, True, self), Rook(0, 0, False, self), Rook(0, 7, False, self), Rook(7, 0, True, self), Rook(7, 7, True, self), Queen(0, 3, False, self), Queen(7, 3, True, self), King(0, 4, False, self), King(7, 4, True, self), Pawn(1, 0, False, self), Pawn(1, 1, False, self), Pawn(1, 2, False, self), Pawn(1, 3, False, self), Pawn(1, 4, False, self), Pawn(1, 5, False, self), Pawn(1, 6, False, self), Pawn(1, 7, False, self), Pawn(6, 0, True, self), Pawn(6, 1, True, self), Pawn(6, 2, True, self), Pawn(6, 3, True, self), Pawn(6, 4, True, self), Pawn(6, 5, True, self), Pawn(6, 6, True, self), Pawn(6, 7, True, self)]
        return figures

    def spawn_new(self):
        figures = [Bishop(0, 2, False, self), Bishop(0, 5, False, self), Bishop(7, 2, True, self), Bishop(7, 5, True, self), Fig1(0, 1, False, self), Fig1(0, 6, False, self), Fig1(7, 1, True, self), Fig1(7, 6, True, self), Rook(0, 0, False, self), Rook(0, 7, False, self), Rook(7, 0, True, self), Rook(7, 7, True, self), Fig2(0, 3, False, self), Fig2(7, 3, True, self), King(0, 4, False, self), King(7, 4, True, self), Pawn(1, 0, False, self), Pawn(1, 1, False, self), Pawn(1, 2, False, self), Pawn(1, 3, False, self), Fig3(1, 4, False, self), Pawn(1, 5, False, self), Pawn(1, 6, False, self), Pawn(1, 7, False, self), Pawn(6, 0, True, self), Pawn(6, 1, True, self), Pawn(6, 2, True, self), Pawn(6, 3, True, self), Fig3(6, 4, True, self), Pawn(6, 5, True, self), Pawn(6, 6, True, self), Pawn(6, 7, True, self)]
        return figures

    def spawn_checkers(self):
        checkers = [Checker(0, 1, False, self), Checker(0, 3, False, self), Checker(0, 5, False, self), Checker(0, 7, False, self), Checker(1, 0, False, self), Checker(1, 2, False, self), Checker(1, 4, False, self), Checker(1, 6, False, self), Checker(2, 1, False, self), Checker(2, 3, False, self), Checker(2, 5, False, self), Checker(2, 7, False, self), Checker(6, 1, True, self), Checker(6, 3, True, self), Checker(6, 5, True, self), Checker(6, 7, True, self), Checker(7, 0, True, self), Checker(7, 2, True, self), Checker(7, 4, True, self), Checker(7, 6, True, self), Checker(5, 0, True, self), Checker(5, 2, True, self), Checker(5, 4, True, self), Checker(5, 6, True, self)]
        return checkers

# Конь
class Knight():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "N"
        else:
            self.icon = "n"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if board_.board[x][y] != '*' and board_.board[x][y].isupper() == self.color:
            return False
        if (x - self.x0) ** 2 + (y - self.y0) ** 2 == 5:
            return True
        else:
            return False


# Ладья
class Rook():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "R"
        else:
            self.icon = "r"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if board_.board[x][y] != '*' and board_.board[x][y].isupper() == self.color:
            return False
        # Горизонталь
        if self.x0 == x:
            for i in range(min(self.y0, y) + 1, max(self.y0, y)):
                if board_.board[self.x0][i] != '*':
                    return False
            return True
        # Вертикаль
        elif self.y0 == y:
            for i in range(min(self.x0, x) + 1, max(self.x0, x)):
                if board_.board[i][self.y0] != '*':
                    return False
            return True
        return False


# Слон
class Bishop():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "B"
        else:
            self.icon = "b"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if board_.board[x][y] != '*' and board_.board[x][y].isupper() == self.color:
            return False
        if abs(self.x0 - x) == abs(self.y0 - y) and self.x0 - x != 0:
            step_y = int((y - self.y0) / abs(y - self.y0))
            step_x = int((x - self.x0) / abs(x - self.x0))
            j = self.x0 + step_x
            for i in range(self.y0 + step_y, y, step_y):
                if board_.board[j][i] != '*':
                    return False
                j += step_x
            return True
        return False


# Ферзь
class Queen(Rook, Bishop):
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "Q"
        else:
            self.icon = "q"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if Rook.check(self, x, y, board_) == True or Bishop.check(self, x, y, board_) == True:
            return True
        else:
            return False


# Король
class King():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "K"
        else:
            self.icon = "k"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if board_.board[x][y] != '*' and board_.board[x][y].isupper() == self.color:
            return False
        if abs(x - self.x0) <= 1 and abs(y - self.y0) <= 1:
            return True
        return False


# Новая фигура 1
class Fig1():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "N"
        else:
            self.icon = "n"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if board_.board[x][y] != '*' and board_.board[x][y].isupper() == self.color:
            return False
        if (x - self.x0) ** 2 + (y - self.y0) ** 2 == 17:
            return True
        else:
            return False


# Новая фигура 2
class Fig2(Rook, Bishop):
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "V"
        else:
            self.icon = "v"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if Rook.check(self, x, y, board_) == True or Bishop.check(self, x, y, board_) == True or Knight.check(self, x, y, board_) == True:
            return True
        else:
            return False


# Новая фигура 3
class Fig3():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "S"
        else:
            self.icon = "s"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if board_.board[x][y] != '*' and board_.board[x][y].isupper() == self.color:
            return False

        if (abs(x - self.x0) <= 1 and abs(y - self.y0) <= 1 and self.x0 == x) or (
                abs(x - self.x0) <= 1 and abs(y - self.y0) <= 1 and self.y0 == y):
            return True
        return False


# Шашка
class Checker():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "O"
        else:
            self.icon = "o"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if abs(y - self.y0) == 1 and board_.board[x][y] == '*' and \
                ((self.color == True and self.x0 - x == 1) or \
                 (self.color == False and self.x0 - x == -1)):
            return True
        elif abs(x - self.x0) == abs(y - self.y0) == 2 and board_.board[x][y] == '*' and \
                board_.board[int(self.x0 - (self.x0 - x) / 2)][int(self.y0 - (self.y0 - y) / 2)] != "*" and \
                board_.board[int(self.x0 - (self.x0 - x) / 2)][int(self.y0 - (self.y0 - y) / 2)].isupper != self.color:
            return True
        return False

    def check_2(self, board_):
        try:
            if self.check(self.x0 - 2, self.y0 - 2, board_) == True:
                return True
        except:
            pass

        try:
            if self.check(self.x0 - 2, self.y0 + 2, board_) == True:
                return True
        except:
            pass

        try:
            if self.check(self.x0 + 2, self.y0 - 2, board_) == True:
                return True
        except:
            pass

        try:
            if self.check(self.x0 + 2, self.y0 + 2, board_) == True:
                return True
        except:
            pass
        return False

# Пешка
class Pawn():
    def __init__(self, x, y, color, board_):
        self.x0 = x
        self.y0 = y
        self.color = color
        if color == True:
            self.icon = "P"
        else:
            self.icon = "p"
        board_.board[self.x0][self.y0] = self.icon

    def check(self, x, y, board_):
        if board_.board[x][y] != '*' and board_.board[x][y].isupper() == self.color:
            return False
        # Простой ход
        if self.y0 == y:
            # Первый длинный ход
            if (self.x0 == 6 and x == 4 and board_.board[5][self.y0] == board_.board[4][
                self.y0] == '*' and self.color == True) or \
                    (self.x0 == 1 and x == 3 and board_.board[2][self.y0] == board_.board[3][
                        self.y0] == '*' and self.color == False):
                return True
            # Короткий ход
            elif board_.board[x][y] == '*' and \
                    ((self.color == True and self.x0 - x == 1) or \
                     (self.color == False and self.x0 - x == -1)):
                return True
        # Взятие фигур
        elif abs(y - self.y0) == 1 and board_.board[x][y] != '*' and \
                ((self.color == True and self.x0 - x == 1) or \
                 (self.color == False and self.x0 - x == -1)):
            return True
        return False

    # Проверка взятия на проходе
    def taking_on_pass(self, psh_xod, x, y, board_):
        # Если ход соперника короткий
        if psh_xod == 0:
            return False
        # Сверху
        if board_.board[self.x0][self.y0] == 'P' and self.x0 == 3 and x == 2 and board_.board[3][y] == 'p':
            board_.board[3][y] = '*'
            return True
        # Внизу
        elif board_.board[self.x0][self.y0] == 'p' and self.x0 == 4 and x == 5 and board_.board[4][y] == 'P':
            board_.board[4][y] = '*'
            return True
        return False


# Проверка
# Формат: "1A", "1a", "a1",  "1 a"
def check_coordinates(s):
    s = s.lower()
    s = s.replace(" ", "")

    if len(s) == 2 and s[0] in '12345678' and s[1] in 'abcdefgh':
        x, y = 8 - int(s[0]), s[1]
    elif len(s) == 2 and s[1] in '12345678' and s[0] in 'abcdefgh':
        x, y = 8 - int(s[1]), s[0]
    else:
        return False

    for i in range(8):
        if y == 'abcdefgh'[i]:
            y = i
            break
    return x, y


# Фигуры
def figure_error_check(x0, y0, color, figures, board_):
    if board_.board[x0][y0] == '*':
        print("Вы не выбрали фигуру!", end='')
        return None
    if board_.board[x0][y0].isupper() != color:
        print("Вы не можете ходить фигурой соперника!", end='')
        return None

    # проверка наличия возможных ходов
    for i in figures:
        if i.x0 == x0 and i.y0 == y0:
            f = i

    for i in range(8):
        for j in range(8):
            if f.check(i, j, board_) == True:
                return x0, y0
    # если нет
    print("Нет возможных ходов! ", end='')
    return None


# Ход
def move_error_check(x0, y0, x, y, color, figures, board_):
    if board_.board[x][y] != '*' and board_.board[x][y].isupper() == color:
        print("Здесь уже стоит ваша фигура! ", end='')
        return None
    for i in figures:
        if i.x0 == x0 and i.y0 == y0:
            if i.check(x, y, board_) == False:
                print("Так ходить нельзя!", end='')
                return None
    return x0, y0, x, y


play()
