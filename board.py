from square import Square

class Board:
    squares = []
    result = []
    def __init__(self):
        squares = [Square(position=0, value=0, is_quan=True)] * 14
        for i in range(0, 12):
            if i % 6 == 0:
                squares[i] = Square(position=i, value=5, is_quan=False)
            elif i == 0:
                squares[i] = Square(position=i, value=10, is_quan=True)
            else:
                squares[i] = Square(position=i, value=10, is_quan=True)
        squares[13] = Square(position=13, value=0, is_quan=False)
        squares[14] = Square(position=14, value=0, is_quan=False)
