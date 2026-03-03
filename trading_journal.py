import json
from pathlib import Path
from tabulate import tabulate
import datetime

BASE_DIR = Path(__file__).resolve().parent
journal = BASE_DIR / "journal.json"
trades = []

def load_trade(journal):
    
    if not journal.exists():
        return []
    try:
        with open(journal, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        return []    
        
def add_trade(trades):
    pair = input("Pair: ").capitalize().strip()

    while True:
        result = input("Result (Win/Loss): ").lower().strip()
        if result and result[0] == "w":
            result = "Win"
            break
        if result and result[0] == "l":
            result = "Loss"
            break
        else:
            print("Enter Win or Loss")

      
    while True:
        try:
            risk = float(input("Risk %: "))
            break
        except ValueError:
            print("Please Enter Number.")  

    while True:
        try:
            Profit_Loss = float(input("Profit/Loss Amount: "))
            break
        except ValueError:
            print("Please Enter Number.")

    if result == "Loss":
        Profit_Loss = -abs(Profit_Loss)
    if result == "Win":
        Profit_Loss = +abs(Profit_Loss)

    emotion = input("Emotion: ").capitalize().strip()
    notes = input("Notes: ").capitalize().strip()

    if trades:
        new_trade_no = max(t["Trade No"] for t in trades) + 1
    else:
        new_trade_no = 1
            
    trades.append({
        "Trade No" : new_trade_no,
        "Date" : str(datetime.date.today().strftime("%d-%m-%Y")),
        "Pair" : pair,
        "Result" : result,
        "Profit/Loss" : Profit_Loss,
        "Risk" : risk,
        "Emotion" : emotion,
        "Notes" : notes
    })

    print("Trade Added Successfully")

def save_trades(trades):
    with open(journal, 'w') as f:
        json.dump(trades, f, indent=4)

def show_trades():
    try:
        with open(journal, 'r', encoding='utf-8') as f:
            content = f.read().strip()

            if not content:
                print("No trades recorded yet.")
                return
            
            data = json.loads(content)

            table = [[t["Trade No"], t["Date"], t["Pair"], t["Result"], f'{t["Risk"]}%', f"{t['Profit/Loss']:+}", t["Emotion"], t["Notes"]] for t in data]

            headers = ["No", "Date", "Pair", "Result", "Risk", "Profit/Loss", "Emotion", "Notes"]

            print(tabulate(table, headers, tablefmt="fancy_grid"))

    except FileNotFoundError:
        print("File Not Found")
    except json.JSONDecodeError as e:
        print("Error reading journal:", e)

def reset_journal():

    while True:
        user = input("Are You Sure? (y/n): ")
        if user == 'y':
            with open (journal, 'w') as f:
                f.write("[]")
                print("Journal has been Reset.")
                break
        else:
            print("Ok!")
            break   

def avg_risk(trades):

    if not trades:
        return 0 
        
    total_risk = 0

    for t in trades:
        total_risk += t["Risk"]

    avg_risk = total_risk / len(trades)

    return avg_risk

def show_summary(trades):

    if not trades:
        print("No Trade to Summarize")
        return
    
    win = 0
    loss = 0
    total_profit = 0
    total_win_amount = 0
    total_loss_amount = 0

    for t in trades:

        if t["Result"].lower() == "win":
            win += 1
            total_win_amount += t["Profit/Loss"]
        elif t["Result"].lower() == "loss":
            loss += 1
            total_loss_amount += abs(t["Profit/Loss"])

        total_profit += t["Profit/Loss"]


    trade = len(trades)

    winrate = win / trade * 100
    lossrate = loss / trade *100


    biggest_win = max(t["Profit/Loss"] for t in trades)
    biggest_loss = min(t["Profit/Loss"] for t in trades)
    avg_risks = avg_risk(trades)
    avg_win = total_win_amount / win if win else 0
    avg_loss = total_loss_amount / loss if loss else 0

    expectancy = (win / trade * avg_win) - (loss / trade *avg_loss)

    print("------------------------------------------")
    print(f"📝 Total Trades = {trade}")
    print(f"✔️ Total Wins = {win}")
    print(f"✖️ Total Loses = {loss}")
    print(f"📈 Winrate = {winrate: .2f}%")
    print(f"📊 Average Win = {avg_win: .2f}")
    print(f"📊 Average Loss = {avg_loss: .2f}")
    print(f"📊 Average Risk = {avg_risks: .2f}%")
    print(f"📊 Total Win: {total_win_amount}")
    print(f"📊 Total Loss: {total_loss_amount}")
    print(f"📊 Bigges Win: {biggest_win}")
    print(f"📊 Biggest Loss: {biggest_loss}")
    print(f"📝 Total Profit = {total_profit: .2f}")
    print(f"⌛ Expectancy per Trade {expectancy: .2f}")
    print("------------------------------------------")

def filtered_trades(trades):

    if not trades:
        print("No Trades to Filter")

    print("'''''''''''''''''''''")
    print("🗓️ Filter By:")
    print("💡 1.Pair")
    print("📉 2.Win/Loss")
    print("📆 3.Date")
    print("💡 4.Exit Filter")
    print("'''''''''''''''''''''")

    filtered = []
    
    while True:
        try:
            choice = int(input("Enter a number: "))
            if choice == 1:
                pair = input("Enter Pair: ").capitalize().strip()
                for t in trades:
                    if t["Pair"] == pair:
                        filtered.append(t)

            elif choice == 2:
                result = input("Enter Win and Loss: ").capitalize().strip()
                for t in trades:
                    if t["Result"][0] == result[0]:
                        filtered.append(t)

            elif choice == 3:
                date = input("Enter the Date(\"%d-%w-%Y\"): ").strip()
                for t in trades:
                    if t["Date"] == date:
                        filtered.append(t)
            
            else:
                print("Invalid Input")
            break
        except ValueError:      
            print("Enter Valid Number.")

    if not filtered:
        print("No Trade found for this filtered")
        return

    table = []
    for i, t in enumerate(filtered, start=1):
        table.append([
            i, t["Date"], t["Pair"], t["Result"], f'{t["Risk"]}%', f"{t['Profit/Loss']:+}", t["Emotion"], t["Notes"]
            ])
        
    headers = ["No", "Date" , "Pair", "Result", "Risk", "Profit/Loss", "Emotion", "Notes"]
        
    print(tabulate(table, headers, tablefmt="fancy_grid"))

def main():

    trades = load_trade(journal)

    while True:
        print("=========================")
        print("✒️ 1.Add Trade")
        print("📜 2.Show Trades")
        print("📁 3.Show Summary")
        print("🔍 4.Filter Trades")
        print("🏳️ 5.Reset Journal")
        print("❌ 6.Exit")
        print("=========================")

        try:
            user = int(input("Enter Number: "))
            if user == 1:
                add_trade(trades)
                save_trades(trades)
            elif user == 2:
                show_trades()
            elif user == 3:
                show_summary(trades)
            elif user == 4:
                filtered_trades(trades)
            elif user == 5:
                reset_journal()    
            else:
                print("Goodbye!")
                break    
        except ValueError:
            print("Please Enter Number.")            
        
main()
