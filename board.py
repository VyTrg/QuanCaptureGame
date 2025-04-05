from square import Square

class Board:
    squares = []
    result = []
    def __init__(self):
        self.results = []
        self.squares = [None] * 14
        for i in range(12):
            if i % 6 != 0:
                self.squares[i] = Square(i, 5, False)
            elif i == 0:
                self.squares[i] = Square(i, 10, True)
            else:
                self.squares[i] = Square(i, 10, True)
        # first player's pit
        self.squares[12] = Square(12, 0, False) 
        # second player's pit
        self.squares[13] = Square(13, 0, False) 
    
    # update board
    def helper(self, position: int, delta: int) -> int:
        self.squares[position].value += delta

    def left(self, position: int) -> tuple[int, int]:
        stones = self.squares[position].value
        if stones == 0:
            return position - 1, 0 # left direction
        
        # get stones at that square and clear
        self.helper(position, -stones)

        pos = position
        while stones > 0:
            pos = (pos + 1) % 12 #make sure position is in board [0-11]
            self.helper(pos, 1)
            stone -= 1
        
        next_pos = (pos + 1) % 12
        score = 0
        if self.squares[next_pos] == 0 and next_pos != 6:
            capture_pos = (next_pos + 1) % 12
            if self.squares[capture_pos].value > 0:
                score = self.squares[capture_pos].value
                self.helper(capture_pos, -score)
                next_next_pos = (capture_pos + 1) % 12
                if (self.squares[next_next_pos].value == 0 and 
                    next_next_pos % 6 != 0):
                    _, additional_score = self.left(next_pos)
                    score += additional_score
        return pos, score

    def right(self, position: int) -> tuple[int, int]:
        stones = self.squares[position].value
        if stones == 0:
            return position + 1, 0 
        
        self.helper(position, -stones)

        pos = position
        while stones > 0:
            pos = pos - 1 if pos > 0 else 11
            self.helper(pos, 1)
            stone -= 1
        
        next_pos = pos - 1 if pos > 0 else 11
        score = 0
        if self.squares[next_pos] == 0 and next_pos != 6:
            capture_pos = next_pos - 1 if next_pos > 0 else 11
            if self.squares[capture_pos].value > 0:
                score = self.squares[capture_pos].value
                self.helper(capture_pos, -score)
                next_next_pos = capture_pos - 1 if capture_pos > 0 else 11
                if (self.squares[next_next_pos].value == 0 and 
                    next_next_pos % 6 != 0):
                    _, additional_score = self.right(next_pos)
                    score += additional_score
        return pos, score

    # def right(self, position: int) -> int:
    #     stones = self.squares[position].value
    #     if stones == 0:
    #         return position + 1 
        
    #     # get stones at that square and clear
    #     self.helper(position, -stones)

    #     pos = position
    #     while stones > 0:
    #         pos = pos - 1 if pos > 0 else 11
    #         self.helper(pos, 1)
    #         stone -= 1
        
    #     next_pos = pos - 1 if pos > 0 else 11
    #     if self.squares[next_pos] != 0 and next_pos % 6 != 0:
    #         return self.right(next_pos)
    #     return pos
    
    # def eat_left(self, position: int) -> int:
    #     pass

    # def eat_right(self, position: int) -> int:
    #     pass
