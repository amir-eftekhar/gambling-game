import tkinter as tk
import random

class BetCalculator:
    def __init__(self, bet_amount, remaining_squares):
        self.bet_amount = bet_amount
        self.remaining_squares = remaining_squares

    def calculate_return(self):
        return self.bet_amount // self.remaining_squares
class MineGame:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x800")
        self.master.configure(bg='black')
        self.non_betting_balance = 0
        self.bet_amount = 0
        self.score = 0
        self.bomb_location = random.randint(1, 16)
        self.remaining_squares = 15
        self.first_run = True
        self.money_goal = 0
        self.balance_set = False
        self.goal_set = False

        self.welcome_screen()

    def welcome_screen(self):
        self.welcome_label = tk.Label(self.master, text="Welcome to the Mine Game!", bg='black', fg='white')
        self.welcome_label.grid(row=0, column=0, columnspan=4)

        self.bet_label = tk.Label(self.master, text="Enter your bet amount:", bg='black', fg='white')
        self.bet_label.grid(row=1, column=0, columnspan=4)

        self.bet_entry = tk.Entry(self.master)
        self.bet_entry.grid(row=2, column=0, columnspan=4)

        if self.first_run:
            self.add_balance_button = tk.Button(self.master, text="Add to Non-Betting Balance", command=self.add_balance)
            self.add_balance_button.grid(row=3, column=0, columnspan=4)

            self.goal_label = tk.Label(self.master, text="Enter your money goal:", bg='black', fg='white')
            self.goal_label.grid(row=4, column=0, columnspan=4)

            self.goal_entry = tk.Entry(self.master)
            self.goal_entry.grid(row=5, column=0, columnspan=4)

            self.set_goal_button = tk.Button(self.master, text="Set Goal", command=self.set_goal)
            self.set_goal_button.grid(row=6, column=0, columnspan=4)

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_button.grid(row=7, column=0, columnspan=4)

        self.balance_display = tk.Label(self.master, text="Non-Betting Balance: " + str(self.non_betting_balance), bg='black', fg='white')
        self.balance_display.grid(row=8, column=0, columnspan=4)

        self.bet_display = tk.Label(self.master, text="Bet Amount: " + str(self.bet_amount), bg='black', fg='white')
        self.bet_display.grid(row=9, column=0, columnspan=4)

        self.goal_display = tk.Label(self.master, text="Money Goal: " + str(self.money_goal), bg='black', fg='white')
        self.goal_display.grid(row=10, column=0, columnspan=4)

    def add_balance(self):
        if not self.balance_set:
            self.non_betting_balance += int(self.bet_entry.get())
            self.bet_entry.delete(0, 'end')
            self.balance_display.config(text="Non-Betting Balance: " + str(self.non_betting_balance))
            self.balance_set = True

    def set_goal(self):
        if not self.goal_set:
            self.money_goal = int(self.goal_entry.get())
            self.goal_entry.delete(0, 'end')
            self.goal_display.config(text="Money Goal: " + str(self.money_goal))
            self.goal_set = True

    def start_game(self):
        self.bet_amount = int(self.bet_entry.get())
        self.non_betting_balance -= self.bet_amount
        self.remaining_squares = 16
        self.bet_calculator = BetCalculator(self.bet_amount, self.remaining_squares)
        
        self.welcome_label.grid_forget()
        self.bet_label.grid_forget()
        self.bet_entry.grid_forget()
        if self.first_run:
            self.add_balance_button.grid_forget()
            self.goal_label.grid_forget()
            self.goal_entry.grid_forget()
            self.set_goal_button.grid_forget()
        self.start_button.grid_forget()
        self.balance_display.grid_forget()
        self.bet_display.grid_forget()
        self.goal_display.grid_forget()

        self.buttons = []
        for i in range(1, 17):
            button = tk.Button(self.master, text=str(i), command=lambda i=i: self.click_square(i), height=3, width=7)
            button.grid(row=(i-1)//4, column=(i-1)%4)
            self.buttons.append(button)

        self.stop_button = tk.Button(self.master, text="Stop Game", command=self.stop_game)
        self.stop_button.grid(row=4, column=0, columnspan=4)

        self.bet_display = tk.Label(self.master, text="Bet Amount: " + str(self.bet_amount), bg='black', fg='white')
        self.bet_display.grid(row=5, column=0, columnspan=4)

        self.balance_display = tk.Label(self.master, text="Non-Betting Balance: " + str(self.non_betting_balance), bg='black', fg='white')
        self.balance_display.grid(row=6, column=0, columnspan=4)

        self.goal_display = tk.Label(self.master, text="Money Goal: " + str(self.money_goal), bg='black', fg='white')
        self.goal_display.grid(row=7, column=0, columnspan=4)

    def click_square(self, square):
        if square == self.bomb_location:
            self.bet_amount = 0
            self.bet_display.config(text="Bet Amount: " + str(self.bet_amount))
            self.buttons[square-1].config(text="Bomb", bg='red')
        else:
            self.score += self.bet_calculator.calculate_return()
            self.bet_amount += self.bet_calculator.calculate_return()
            self.remaining_squares -= 1
            self.bet_calculator = BetCalculator(self.bet_amount, self.remaining_squares)
            self.bet_display.config(text="Bet Amount: " + str(self.bet_amount))
            self.buttons[square-1].config(text="Gem", bg='green')

        if self.bet_amount + self.non_betting_balance <= 0:
            self.game_over()
        elif self.bet_amount + self.non_betting_balance >= self.money_goal:
            self.you_win()

    def stop_game(self):
        self.non_betting_balance += self.bet_amount
        self.bet_amount = 0
        self.bomb_location = random.randint(1, 16)
        for button in self.buttons:
            button.grid_forget()
        self.stop_button.grid_forget()
        self.bet_display.grid_forget()
        self.balance_display.grid_forget()
        self.goal_display.grid_forget()
        self.welcome_screen()

    def game_over(self):
        for button in self.buttons:
            button.grid_forget()
        self.stop_button.grid_forget()
        self.bet_display.grid_forget()
        self.balance_display.grid_forget()
        self.goal_display.grid_forget()
        tk.Label(self.master, text="Game Over", bg='black', fg='white', font=("Helvetica", 32)).grid(row=7, column=0, columnspan=4)
        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=8, column=0, columnspan=4)

    def reset_game(self):
        self.reset_button.grid_forget()
        self.non_betting_balance = 0
        self.bet_amount = 0
        self.score = 0
        self.bomb_location = random.randint(1, 16)
        self.remaining_squares = 15
        self.first_run = False
        self.welcome_screen()

    def you_win(self):
        for button in self.buttons:
            button.grid_forget()
        self.stop_button.grid_forget()
        self.bet_display.grid_forget()
        self.balance_display.grid_forget()
        self.goal_display.grid_forget()
        tk.Label(self.master, text="You Win!", bg='black', fg='white', font=("Helvetica", 32)).grid(row=7, column=0, columnspan=4)
        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=8, column=0, columnspan=4)


root = tk.Tk()
game = MineGame(root)
root.mainloop()
