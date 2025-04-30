def heuristic(data):
    ai_score = data.aiScore
    player_score = data.playerScore
    ai_stones = sum(data.square[1:6])
    player_stones = sum(data.square[7:12])
    mandarin_diff = data.square[0] - data.square[6]
    #đếm số ô trống của người chơi và AI
    player_empty_squares = sum(1 for i in range(7, 12) if data.square[i] == 0)
    ai_empty_squares = sum(1 for i in range(1, 6) if data.square[i] == 0)

    value = (10 * (ai_score - player_score)) + (ai_stones - player_stones) + (2 * mandarin_diff) + (3 * (player_empty_squares - ai_empty_squares)) 
    return value if data.player == 1 else -value  
