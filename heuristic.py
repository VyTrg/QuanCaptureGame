def heuristic(data):
    ai_score = data.aiScore
    player_score = data.playerScore
    ai_stones = sum(data.square[1:6])
    player_stones = sum(data.square[7:12])
    mandarin_diff = data.square[0] - data.square[6]
    # đếm số ô trống của người chơi và AI
    player_empty_squares = sum(1 for i in range(7, 12) if data.square[i] == 0)
    ai_empty_squares = sum(1 for i in range(1, 6) if data.square[i] == 0)

    total_stones = sum(data.square)

    # early game
    if total_stones >= 40:
        resource_weight = 2
        score_weight = 5
    # late game
    else:
        resource_weight = 1
        score_weight = 10

    capture_potential = estimate_capture_potential(data)

    isolation_penalty = count_isolated_squares(data, range(1, 6)) if data.player == 1 else count_isolated_squares(data,range(7,12))

    value = (
            score_weight * (ai_score - player_score) +
            resource_weight * (ai_stones - player_stones) +
            5 * mandarin_diff +
            3 * (player_empty_squares - ai_empty_squares) +
            5 * capture_potential -
            2 * isolation_penalty
    )
    return value if data.player == 1 else -value

def estimate_capture_potential(data):
    count = 0
    if data.player == 1:
        for i in range(1, 6):
            if data.square[i] > 0:
                next_idx = (i + data.square[i]) % 12
                if data.square[(next_idx + 1) % 12] == 0 and data.square[(next_idx + 2) % 12] > 0:
                    count += 1
    else:
        for i in range(7, 12):
            if data.square[i] > 0:
                next_idx = (i + data.square[i]) % 12
                if data.square[(next_idx + 1) % 12] == 0 and data.square[(next_idx + 2) % 12] > 0:
                    count += 1
    return count


def count_isolated_squares(data, indices):
    count = 0
    for i in indices:
        if data.square[i] > 0:
            left = data.square[(i - 1) % 12]
            right = data.square[(i + 1) % 12]
            if left == 0 and right == 0:
                count += 1
    return count