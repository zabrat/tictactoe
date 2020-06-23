import re, random

class game:
  
    def __init__(self):
        self.menu_loop()

    def game_map(self, comb):
        print("---------")
        print("|",comb[0],comb[1],comb[2],"|")
        print("|",comb[3],comb[4],comb[5],"|")
        print("|",comb[6],comb[7],comb[8],"|")
        print("---------")

    def user(self):
        while True:
            move = input("Enter the coordinates: ")
            if re.match(r"[4-9] [1-9]|[1-9] [4-9]|[4-9] [4-9]", move):
                print("Coordinates should be from 1 to 3!")
            elif move not in self.main_coordinates:
                print("You should enter numbers!")
            elif move not in self.empty_coordinates and move in self.main_coordinates:
                print("This cell is occupied! Choose another one!")
            else:
                if self.next_move() == "X":
                    self.occupied_x.add(move)
                else:
                    self.occupied_o.add(move)
                self.start_comb[self.main_coordinates.index(move)] = self.next_move()
                self.empty_coordinates.remove(move)
                self.game_map(self.start_comb)
                break
            
    def easy(self):
        print('Making move level "easy"')
        bot_move = random.choice(self.empty_coordinates)
        if self.next_move() == "X":
            self.occupied_x.add(bot_move)
        else:
            self.occupied_o.add(bot_move)
        self.start_comb[self.main_coordinates.index(bot_move)] = self.next_move()
        self.empty_coordinates.remove(bot_move)
        self.game_map(self.start_comb)

    def check_positions(self, set1, set2):
        for i in self.win_comb:
            if self.next_move() == "X":
                a = i.difference(set1)
                if len(a) == 1 and a.issubset(self.empty_coordinates):
                    bot_move = a.pop()
                    return bot_move
            else:
                b = i.difference(set2)
                if len(b) == 1 and b.issubset(self.empty_coordinates):
                    bot_move = b.pop()
                    return bot_move
        
    def medium(self):
        print('Making move level "medium"')
        attack_move = self.check_positions(self.occupied_x, self.occupied_o)
        defence_move = self.check_positions(self.occupied_o, self.occupied_x)
        if attack_move:
            bot_move = attack_move
        elif defence_move:
            bot_move = defence_move
        else:
            bot_move = random.choice(self.empty_coordinates)
        if self.next_move() == "X":
            self.occupied_x.add(bot_move)
        else:
            self.occupied_o.add(bot_move)
        self.start_comb[self.main_coordinates.index(bot_move)] = self.next_move()
        self.empty_coordinates.remove(bot_move)
        self.game_map(self.start_comb)

    def minimax(self, empty_coordinates, occupied_x, occupied_o, let , st_let = None, c = 0):                
        for i in self.win_comb:
            if i.issubset(occupied_x) and st_let == "X":
                return 1
            elif i.issubset(occupied_o) and st_let == "O":
                return 1
            elif i.issubset(occupied_o):
                return -1
            elif i.issubset(occupied_x):
                return -1
        if len(empty_coordinates) == 0:
             return 0
        moves = {}
        empty_coordinates1 = empty_coordinates.copy()
        for i in empty_coordinates:
            if let == "X":
                occupied_x.add(i)
                empty_coordinates1.remove(i)
                moves[i] = self.minimax(empty_coordinates1, occupied_x, occupied_o, "O", st_let, c = 1)
                occupied_x.remove(i)
                empty_coordinates1.append(i)
            else:
                occupied_o.add(i)
                empty_coordinates1.remove(i)
                moves[i] = self.minimax(empty_coordinates1, occupied_x, occupied_o, "X", st_let, c = 1)
                occupied_o.remove(i)
                empty_coordinates1.append(i)
        maxim = -2
        if c == 0:
            for key, value in moves.items():
                if maxim < value:
                	maxim = value
                	maxim_key = key
            return maxim_key
        if let == st_let:
            return max(moves.values())
        else:
            return min(moves.values())
        
    def hard(self):
        print('Making move level "hard"')
        empty_coordinates1 = self.empty_coordinates.copy()
        occupied_x1 = self.occupied_x.copy()
        occupied_o1 = self.occupied_o.copy()
        next_move = self.next_move()
        bot_move = self.minimax(empty_coordinates1, occupied_x1, occupied_o1, next_move, st_let = next_move)
        if next_move == "X":
            self.occupied_x.add(bot_move)
        else:
            self.occupied_o.add(bot_move)
        self.start_comb[self.main_coordinates.index(bot_move)] = next_move
        self.empty_coordinates.remove(bot_move)
        self.game_map(self.start_comb)

    def win(self):
        for i in self.win_comb:
            if i.issubset(self.occupied_x):
                print("X wins")
                self.checker = 1
            if i.issubset(self.occupied_o):
                print("O wins")
                self.checker = 1
    
    def menu_loop(self):
        while True:
            self.start_comb = [" " for i in range(9)]
            self.main_coordinates = ["1 3","2 3","3 3","1 2","2 2","3 2","1 1","2 1","3 1"]
            self.empty_coordinates = self.main_coordinates.copy()
            self.checker = 0
            self.occupied_x = set()
            self.occupied_o = set()
            self.win_comb = [{"1 3","2 3","3 3"},
                             {"1 2","2 2","3 2"},
                             {"1 1","2 1","3 1"},
                             {"1 3","1 2","1 1"},
                             {"2 3","2 2","2 1"},
                             {"3 3","3 2","3 1"},
                             {"1 3","2 2","3 1"},
                             {"3 3","2 2","1 1"}]
            self.start = input("Input your command: ")
            if re.match(r"start (user|easy|medium|hard) (user|easy|medium|hard)", self.start):
                self.game_map(self.start_comb)
                self.game_loop() 
            elif self.start == "exit":
                break
            else:
                print("Bad parametres!")

    def game_loop(self):
        while True:
            if self.start.split()[1] == "user":
                self.user()
            elif self.start.split()[1] == "medium":
                self.medium()
            elif self.start.split()[1] == "hard":
                self.hard()  
            else:
                self.easy()
            self.win()
            if self.checker:
                break 
            if len(self.empty_coordinates) == 0:
                print("Draw")
                break
            if self.start.split()[2] == "user":
                self.user()
            elif self.start.split()[2] == "medium":
                self.medium()
            elif self.start.split()[2] == "hard":
                self.hard() 
            else:
                self.easy()
            self.win()
            if self.checker:
                break 

    def next_move(self):
        if self.start_comb.count("X") == self.start_comb.count("O"):
            return "X"
        else:
            return "O"
a = game()