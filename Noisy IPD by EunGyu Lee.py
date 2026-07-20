import random
random.seed(67)
import math
# Prisoner's Dilemma payoff matrix
R = 3
P = 1
S = 0
T = 5
PAYOFF = {
    ('C', 'C'): (R, R),
    ('C', 'D'): (S, T),
    ('D', 'C'): (T, S),
    ('D', 'D'): (P, P),
}

# Base strategy class
class Strategy:
    def __init__(self):
        self.history = []
        self.opponent_history = []

    def reset(self):
        self.history = []
        self.opponent_history = []
    def move(self):
        raise NotImplementedError

    def record(self, my_move, opponent_move):
        self.history.append(my_move)
        self.opponent_history.append(opponent_move)

# Define 15 original strategies
class Downing(Strategy):
    def __init__(self):
        super().__init__()
        self.opponent_coop_after_C = 0.5
        self.opponent_coop_after_D = 0.5
        self.reward = R
        self.punish = P
        self.sucker = S
        self.tempt = T

    def reset(self):
        super().reset()
        self.opponent_coop_after_C = 0
        self.opponent_coop_after_D = 0

    def move(self):
        round_num = len(self.history) + 1

        if round_num == 1:
            return 'D'
        if round_num == 2:
            if self.opponent_history and self.opponent_history[-1] == 'C':
                self.opponent_coop_after_C += 1
            return 'D'

        if len(self.history) >= 2:
            if self.history[-2] == 'C' and self.opponent_history[-1] == 'C':
                self.opponent_coop_after_C += 1
            if self.history[-2] == 'D' and self.opponent_history[-1] == 'C':
                self.opponent_coop_after_D += 1

        total_C = self.history.count('C') + 1  
        total_D = max(self.history.count('D'), 2)  

        alpha = self.opponent_coop_after_C / total_C
        beta = self.opponent_coop_after_D / total_D

        expected_C = alpha * self.reward + (1 - alpha) * self.sucker
        expected_D = beta * self.tempt + (1 - beta) * self.punish

        if expected_C > expected_D:
            return 'C'
        if expected_C < expected_D:
            return 'D'
        return 'D' if self.history[-1] == 'C' else 'C'
class Joss(Strategy):
    def move(self):
        if not self.opponent_history:
            return 'C'
        elif self.opponent_history[-1] == 'C':
            Jossnum = random.randint(1, 10)
            if Jossnum == 5:
                return 'D'
            else:
                return 'C'
        elif self.opponent_history[-1] == 'D':
            return 'D'
class Davis(Strategy):
    def __init__(self):
        super().__init__()
        self.grudge = False
    def move(self):
        if len(self.history) < 11:
            return 'C'
        else:
            if not self.grudge and 'D' in self.opponent_history:
                self.grudge = True
            return 'D' if self.grudge else 'C'

class TitForTat(Strategy):
    def move(self):
        if not self.opponent_history:
            return 'C'
        return self.opponent_history[-1]

class RandomStrategy(Strategy):
    def move(self):
        return random.choice(['C', 'D'])

class Grudger(Strategy):
    def __init__(self):
        super().__init__()
        self.grudging = False

    def move(self):
        if 'D' in self.opponent_history:
            self.grudging = True
        return 'D' if self.grudging else 'C'
class Nydegger(Strategy):
    def move(self):
        NydeggerNum = 0
        NydeggerDefect = [1,6,7,17,22,23,26,29,30,31,33,38,39,45,49,54,55,58,61]
        if len(self.history)<3:
            if len(self.history) == 2:
                if self.history[0] == 'C' and self.opponent_history[0] == 'D':
                    if self.history[1] == 'D' and self.opponent_history[1] == 'C':
                        return 'D'
            elif not self.opponent_history:
                return 'C'
            return self.opponent_history[-1]
        elif len(self.history)>=3:
            if self.opponent_history[-3] == 'D':
                NydeggerNum = NydeggerNum + 32
            if self.history[-3] == 'D':
                NydeggerNum = NydeggerNum + 16
            if self.opponent_history[-2] == 'D':
                NydeggerNum = NydeggerNum + 8
            if self.history[-2] == 'D':
                NydeggerNum = NydeggerNum + 4
            if self.opponent_history[-1] == 'D':
                NydeggerNum = NydeggerNum + 2
            if self.history[-1] == 'D':
                NydeggerNum = NydeggerNum + 1
            for i in range(len(NydeggerDefect)):
                if NydeggerNum == NydeggerDefect[i]:
                    return 'D'
            return 'C'
class Grofman(Strategy):
    def move(self):
        if not self.opponent_history or self.history[-1] == self.opponent_history[-1]:
            return 'C'
        elif self.history[-1] != self.opponent_history[-1]:
            GrofmanNum = random.randint(1,7)
            if GrofmanNum == 1 or GrofmanNum == 2:
                return 'C'
            else:
                return 'D'
class Feld(Strategy):
    def __init__(self):
        super().__init__()
        self.coop_prob = 1.0

    def reset(self):
        super().reset()
        self.coop_prob = 1.0

    def move(self):
        if not self.opponent_history:
            return 'C'
        if self.opponent_history[-1] == 'D':
            return 'D'
        elif random.random() < self.coop_prob:
            self.coop_prob -= 0.0025
            return 'C'
        else:
            self.coop_prob -= 0.0025
            return 'D'

        

class Shubik(Strategy):
    def __init__(self):
        super().__init__()
        self.defect_counter = 0
        self.defect_left = 0
        self.round_count = 0

    def reset(self):
        super().reset()
        self.defect_counter = 0
        self.defect_left = 0
        self.round_count = 0

    def move(self):
        self.round_count += 1
        if not self.opponent_history:
            return 'C'
        if self.opponent_history[-1] == 'D' and self.defect_left == 0:
            self.defect_counter += 1
            self.defect_left = self.defect_counter
        if self.defect_left != 0:
            self.defect_left -= 1
            return 'D'
        return 'C'

class Tullock(Strategy):
    def __init__(self):
        super().__init__()
        self.CooperationCounter = 0
    def reset(self):
        super().reset()
        self.CooperationCounter = 0
    def move(self):
        self.CooperationCounter = 0
        if len(self.history) < 12:
            return 'C'
        else:
            for i in range(10):
                if self.opponent_history[(-1-i)] == 'C':
                    self.CooperationCounter += 1
            if random.randint(1,10) <=(self.CooperationCounter -1):
                return 'C'
            return 'D'
class Graaskamp(Strategy):
    def __init__(self):
        super().__init__()
        self.tft = False
        self.clone = False
        self.randomstrategy = False
        self.nomatch = False
        self.defect_round = 0

    def reset(self):
        super().reset()
        self.tft = False
        self.clone = False
        self.randomstrategy = False
        self.nomatch = False
        self.defect_round = 0
    def move(self):
        graascoop = 0
        graasdef = 0
        if len(self.history) < 50 or 51 <= len(self.history) <= 55:
            return 'C' if not self.opponent_history else self.opponent_history[-1]
        if len(self.history) == 50:
            for i in range(len(self.opponent_history)):
                if self.opponent_history[i] == 'C':
                    graascoop += 1
                if self.opponent_history[i] == 'D':
                    graasdef += 1
            graaschi = (((graascoop - 25)**2)/25) + (((graasdef - 25)**2)/25)
            if graaschi < 3.841:
                self.randomstrategy = True
            tftcheck = sum(
                1 for i in range(49)
                if self.opponent_history[i + 1] == self.history[i]
            )
            if tftcheck >= 45: 
                self.tft = True
            elif self.opponent_history == self.history and self.opponent_history[-1] == 'D':
                self.clone = True
            return 'D'
        
        if self.tft or self.clone:
            return self.opponent_history[-1]
        elif self.randomstrategy:
            return 'D'  
        elif self.nomatch and self.defect_round != 0:
            self.defect_round -= 1
            return 'C'
        elif self.defect_round == 0:
            self.nomatch = True
            self.defect_round = random.randint(5, 15)
            return 'D'
        else:
            return 'C'
class TidemanandChieruzzi(Strategy):
    def __init__(self):
        super().__init__()
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0
        self.current_score = 0
        self.opponent_score = 0
        self.last_fresh_start = 0
        self.fresh_start = False
        self.remembered_number_of_opponent_defections = 0
        self.randomst = False
        self.randomset = []
    def reset(self):
        super().reset()
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0
        self.current_score = 0
        self.opponent_score = 0
        self.last_fresh_start = 0
        self.fresh_start = False
        self.remembered_number_of_opponent_defections = 0
        self.randomst = False
        self.randomset = []
    def move(self):
        while len(self.randomset) < len(self.opponent_history):
            self.randomset.append(random.choice(['C','D']))
        self.random_defections = 0
        self.opponent_defections = 0
        self.last_fresh_start += 1
        for j in range(len(self.opponent_history)):
            if self.opponent_history[j] == 'D':
                self.opponent_defections += 1
            if self.randomset[j] == 'D':
                self.random_defections += 1
        if self.random_defections - 3 <self.opponent_defections< self.random_defections + 3:
            self.randomst = True
        elif self.random_defections - 3 >self.opponent_defections or self.opponent_defections> self.random_defections + 3:
            self.randomst = False
        if  len(self.history) != 0 and self.history[-1] == 'C' and self.opponent_history[-1] == 'C':
            self.current_score += R
            self.opponent_score += R
        if  len(self.history) != 0 and self.history[-1] == 'C' and self.opponent_history[-1] == 'D':
            self.current_score += S
            self.opponent_score += T
            self.remembered_number_of_opponent_defections += 1
        if  len(self.history) != 0 and self.history[-1] == 'D' and self.opponent_history[-1] == 'C':
            self.current_score += T
            self.opponent_score += S
        if  len(self.history) != 0 and self.history[-1] == 'D' and self.opponent_history[-1] == 'D':
            self.current_score += P
            self.opponent_score += P
            self.remembered_number_of_opponent_defections += 1
        if len(self.opponent_history) !=0 and self.is_retaliating == False and self.opponent_history[-1] == 'D':
            self.retaliation_length += 1
            self.retaliation_remaining = self.retaliation_length
        if self.retaliation_remaining !=0:
            self.is_retaliating = True
        elif self.retaliation_remaining == 0:
            self.is_retaliating = False
        if self.current_score - self.opponent_score > 10 and self.opponent_history[-1] == 'C' and self.last_fresh_start > 20 and len(self.history) < 190 and self.randomst == False:
            self.fresh_start = True
        if self.fresh_start == True:
            self.is_retaliating = False
            self.retaliation_length = 0
            self.retaliation_remaining = 0
            self.last_fresh_start = 0
            self.fresh_start = False
            self.remembered_number_of_opponent_defections = 0
            self.randomst = False
            return 'C'
        if self.is_retaliating == False:
            if not self.opponent_history:
                return 'C'
            return self.opponent_history[-1]
        elif self.is_retaliating == True:
            self.retaliation_remaining -= 1
            return 'D'
class Anonymous(Strategy):
    def __init__(self):
        super().__init__()
    def reset(self):
        super().reset()
        anonnum = 0
    def move(self):
        anonnum = random.uniform(0.3,0.7)
        if random.random() < anonnum:
            return 'C'
        else:
            return 'D'
class SteinandRapoport(Strategy):
    def __init__(self):
        super().__init__()

    def reset(self):
        super().reset()

    def move(self):
        if len(self.history) <= 4:
            return 'C'
        if len(self.history) >= 199:
            return 'D'

        if (len(self.history) + 1) % 15 == 0:
            total_moves = len(self.opponent_history)
            if total_moves == 0:
                return 'C'  

            coop_count = self.opponent_history.count('C')
            defect_count = total_moves - coop_count
            expected = total_moves / 2

            chi_sq = ((coop_count - expected) ** 2) / expected + ((defect_count - expected) ** 2) / expected

            if chi_sq < 3.841:
                return 'D'
            else:
                return self.opponent_history[-1]
        else:
            return self.opponent_history[-1]
# Tournament manager
NOISE_LEVEL = 0.05

def noisy_move(move):
    if random.random() < NOISE_LEVEL:
        return 'D' if move == 'C' else 'C'
    return move

def play_round(p1, p2, rounds=200):
    p1.reset()
    p2.reset()
    score1 = 0
    score2 = 0
    for _ in range(rounds):
        m1 = p1.move()
        m2 = p2.move()

        # Apply noise here:
        m1_noisy = noisy_move(m1)
        m2_noisy = noisy_move(m2)

        s1, s2 = PAYOFF[(m1_noisy, m2_noisy)]
        score1 += s1
        score2 += s2
        p1.record(m1_noisy, m2_noisy)
        p2.record(m2_noisy, m1_noisy)

    return score1, score2

def run_tournament():
    strategy_classes = [
        (Joss, "Joss"),
        (Davis, "Davis"),
        (TitForTat, "TitForTat"),
        (RandomStrategy, "RandomStrategy"),
        (Grudger, "Grudger"),
        (Nydegger, "Nydegger"),
        (Grofman, "Grofman"),
        (Feld, "Feld"),
        (Shubik, "Shubik"),
        (Tullock, "Tullock"),
        (Graaskamp, "Graaskamp"),
        (TidemanandChieruzzi, "TidemanandChieruzzi"),
        (Anonymous, "Anonymous"),
        (SteinandRapoport, "SteinandRapoport"),
        (Downing, "Downing"),
    ]

    n = len(strategy_classes)
    scores = [0.0] * n
    strategies = [cls() for cls, _ in strategy_classes]
    names = [name for _, name in strategy_classes]

    for i in range(n):
        for j in range(i, n):
            s1 = strategies[i]
            s2 = strategies[j]
            score1, score2 = play_round(s1, s2)
            scores[i] += score1
            scores[j] += score2 

    return names, scores


def run_multiple_tournaments(num_runs=10):
    names = None
    total_scores = None

    for _ in range(num_runs):
        n, scores = run_tournament()
        if total_scores is None:
            names = n
            total_scores = [0.0] * len(scores)
        for i in range(len(scores)):
            total_scores[i] += scores[i]

    avg_scores = [s / num_runs for s in total_scores]
    ranked = list(zip(names, avg_scores))
    ranked.sort(key=lambda x: x[1], reverse=True)

    print(f"\nAverage Axelrod Tournament Rankings (over {num_runs} runs):")
    for rank, (name, score) in enumerate(ranked, start=1):
        print(f"{rank:2d}. {name:25} - {round(score/15)}")  
    return ranked


# Run averaged tournament
run_multiple_tournaments(num_runs=10)
