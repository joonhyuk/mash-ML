import random
from Dice import Dice

WIN = 1
DRAW = 0
LOSE = -1

QUIT = -1
UNDERFLOW = 0
ROCK = 1
PAPER = 2
SCISSORS = 3
OVERFLOW = 4

MOVES = (ROCK, PAPER, SCISSORS)
COMMANDS = {'Q':QUIT, 'R':ROCK, 'P':PAPER, 'S':SCISSORS}

RANDOM_MOVE = Dice(MOVES)

def check_rnd(rnd:float):
    rnd = min(1, max(0, rnd))
    return random.random < rnd

def get_random_action():
    return RANDOM_MOVE.roll()

def get_win_action(target:int):
    ''' return winning move aginst target move '''
    if target not in MOVES:
        return get_random_action()
    action = target + WIN
    if action == OVERFLOW: action = MOVES[0]
    return action

def get_lose_action(target:int):
    ''' return losing move aginst target move '''
    if target not in MOVES:
        return get_random_action()
    action = target + LOSE
    if action == UNDERFLOW: action = MOVES[-1]
    return action

def get_the_third(target:int, result:int):
    ''' supposed lose, choose the left move '''
    if target not in MOVES:
        return get_random_action()
    if result == WIN:
        return get_win_action(target)
    elif result == LOSE:
        return get_lose_action(target)
    else: return get_random_action()

class RPSCharacter:
    ''' base class of RPS player '''
    def __init__(self, name:str = None) -> None:
        self.action_list = [ROCK, PAPER, SCISSORS]
        self.name = self.set_name(name)
        self.reset()
    
    def reset(self):
        self.wins = 0
        self.win_streak = 0
        self.max_streak = 0
        self.score = 0
        self.last_action = None
        self.last_result = None
    
    def set_name(self, name:str = None) -> str:
        if name is None: name = f'Player{id(self)}'
        return name
    
    def action(self):
        pass
    
    def win(self):
        self.wins += 1
        self.win_streak += 1
        self.max_streak = max(self.max_streak, self.win_streak)
        self.score += 1
        self.last_result = WIN
    
    def lose(self):
        self.win_streak = 0
        self.score -= 1
        self.last_result = LOSE
    
    def draw(self):
        self.win_streak = 0
        self.last_result = DRAW

class NPC(RPSCharacter):
    def reset(self):
        self.action_history = []
        return super().reset()
    
    def action(self):
        if self.last_result is None:
            action = self.action_first_move()
        elif self.last_result == WIN:
            action = self.action_after_win()
        elif self.last_result == DRAW:
            action = self.action_after_draw()
        elif self.last_result == LOSE:
            action = self.action_after_lose()
        self.action_history.append(action)
        self.last_action = action
    
    def action_first_move(self):
        return get_random_action()
    
    def action_after_win(self):
        return get_random_action()
    
    def action_after_draw(self):
        return get_random_action()
    
    def action_after_lose(self):
        return get_random_action()

class HumanLike(NPC):
    def __init__(self, name: str = 'HumanLike') -> None:
        super().__init__(name)
    
    def action_first_move(self):
        if check_rnd(0.7): return ROCK
        return super().action_first_move()

class SimplePC(RPSCharacter):
    def set_name(self, name: str = None) -> str:
        if name is None: name = input('Input player name : ')
        return name
        
    def action(self):
        self.last_action = None
        action = None
        while action not in COMMANDS :
            action = input(f'{self.name} -> [Rr]ock, [Pp]aper, [Ss]cissor, [Qq]uit : ').capitalize()
            # if action == 'Q': exit()
        self.last_action = COMMANDS.get(action)

class Mimic(NPC):
    ''' 상대방이 방금 낸 손을 그대로 따라함 '''
    def __init__(self, name: str = 'Mimic') -> None:
        super().__init__(name)
    
    def action_after_win(self):
        return get_lose_action(self.last_action)
    
    def action_after_draw(self):
        return self.last_action
    
    def action_after_lose(self):
        return get_win_action(self.last_action)

class Tory(NPC):
    ''' 미리 정해진 것만 낸다 '''
    def __init__(self, name: str = 'Tory') -> None:
        super().__init__(name)
        self.my_action = Dice((ROCK, PAPER))
    
    def action(self):
        self.last_action = self.my_action.roll()

class SmartyPants(NPC):
    ''' 머리 좀 써보려 하지만 별 것 아님 '''
    def __init__(self, name: str = 'SmartyPants') -> None:
        super().__init__(name)
    
    def action_after_win(self):
        return get_lose_action(self.last_action)
    
    def action_after_draw(self):
        ''' 지금까지 가장 적게 낸 것을 낸다 '''
        action_count = (self.action_history.count(ROCK), 
                        self.action_history.count(PAPER), 
                        self.action_history.count(SCISSORS))
        return action_count.index(min(action_count)) + 1
    
    def action_after_lose(self):
        return get_lose_action(self.last_action)

class Weirdo(NPC):
    def __init__(self, name: str = 'Weirdo') -> None:
        super().__init__(name)
    
    def action_after_win(self):
        return get_win_action(self.last_action)
    
    def action_after_draw(self):
        ''' 지금까지 가장 많이 낸 것을 낸다 '''
        action_count = (self.action_history.count(ROCK), 
                        self.action_history.count(PAPER), 
                        self.action_history.count(SCISSORS))
        return action_count.index(max(action_count)) + 1
    
    def action_after_lose(self):
        return get_lose_action(self.last_action)
    
class Knucklehead(NPC):
    ''' 싸나이. 무조건 이기는 쪽으로 선택 '''
    def __init__(self, name: str = 'Knucklehead') -> None:
        super().__init__(name)
    
    def action_after_win(self):
        return self.last_action
    
    def action_after_draw(self):
        return get_win_action(self.last_action)
    
    def action_after_lose(self):
        return get_lose_action(self.last_action)

class RPSGame2P:
    def __init__(self, p1:RPSCharacter, p2:RPSCharacter) -> None:
        self.p1:RPSCharacter = p1()
        self.p2:RPSCharacter = p2()
        self.running = True
        self.init_game()
    
    def init_game(self):
        self.roundnum = 1
        self.p1.reset()
        self.p2.reset()
        print(f'RPS Game {self.p1.name} vs. {self.p2.name} start.\r\n')
        self.init_session()
    
    def init_session(self):
        # self.p1.last_action = None
        # self.p2.last_action = None
        pass
    
    def result(self, p1_result:int):
        winner, loser = None, None
        if p1_result not in (WIN, DRAW, LOSE):
            return False
        
        if p1_result == WIN:
            winner = self.p1
            loser = self.p2     
        if p1_result == LOSE:
            winner = self.p2
            loser = self.p1
        
        if p1_result == DRAW:
            self.p1.draw()
            self.p2.draw()
        else:
            winner.win()
            loser.lose()
        
        self.print_result(winner, loser)
        
    def print_result(self, winner:RPSCharacter, loser:RPSCharacter):
        print(f'Round #{self.roundnum} : ', end = '')
        if winner is None:
            print('DRAW\r\n')
            return True
        if winner.win_streak > 1:
            win_streak = f' ({winner.win_streak} straignt wins)'
        else : win_streak = ''
        print(f'{winner.name} wins.{win_streak}')
        self.print_total_stats(winner, loser)
    
    def print_total_stats(self, winner:RPSCharacter, loser:RPSCharacter):
        formatter = "{:<21} {:>8} {:>8} {:>9} {:>8}"
        commands = list(COMMANDS.keys())
        print(formatter.format('Player','Action','Wins', 'MaxStreak', 'Score'))
        print(formatter.format(winner.name, commands[winner.last_action], winner.wins, winner.max_streak, winner.score))
        print(formatter.format(loser.name, commands[loser.last_action], loser.wins, loser.max_streak, loser.score))
        print('')
    
    def run(self):
        while self.running:
            self.init_session()
            self.p1.action()
            self.p2.action()
            
            if self.p1.last_action == QUIT or self.p2.last_action == QUIT:
                ''' if quit '''
                self.running = False
                break
            
            p1_result = self.p1.last_action - self.p2.last_action
            ''' 1 : p1 win, 0 : draw, -1 : p2 win
            '''
            if p1_result == 2: p1_result = -1
            if p1_result == -2: p1_result = 1
            
            self.result(p1_result)
            self.roundnum += 1
            
            if self.roundnum > 16384:
                self.running = False
        
        players = (self.p1, self.p2)
        player_scores = [self.p1.score, self.p2.score]
        winner = players[player_scores.index(max(player_scores))]
        
        if winner == self.p1:
            loser = self.p2
        else: loser = self.p1
        
        print(f'\r\nGame ends : {winner.name} wins !!!')
        self.print_total_stats(winner, loser)

if __name__ == '__main__':
    game = RPSGame2P(NPC, Tory)
    game.run()