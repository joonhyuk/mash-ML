import random

class RPSCharacter:
    def __init__(self, name:str = None) -> None:
        self.action_list = ['Q', 'R', 'P', 'S']
        self.name = self.set_name(name)
        self.reset()
    
    def reset(self):
        self.wins = 0
        self.win_streak = 0
        self.score = 0
        self.last_action = None
    
    def set_name(self, name:str = None) -> str:
        if name is None: name = f'Player{id(self)}'
        return name
    
    def get_action_result(self, id:int) -> int:
        return id
    
    def action(self):
        pass
    
    def win(self):
        self.wins += 1
        self.win_streak += 1
        self.score += 1
    
    def lose(self):
        self.win_streak = 0
        self.score -= 1
    
    def draw(self):
        self.win_streak = 0

class SimplePC(RPSCharacter):
    def set_name(self, name: str = None) -> str:
        if name is None: name = input('Input player name : ')
        return name
        
    def action(self):
        self.last_action = None
        action = None
        while action not in self.action_list:
            action = input(f'{self.name} -> [Rr]ock, [Pp]aper, [Ss]cissor, [Qq]uit : ').capitalize()
        self.last_action = self.get_action_result(self.action_list.index(action))

class SimpleNPC(RPSCharacter):
    def action(self):
        self.last_action = self.get_action_result(random.randint(1, 3))

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
        self.p1.last_action = None
        self.p2.last_action = None
    
    def result(self, game_result:int):
        winner, loser = None, None
        if game_result not in (-1, 0, 1):
            return False
        
        if game_result == -1:
            winner = self.p1
            loser = self.p2            
        if game_result == 1:
            winner = self.p2
            loser = self.p1
        
        
        if game_result == 0:
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
        print(f'{winner.name} wins!{win_streak}')
        formatter = "{:<21} {:>8} {:>8} {:>8}"
        print(formatter.format('Player','Action','Wins','Score'))
        print(formatter.format(winner.name, winner.action_list[winner.last_action], winner.wins, winner.score))
        print(formatter.format(loser.name, loser.action_list[loser.last_action], loser.wins, loser.score))
        print('')
    def run(self):
        while self.running:
            self.init_session()
            self.p1.action()
            self.p2.action()
            
            if self.p1.last_action * self.p2.last_action == 0:
                ''' if quit '''
                self.running = False
                break
            
            game_result = self.p2.last_action - self.p1.last_action
            ''' -1 : p1 win, 0 : draw, 1 : p2 win
            '''
            if game_result == 2: game_result = -1
            if game_result == -2: game_result = 1
            
            self.result(game_result)
            self.roundnum += 1
            if self.roundnum > 16384:
                self.running = False

if __name__ == '__main__':
    game = RPSGame2P(SimplePC, SimpleNPC)
    game.run()