import random
import json
import os

# Set the path for saving the game
SAVE_DIRECTORY = r'C:\Users\loren\gamble_saves'

# Ensure the directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

SAVE_FILE = os.path.join(SAVE_DIRECTORY, 'game_save.json')


# Save the game
def save_game(balance, total_wins, total_losses, loans, loan_rounds, high_score):
    data = {
        "balance": balance,
        "total_wins": total_wins,
        "total_losses": total_losses,
        "loans": loans,
        "loan_rounds": loan_rounds,
        "high_score": high_score
    }
    with open(SAVE_FILE, 'w') as save_file:
        json.dump(data, save_file)
    print(f"Game saved to {SAVE_FILE}!")


# Load the game
def load_game():
    try:
        with open(SAVE_FILE, 'r') as save_file:
            data = json.load(save_file)
        print(f"Game loaded from {SAVE_FILE}!")
        return data["balance"], data["total_wins"], data["total_losses"], data["loans"], data["loan_rounds"], data["high_score"]
    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return 20, 0, 0, 0, 0, 0  # Starting balance, wins, losses, loans, loan_rounds, and high score


# Delete the save file if the player loses
def delete_save_file():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print(f"Game save deleted: {SAVE_FILE}")
    else:
        print("No save file to delete.")


def gamble_game():
    # Load or start a new game
    balance, total_wins, total_losses, loans, loan_rounds, high_score = load_game()

    print("Welcome to the Gambling Game with Loans and Leaderboard!")
    print(f"Your starting balance is £{balance}. Loans taken: £{loans}. High score: £{high_score}")

    # Game loop
    while balance > 0:
        print(f"\nYour current balance is £{balance}.")
        print(f"Loans taken: £{loans}. Loan rounds left: {loan_rounds}")
        print(f"High score: £{high_score}")
        print("1. 50/50 Bet: Win double or lose your bet.")
        print("2. High-Risk Bet: 20% chance to win 5x your bet.")
        print("3. Low-Risk Bet: 90% chance to win 1.1x your bet.")
        print("4. Take a loan (£10, 20% interest).")
        print("5. Repay loan.")
        print("6. Save and Quit.")
        print("7. Quit without saving.")

        # Get user choice
        choice = input("Choose a game (1-7): ")

        if choice == "6":
            # Update high score if applicable
            if balance > high_score:
                high_score = balance
            save_game(balance, total_wins, total_losses, loans, loan_rounds, high_score)
            print(f"Game saved. You left the game with £{balance}. Wins: {total_wins}, Losses: {total_losses}.")
            break

        if choice == "7":
            print(f"You quit without saving. Final balance: £{balance}. Wins: {total_wins}, Losses: {total_losses}.")
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Please select 1-7.")
            continue

        # Take a loan
        if choice == "4":
            if loans > 0:
                print("You already have an outstanding loan. Repay the loan first!")
            else:
                balance += 10
                loans += 12  # 20% interest
                loan_rounds = 5  # You must repay within 5 rounds
                print("You took a loan of £10. You now owe £12.")
            continue

        # Repay loan
        if choice == "5":
            if loans == 0:
                print("You don't have any loans to repay!")
            elif balance < loans:
                print(f"You don’t have enough money to repay the full loan. You need £{loans}.")
            else:
                balance -= loans
                print(f"Loan repaid! You deducted £{loans} from your balance.")
                loans = 0
                loan_rounds = 0
            continue

        # Loan interest penalty
        if loans > 0 and loan_rounds == 0:
            penalty = loans * 0.1  # 10% penalty if loan is not repaid in time
            loans += penalty
            loan_rounds = 5  # Reset repayment period
            print(f"Loan overdue! Interest penalty of £{penalty:.2f} added. New loan balance: £{loans}.")

        # Place a bet
        try:
            bet = float(input("How much do you want to bet?: £"))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if bet <= 0:
            print("You need to bet a positive amount!")
            continue
        if bet > balance:
            print("You cannot bet more than your current balance!")
            continue

        # Bet options logic
        if choice == "1":  # 50/50 bet
            outcome = random.choice(["win", "lose"])
            if outcome == "win":
                balance += bet
                total_wins += 1
                print(f"You won! You gained £{bet}.")
            else:
                balance -= bet
                total_losses += 1
                print(f"You lost £{bet}.")
        
        elif choice == "2":  # High-Risk Bet
            outcome = random.choices(["win", "lose"], weights=[20, 80])[0]
            if outcome == "win":
                balance += bet * 5
                total_wins += 1
                print(f"High-Risk Win! You gained £{bet * 5}.")
            else:
                balance -= bet
                total_losses += 1
                print(f"High-Risk Loss! You lost £{bet}.")
        
        elif choice == "3":  # Low-Risk Bet
            outcome = random.choices(["win", "lose"], weights=[90, 10])[0]
            if outcome == "win":
                balance += bet * 1.1
                total_wins += 1
                print(f"Low-Risk Win! You gained £{bet * 0.1:.2f}.")
            else:
                balance -= bet
                total_losses += 1
                print(f"Low-Risk Loss! You lost £{bet}.")
        
        # Lucky bonus event (rare)
        if random.random() < 0.01:
            bonus = random.randint(1, 20)
            balance += bonus
            print(f"Lucky Bonus! You found an extra £{bonus}.")

        # Update loan repayment countdown
        if loans > 0:
            loan_rounds -= 1
        
        # Update high score
        if balance > high_score:
            high_score = balance

    if balance == 0:
        print(f"You have no money left. Game over! Wins: {total_wins}, Losses: {total_losses}. High score: £{high_score}. You owe £{loans} in loans.")
        delete_save_file()  # Delete the save file if the player loses

# Start the game
if __name__ == "__main__":
    gamble_game()
