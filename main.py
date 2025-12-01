import random
import time
import os

HIGHSCORE_FILE = "highscore.txt"

class Item:
    def __init__(self, name, cost, description, value):
        self.name = name
        self.cost = cost
        self.description = description
        self.value = value # Collateral value

class Business:
    def __init__(self, name, cost, income, description):
        self.name = name
        self.cost = cost
        self.income = income
        self.description = description

class CommentarySystem:
    def __init__(self):
        self.win_streak = 0
        self.loss_streak = 0
        
        self.comments = {
            "win": [
                "The bits align in your favor.",
                "A lucky 1 in a sea of 0s.",
                "Calculated? Or just random noise?",
                "You have pleased the machine spirit.",
                "Binary brilliance.",
                "One step closer to the singularity.",
                "Not bad for a carbon-based lifeform.",
                "Wow, you actually won. I'm shocked.",
                "Did you cheat? Be honest.",
                "A broken clock is right twice a day.",
                "Enjoy it while it lasts, meatbag."
            ],
            "loss": [
                "The void stares back.",
                "Zero sum game, and you are the zero.",
                "Glitch in the matrix?",
                "Your logic is flawed.",
                "404: Luck not found.",
                "Have you tried turning it off and on again?",
                "Entropy increases.",
                "Pathetic. Simply pathetic.",
                "My grandma bets better than you.",
                "Are you even trying?",
                "I'd say 'better luck next time', but I doubt it.",
                "Don't quit your day job."
            ],
            "jackpot": [
                "🚨 SYSTEM OVERLOAD! JACKPOT! 🚨",
                "CRITICAL HIT! THE DATABANKS ARE YOURS!",
                "UNBELIEVABLE! A PERFECT STREAM OF ONES!",
                "YOU BROKE THE ALGORITHM!",
                "MAXIMUM YIELD ACHIEVED!",
                "OKAY, WHO GAVE YOU THE ADMIN CODES?!",
                "I AM LEGITIMATELY IMPRESSED. AND SCARED."
            ],
            "win_streak": [
                "You are on fire! The CPU is sweating.",
                "Impossible probability! Are you hacking?",
                "The algorithm cannot predict you!",
                "Streak detected. Difficulty increasing... just kidding.",
                "You are the One.",
                "Okay, stop it. You're embarrassing me.",
                "Leave some coins for the rest of us!"
            ],
            "loss_streak": [
                "Ouch. The algorithm is ruthless today.",
                "Maybe switch to analog?",
                "System failure imminent. Yours, not mine.",
                "Do you need a tutorial?",
                "Persisting in error is... human.",
                "This is getting painful to watch.",
                "Just give up. It's easier.",
                "I'm starting to feel bad for you. Almost."
            ],
            "double_win": [
                "GREED PAYS OFF!",
                "Fortune favors the bold (and foolish)!",
                "Double trouble for the house!",
                "You maniac! You actually did it!"
            ],
            "double_loss": [
                "Greed is good... until it isn't.",
                "Flew too close to the sun, Icarus.",
                "Easy come, easy go.",
                "Should have walked away."
            ]
        }

    def get_comment(self, result_type):
        if result_type == "win":
            self.win_streak += 1
            self.loss_streak = 0
            if self.win_streak >= 3:
                return random.choice(self.comments["win_streak"])
            return random.choice(self.comments["win"])
        
        elif result_type == "loss":
            self.loss_streak += 1
            self.win_streak = 0
            if self.loss_streak >= 3:
                return random.choice(self.comments["loss_streak"])
            return random.choice(self.comments["loss"])
            
        elif result_type == "jackpot":
            self.win_streak += 1 # Jackpot counts as win
            self.loss_streak = 0
            return random.choice(self.comments["jackpot"])
            
        elif result_type == "double_win":
             return random.choice(self.comments["double_win"])
             
        elif result_type == "double_loss":
             return random.choice(self.comments["double_loss"])
            
        return "..."

class Game:
    def __init__(self):
        self.balance = 100
        self.commentary = CommentarySystem()
        self.round = 0
        self.highscore = self.load_highscore()
        self.achievements = set()
        
        # Economy
        self.inventory = []
        self.businesses = []
        self.loan_balance = 0
        self.collateral_items = [] # Items held by bank
        
        # Shop Inventory
        self.shop_items = [
            Item("Golden Bit", 50, "A shiny souvenir. Worth 40 collateral.", 40),
            Item("Quantum Chip", 200, "Increases processing power. Worth 150 collateral.", 150),
            Item("Neural Implant", 500, "Direct interface. Worth 400 collateral.", 400),
            Item("The Source Code", 1000, "A fragment of the matrix. Worth 800 collateral.", 800)
        ]
        
        # Available Businesses
        self.available_businesses = [
            Business("Bit Mine", 100, 5, "Mining 0s and 1s. Income: 5/round"),
            Business("Server Farm", 300, 20, "Hosting the cloud. Income: 20/round"),
            Business("AI Startup", 1000, 100, "Disrupting the industry. Income: 100/round")
        ]

    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return int(f.read().strip())
            except:
                return 100
        return 100

    def save_highscore(self):
        if self.balance > self.highscore:
            self.highscore = self.balance
            try:
                with open(HIGHSCORE_FILE, "w") as f:
                    f.write(str(self.highscore))
                print(f"\n🏆 NEW HIGH SCORE SAVED: {self.highscore} 🏆")
            except:
                print("Could not save high score.")

    def check_achievements(self):
        new_achievements = []
        if self.balance >= 500 and "High Roller" not in self.achievements:
            self.achievements.add("High Roller")
            new_achievements.append("High Roller (Reach 500 coins)")
        if self.commentary.win_streak >= 5 and "Unstoppable" not in self.achievements:
             self.achievements.add("Unstoppable")
             new_achievements.append("Unstoppable (5 win streak)")
        if self.balance <= 0 and "Bankrupt" not in self.achievements:
             self.achievements.add("Bankrupt")
             new_achievements.append("Bankrupt (Lose everything)")
        if len(self.businesses) >= 1 and "Entrepreneur" not in self.achievements:
            self.achievements.add("Entrepreneur")
            new_achievements.append("Entrepreneur (Buy a business)")
        if self.loan_balance > 0 and "Debtor" not in self.achievements:
            self.achievements.add("Debtor")
            new_achievements.append("Debtor (Take a loan)")
             
        if new_achievements:
            print("\n🌟 ACHIEVEMENTS UNLOCKED! 🌟")
            for ach in new_achievements:
                print(f" - {ach}")

    def visit_shop(self):
        print("\n🛒 --- THE BINARY BAZAAR --- 🛒")
        print(f"Your Balance: {self.balance}")
        for i, item in enumerate(self.shop_items):
            print(f"{i+1}. {item.name} - {item.cost} coins ({item.description})")
        print("0. Exit Shop")
        
        choice = input("Buy item (number): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.shop_items):
                item = self.shop_items[idx]
                if self.balance >= item.cost:
                    self.balance -= item.cost
                    self.inventory.append(item)
                    print(f"✅ Bought {item.name}!")
                else:
                    print("❌ Not enough coins.")
            elif idx == -1:
                return
            else:
                print("❌ Invalid selection.")

    def manage_businesses(self):
        print("\n🏢 --- BUSINESS EMPIRE --- 🏢")
        print(f"Your Balance: {self.balance}")
        print("Owned Businesses:")
        if not self.businesses:
            print(" - None")
        for b in self.businesses:
            print(f" - {b.name} (Income: {b.income}/round)")
            
        print("\nAvailable for Purchase:")
        for i, biz in enumerate(self.available_businesses):
            print(f"{i+1}. {biz.name} - {biz.cost} coins ({biz.description})")
        print("0. Exit")
        
        choice = input("Buy business (number): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.available_businesses):
                biz = self.available_businesses[idx]
                if self.balance >= biz.cost:
                    self.balance -= biz.cost
                    self.businesses.append(biz)
                    print(f"✅ Acquired {biz.name}!")
                else:
                    print("❌ Not enough coins.")
            elif idx == -1:
                return
            else:
                print("❌ Invalid selection.")

    def visit_bank(self):
        print("\n🏦 --- THE DATA BANK --- 🏦")
        print(f"Current Loan: {self.loan_balance}")
        print(f"Collateral Held: {', '.join([i.name for i in self.collateral_items]) if self.collateral_items else 'None'}")
        print("1. Borrow (Requires Collateral)")
        print("2. Repay Loan")
        print("0. Exit")
        
        choice = input("Select: ").strip()
        
        if choice == '1':
            if not self.inventory:
                print("❌ You have no items to use as collateral!")
                return
            
            print("\nSelect item for collateral:")
            for i, item in enumerate(self.inventory):
                print(f"{i+1}. {item.name} (Value: {item.value})")
            
            idx_input = input("Item number: ").strip()
            if idx_input.isdigit():
                idx = int(idx_input) - 1
                if 0 <= idx < len(self.inventory):
                    item = self.inventory.pop(idx)
                    loan_amount = item.value
                    self.loan_balance += loan_amount
                    self.balance += loan_amount
                    self.collateral_items.append(item)
                    print(f"✅ Loan approved! Received {loan_amount} coins. {item.name} held as collateral.")
                else:
                    print("❌ Invalid item.")
                    
        elif choice == '2':
            if self.loan_balance == 0:
                print("You have no debt.")
                return
            
            amount = input(f"Enter amount to repay (Max {self.loan_balance}): ").strip()
            if amount.isdigit():
                amt = int(amount)
                if amt > self.loan_balance: amt = self.loan_balance
                if amt > self.balance:
                    print("❌ Not enough funds.")
                    return
                
                self.balance -= amt
                self.loan_balance -= amt
                print(f"✅ Repaid {amt} coins.")
                
                if self.loan_balance == 0 and self.collateral_items:
                    print("🎉 Loan cleared! Collateral returned:")
                    for item in self.collateral_items:
                        print(f" - {item.name}")
                        self.inventory.append(item)
                    self.collateral_items = []

    def process_economy(self):
        # Passive Income
        income = sum(b.income for b in self.businesses)
        if income > 0:
            self.balance += income
            print(f"\n💰 Business Income: +{income} coins")
            
        # Loan Interest (10% per round)
        if self.loan_balance > 0:
            interest = int(self.loan_balance * 0.10)
            self.loan_balance += interest
            print(f"📉 Loan Interest: Loan increased by {interest} coins (Total: {self.loan_balance})")
            
            # Default Check (Simple: If loan > 2x collateral value, seize it)
            collateral_value = sum(i.value for i in self.collateral_items)
            if self.loan_balance > collateral_value * 2:
                print("\n🚨 DEFAULT! The bank has seized your collateral!")
                self.collateral_items = []
                self.loan_balance = 0 # Debt wiped but items lost
                # Actually, usually you still owe money, but let's be "nice" and just take items + wipe debt for simplicity
                # Or maybe just take items and debt remains?
                # Let's say: Bank takes items to cover debt. If not enough, debt remains.
                # Simpler: Bank takes items. Debt reset to 0. (Gamey logic)

    def get_bet(self):
        while True:
            try:
                prompt = f"\nBalance: {self.balance} | Place your bet (integer amount, 'all', 'half', or 0 to quit): "
                bet_input = input(prompt).strip().lower()
                
                if bet_input == '0':
                    return 0
                
                if bet_input == 'all':
                    return self.balance
                
                if bet_input == 'half':
                    return self.balance // 2
                
                bet = int(bet_input)
                
                if bet < 0:
                    print("❌ You can't bet negative coins.")
                    continue
                if bet > self.balance:
                    print(f"❌ You only have {self.balance} coins!")
                    continue
                    
                return bet
                
            except ValueError:
                print("❌ Invalid amount. Please enter a whole number (integer), 'all', or 'half'.")
            except KeyboardInterrupt:
                print("\n\nQuitting...")
                return 0

    def double_or_nothing(self, winnings):
        if self.balance <= 0: return # Can't bet if 0
        
        print("\n⚖️  DOUBLE OR NOTHING? ⚖️")
        print(f"Risk your winnings ({winnings}) to win {winnings * 2}?")
        
        while True:
            choice = input("Type 'y' to risk it, 'n' to keep safe: ").strip().lower()
            if choice == 'y':
                print("Flipping the coin of destiny...", end="", flush=True)
                time.sleep(1.0)
                if random.random() < 0.5:
                    print(" WIN! 💰")
                    self.balance += winnings # Add another winnings amount (total 2x winnings added effectively? No wait)
                    # Logic: 
                    # Initial state: Balance = OldBalance + Winnings
                    # Risking Winnings.
                    # If Win: Balance = OldBalance + Winnings + Winnings (Total +2x Winnings)
                    # If Loss: Balance = OldBalance (Total +0 Winnings)
                    # Wait, current self.balance ALREADY includes winnings.
                    # So if we lose, we subtract winnings.
                    # If we win, we add winnings.
                    self.balance += winnings
                    print(f"✅ Doubled! You won an extra {winnings} coins!")
                    print(f"🔮 Oracle: \"{self.commentary.get_comment('double_win')}\"")
                else:
                    print(" LOSS. 💸")
                    self.balance -= winnings
                    print(f"❌ You lost your winnings of {winnings}.")
                    print(f"🔮 Oracle: \"{self.commentary.get_comment('double_loss')}\"")
                return
            elif choice == 'n':
                print("Playing it safe. Wise... or cowardly?")
                return
            else:
                print("Invalid choice. 'y' or 'n'.")

    def play_guess_the_bit(self, bet):
        print("\n--- Guess the Bit ---")
        while True:
            choice_input = input("Choose 0 or 1: ").strip()
            if choice_input in ['0', '1']:
                choice = int(choice_input)
                break
            print("❌ Binary only. Enter 0 or 1.")

        # Jackpot chance (10%)
        is_jackpot = random.random() < 0.10
        multiplier = 5 if is_jackpot else 2
        
        if is_jackpot:
            print("\n🎰🚨 JACKPOT CHANCE! 5x MULTIPLIER! 🚨🎰\n")

        print("Generating bit...", end="", flush=True)
        time.sleep(1.0)
        result = random.randint(0, 1)
        print(f" Result: {result}")

        if choice == result:
            winnings = bet * multiplier
            profit = winnings - bet # Just for display if needed, but we use full winnings
            self.balance += winnings
            print(f"\n✅ You WON {winnings} coins!")
            
            if is_jackpot:
                print(f"🔮 Oracle: \"{self.commentary.get_comment('jackpot')}\"")
            else:
                print(f"🔮 Oracle: \"{self.commentary.get_comment('win')}\"")
                
            self.double_or_nothing(winnings)
            
        else:
            self.balance -= bet
            print(f"\n❌ You lost {bet} coins.")
            print(f"🔮 Oracle: \"{self.commentary.get_comment('loss')}\"")

    def play_bit_flip(self, bet):
        print("\n--- Bit Flip ---")
        print("A bit starts at 0. Will it FLIP to 1 or STAY 0?")
        while True:
            choice_input = input("Choose 'flip' (1) or 'stay' (0): ").strip().lower()
            if choice_input in ['flip', '1']:
                choice = 1
                break
            elif choice_input in ['stay', '0']:
                choice = 0
                break
            print("❌ Enter 'flip' or 'stay'.")

        print("Observing quantum state...", end="", flush=True)
        time.sleep(1.0)
        result = random.randint(0, 1) # 0 = stay, 1 = flip
        result_str = "FLIPPED (1)" if result == 1 else "STAYED (0)"
        print(f" Result: {result_str}")

        if choice == result:
            winnings = bet * 2
            self.balance += winnings
            print(f"\n✅ You WON {winnings} coins!")
            print(f"🔮 Oracle: \"{self.commentary.get_comment('win')}\"")
            self.double_or_nothing(winnings)
        else:
            self.balance -= bet
            print(f"\n❌ You lost {bet} coins.")
            print(f"🔮 Oracle: \"{self.commentary.get_comment('loss')}\"")

    def play_binary_slots(self, bet):
        print("\n--- Binary Slots ---")
        print("Spin for 3 bits. Match all three (000 or 111) to win BIG (10x)!")
        print("Match alternating (101 or 010) to win (3x).")
        input("Press Enter to spin...")

        print("Spinning...", end="", flush=True)
        time.sleep(1.0)
        b1 = random.randint(0, 1)
        b2 = random.randint(0, 1)
        b3 = random.randint(0, 1)
        print(f" [{b1}] [{b2}] [{b3}]")

        if b1 == b2 == b3:
            winnings = bet * 10
            self.balance += winnings
            print(f"\n✅ JACKPOT! You WON {winnings} coins!")
            print(f"🔮 Oracle: \"{self.commentary.get_comment('jackpot')}\"")
            self.double_or_nothing(winnings)
        elif (b1 == 1 and b2 == 0 and b3 == 1) or (b1 == 0 and b2 == 1 and b3 == 0):
             winnings = int(bet * 3)
             self.balance += winnings
             print(f"\n✅ Nice Pattern! You WON {winnings} coins!")
             print(f"🔮 Oracle: \"{self.commentary.get_comment('win')}\"")
             self.double_or_nothing(winnings)
        else:
            self.balance -= bet
            print(f"\n❌ No pattern. You lost {bet} coins.")
            print(f"🔮 Oracle: \"{self.commentary.get_comment('loss')}\"")

    def play_round(self):
        self.round += 1
        self.process_economy()
        
        print(f"\n{'='*50}")
        print(f"Round {self.round} | Balance: {self.balance} | High Score: {self.highscore}")
        if self.loan_balance > 0:
            print(f"⚠️  Outstanding Loan: {self.loan_balance}")
        print('='*50)

        if self.balance <= 0 and not self.inventory and not self.businesses:
            print("\n💀 You are bankrupt. The Oracle claims your soul.")
            self.check_achievements() # Check for bankrupt achievement
            return False

        print("1. Guess the Bit (Classic)")
        print("2. Bit Flip (50/50)")
        print("3. Binary Slots (High Risk, High Reward)")
        print("4. 🛒 Shop")
        print("5. 🏢 Business Empire")
        print("6. 🏦 Bank (Loans)")
        print("0. Quit")
        
        while True:
            choice = input("Select Option: ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '0']:
                break
            print("Invalid selection.")

        if choice == '0':
            return False

        if choice == '4':
            self.visit_shop()
            return True
        elif choice == '5':
            self.manage_businesses()
            return True
        elif choice == '6':
            self.visit_bank()
            return True

        bet = self.get_bet()
        if bet == 0:
            return False

        if choice == '1':
            self.play_guess_the_bit(bet)
        elif choice == '2':
            self.play_bit_flip(bet)
        elif choice == '3':
            self.play_binary_slots(bet)

        self.check_achievements()
        self.save_highscore()
        return True

def main():
    print("\n" + "="*50)
    print("🎮 Welcome to BINARY ORACLE 2.2 🎮")
    print("="*50)
    print("Everything is 0 or 1. Choose wisely.")
    print("="*50 + "\n")
    
    game = Game()
    
    while True:
        if not game.play_round():
            break
    
    print("\n" + "="*50)
    print(f"🎲 Game Over | Final Balance: {game.balance} coins 🎲")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
