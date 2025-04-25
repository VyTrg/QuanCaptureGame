def heuristic(data):
    ai_score = data.aiScore
    player_score = data.playerScore
    ai_stones = sum(data.square[1:6])
    player_stones = sum(data.square[7:12])
    mandarin_diff = data.square[0] - data.square[6]

    value = (10 * (ai_score - player_score)) + (ai_stones - player_stones) + (2 * mandarin_diff)
    return value if data.player == 1 else -value  
