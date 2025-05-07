# File học máy cho AI chơi Ô Ăn Quan
import os
import json
import random
import numpy as np
from collections import defaultdict

# Đường dẫn file để lưu dữ liệu học tập
GAME_HISTORY_FILE = "game_history.json"
LEARNING_MODEL_FILE = "learning_model.json"

class ReinforcementLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.2):
        self.learning_rate = learning_rate      # Tốc độ học (alpha)
        self.discount_factor = discount_factor  # Hệ số chiết khấu (gamma)
        self.exploration_rate = exploration_rate  # Tỉ lệ khám phá (epsilon)
        
        # Bảng Q lưu trữ giá trị của các cặp trạng thái-hành động
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # Lịch sử trận đấu để học tập
        self.game_history = []
        
        # Trọng số cho hàm đánh giá có thể học được
        self.weights = {
            'score': 5.0,            # Trọng số cho điểm số
            'resources': 2.0,        # Trọng số cho tài nguyên (số quân)
            'mandarin': 6.0,         # Trọng số cho quân Quan
            'empty_squares': 2.5,    # Trọng số cho ô trống
            'capture_potential': 5.0, # Trọng số cho khả năng bắt quân
            'isolation': 1.5,        # Trọng số cho ô cô lập
            'distribution': 1.5,     # Trọng số cho phân bố quân
            'mandarin_safety': 4.0,  # Trọng số cho an toàn của quân Quan
            'sequence': 2.0          # Trọng số cho chuỗi ăn quân
        }
        
        # Tải mô hình nếu đã có từ trước
        self.load_model()
    
    def get_state_key(self, data):
        """Tạo khóa duy nhất cho trạng thái trò chơi"""
        board_str = ",".join(str(x) for x in data.square)
        player_str = str(data.player)
        return f"{board_str}:{player_str}"
    
    def get_action_key(self, pos, direction):
        """Tạo khóa duy nhất cho hành động"""
        return f"{pos}-{direction}"
    
    def choose_action(self, state_key, possible_actions):
        """Chọn hành động dựa trên chiến lược epsilon-greedy"""
        # Khám phá: chọn hành động ngẫu nhiên
        if random.random() < self.exploration_rate:
            return random.choice(possible_actions)
        
        # Khai thác: chọn hành động tốt nhất dựa trên Q-value
        q_values = {action: self.q_table[state_key][action] for action in possible_actions}
        
        # Nếu không có giá trị Q nào, chọn ngẫu nhiên
        if not q_values or all(value == 0 for value in q_values.values()):
            return random.choice(possible_actions)
        
        # Chọn hành động có giá trị Q cao nhất
        return max(q_values, key=q_values.get)
    
    def update_q_value(self, state, action, next_state, reward, is_terminal=False):
        """Cập nhật giá trị Q cho cặp trạng thái-hành động"""
        # Q-learning formula: Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
        current_q = self.q_table[state][action]
        
        if is_terminal:
            # Nếu là trạng thái kết thúc, không có giá trị tương lai
            max_future_q = 0
        else:
            # Nếu không phải trạng thái kết thúc, tính giá trị tương lai tối đa
            future_q_values = [self.q_table[next_state][a] for a in self.q_table[next_state]]
            max_future_q = max(future_q_values) if future_q_values else 0
        
        # Công thức Q-learning
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        
        # Cập nhật giá trị Q
        self.q_table[state][action] = new_q
    
    def record_move(self, data, pos, direction, score):
        """Ghi lại một nước đi vào lịch sử trận đấu"""
        state_key = self.get_state_key(data)
        action_key = self.get_action_key(pos, direction)
        
        self.game_history.append({
            'state': state_key,
            'action': action_key,
            'score': score,
            'player': data.player
        })
    
    def learn_from_game(self, winner):
        """Học từ lịch sử trận đấu vừa kết thúc"""
        # Nếu không có lịch sử, không có gì để học
        if not self.game_history:
            return
        
        # Phân tích lịch sử trận đấu để học hỏi
        for i in range(len(self.game_history) - 1):
            current = self.game_history[i]
            next_move = self.game_history[i + 1]
            
            # Tính toán phần thưởng
            reward = current['score']
            
            # Thêm phần thưởng cho người chiến thắng
            if i == len(self.game_history) - 2:  # Nước đi cuối cùng
                if (winner == 1 and current['player'] == 1) or (winner == 2 and current['player'] == 2):
                    reward += 10  # Phần thưởng lớn cho người thắng
                else:
                    reward -= 5   # Hình phạt cho người thua
            
            # Cập nhật giá trị Q
            self.update_q_value(
                state=current['state'],
                action=current['action'],
                next_state=next_move['state'],
                reward=reward,
                is_terminal=(i == len(self.game_history) - 2)
            )
        
        # Điều chỉnh trọng số dựa trên kết quả trận đấu
        self.adjust_weights(winner)
        
        # Lưu mô hình và xóa lịch sử trận đấu
        self.save_model()
        self.game_history = []
    
    def adjust_weights(self, winner):
        """Điều chỉnh trọng số dựa trên kết quả trận đấu"""
        # Phân tích các nước đi của người chiến thắng
        winner_moves = [move for move in self.game_history if move['player'] == winner]
        
        if not winner_moves:
            return
        
        # Tính điểm trung bình của các nước đi thắng
        avg_score = sum(move['score'] for move in winner_moves) / len(winner_moves)
        
        # Điều chỉnh trọng số dựa trên điểm trung bình
        if avg_score > 2:  # Nếu điểm trung bình cao
            self.weights['capture_potential'] *= 1.05  # Tăng trọng số bắt quân
            self.weights['sequence'] *= 1.03          # Tăng trọng số chuỗi ăn quân
        else:  # Nếu điểm trung bình thấp
            self.weights['resources'] *= 1.03         # Tăng trọng số tài nguyên
            self.weights['mandarin_safety'] *= 1.02   # Tăng trọng số bảo vệ quân Quan
        
        # Giới hạn trọng số để không tăng vô hạn
        for key in self.weights:
            self.weights[key] = min(self.weights[key], 10.0)
    
    def save_model(self):
        """Lưu mô hình học máy"""
        model_data = {
            'weights': self.weights,
            'q_table': {state: dict(actions) for state, actions in self.q_table.items()}
        }
        
        try:
            with open(LEARNING_MODEL_FILE, 'w') as f:
                json.dump(model_data, f, indent=2)
        except Exception as e:
            print(f"Không thể lưu mô hình: {e}")
    
    def load_model(self):
        """Tải mô hình học máy nếu có"""
        if not os.path.exists(LEARNING_MODEL_FILE):
            return
        
        try:
            with open(LEARNING_MODEL_FILE, 'r') as f:
                model_data = json.load(f)
                
                # Cập nhật trọng số
                if 'weights' in model_data:
                    self.weights.update(model_data['weights'])
                
                # Cập nhật bảng Q
                if 'q_table' in model_data:
                    for state, actions in model_data['q_table'].items():
                        for action, value in actions.items():
                            self.q_table[state][action] = value
        except Exception as e:
            print(f"Không thể tải mô hình: {e}")

# Tạo instance mặc định
learning_agent = ReinforcementLearning()

# Hàm đánh giá tích hợp với học máy
def learned_heuristic(data):
    """Hàm đánh giá sử dụng trọng số học được từ reinforcement learning"""
    ai_score = data.aiScore
    player_score = data.playerScore
    ai_stones = sum(data.square[1:6])
    player_stones = sum(data.square[7:12])
    
    # Đánh giá hiệu số quân Quan
    mandarin_diff = data.square[0] - data.square[6]
    
    # Đếm số ô trống
    player_empty_squares = sum(1 for i in range(7, 12) if data.square[i] == 0)
    ai_empty_squares = sum(1 for i in range(1, 6) if data.square[i] == 0)
    
    # Đánh giá khả năng bắt quân đơn giản
    capture_potential = 0
    for i in range(1, 6) if data.player == 1 else range(7, 12):
        if data.square[i] > 0:
            end_pos = (i + data.square[i]) % 12
            if 0 <= end_pos < 12 and data.square[(end_pos + 1) % 12] == 0 and data.square[(end_pos + 2) % 12] > 0:
                capture_potential += 1
    
    # Đánh giá ô cô lập
    isolation_penalty = 0
    for i in range(1, 6) if data.player == 1 else range(7, 12):
        if data.square[i] > 0:
            left = data.square[(i - 1) % 12]
            right = data.square[(i + 1) % 12]
            if left == 0 and right == 0:
                isolation_penalty += 1
    
    # Tính giá trị dựa trên trọng số học được
    value = (
        learning_agent.weights['score'] * (ai_score - player_score) +
        learning_agent.weights['resources'] * (ai_stones - player_stones) +
        learning_agent.weights['mandarin'] * mandarin_diff +
        learning_agent.weights['empty_squares'] * (player_empty_squares - ai_empty_squares) +
        learning_agent.weights['capture_potential'] * capture_potential -
        learning_agent.weights['isolation'] * isolation_penalty
    )
    
    return value if data.player == 1 else -value

# Hàm tích hợp với mainAI.py để ghi lại nước đi
def record_move_and_learn(data, pos, direction, score, game_over=False, winner=None):
    """Ghi lại nước đi và học nếu trò chơi kết thúc"""
    learning_agent.record_move(data, pos, direction, score)
    
    if game_over and winner is not None:
        learning_agent.learn_from_game(winner)
        return True
    
    return False
