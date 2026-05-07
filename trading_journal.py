from tabulate import tabulate
import datetime
import sqlite3

# Making Connection
def get_connection(db_name):

    # Connecting to Database
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"ERROR: {e}")

# Creating Table
def create_table(connection):

    # Query: Creating Table
    query = """CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY,
        date TEXT,
        pair TEXT,
        position TEXT,
        entry_price REAL,
        exit_price REAL,
        timeframe TEXT,
        result TEXT,
        risk_percent REAL,
        total_rr REAL,
        profit_loss REAL,
        emotion TEXT,
        strategy TEXT,
        rule TEXT,
        Notes TEXT
        )"""
    
    # Execute Query
    try:
        with connection:
            connection.execute(query)
    except Exception as e:
        print(f"ERROR: {e}")

# Take Trade and give clean Data
def add_trade():

    date = input("Date: ").strip()
    pair = input("Pair: ").capitalize().strip()

    # Position
    while True:
        position = input("Position (Long/Short): ").lower().strip()

        if position and position[0] == "l":
            position = "Long"
            break
        elif position and position[0] == "s":
            position = "Short"
            break
        else:
            print("Enter Long or Short")

    # Prices
    while True:
        try:
            entry_price = float(input("Entry Price: "))
            exit_price = float(input("Exit Price: "))
            break
        except ValueError:
            print("Enter valid numbers")

    # Timeframe
    while True:
        try:
            timeframe = int(input("Timeframe: "))
            break
        except ValueError:
            print("Enter a number")

    # Result
    while True:
        result = input("Result (Win/Loss): ").lower().strip()

        if result and result[0] == "w":
            result = "Win"
            break
        elif result and result[0] == "l":
            result = "Loss"
            break
        else:
            print("Enter Win or Loss")

    # Risk + RR
    while True:
        try:
            risk_percent = float(input("Risk %: "))
            total_rr = float(input("RR: "))
            break
        except ValueError:
            print("Enter valid numbers")

    # PROFIT/LOSS 
    while True:
        try:
            profit_loss = float(input("Profit/Loss: "))
            break
        except ValueError:
            print("Enter valid number")

    if result == "Loss":
        profit_loss = -abs(profit_loss)
    else:
        profit_loss = abs(profit_loss)

    # Extra Data
    emotion = input("Emotion: ").capitalize().strip()
    strategy = input("Strategy (Breakout, Reversal, Continuation, Ranging): ").capitalize().strip()

    # Rule
    while True:
        rule = input("Followed plan? (y/n): ").lower().strip()

        if rule and rule[0] == "y":
            rule = "Yes"
            break
        elif rule and rule[0] == "n":
            rule = "No"
            break
        else:
            print("Enter y or n")

    notes = input("Notes: ").capitalize().strip()

    # Final Clean Data
    trade_data = {
        "date": date,
        "pair": pair,
        "position": position,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "timeframe": timeframe,
        "result": result,
        "risk_percent": risk_percent,
        "total_rr": total_rr,
        "profit_loss": profit_loss,
        "emotion": emotion,
        "strategy": strategy,
        "rule": rule,
        "notes": notes
    }

    return trade_data

# Insert Table
def insert_trade(connection, trade):

    # Query: Values To Table
    query = """
    INSERT INTO trades (
        date,
        pair,
        position,
        entry_price,
        exit_price,
        timeframe,
        result,
        risk_percent,
        total_rr,
        profit_loss,
        emotion,
        strategy,
        rule,
        notes
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    # Execute the Query
    try:
        with connection:
            connection.execute(query, (
                trade["date"],
                trade["pair"],
                trade["position"],
                trade["entry_price"],
                trade["exit_price"],
                trade["timeframe"],
                trade["result"],
                trade["risk_percent"],
                trade["total_rr"],
                trade["profit_loss"],
                trade["emotion"],
                trade["strategy"],
                trade["rule"],
                trade["notes"]
            ))
        print("Trade inserted successfully.")
    
    except Exception as e:
        print(f"Database Error: {e}")

# Show All Trades
def show_trades(connection):
    
    # Query: Show Table
    query = "SELECT * FROM trades"

    # Shows Trades
    try:
        with connection:

            # Cursor: Description for headers Data
            cursor = connection.cursor()
            cursor.execute(query)

            # Headers
            headers = [description[0] for description in cursor.description]

            # Row
            rows = cursor.fetchall()

            # Combine: Tabulate
            print(tabulate(rows, headers=headers, tablefmt = "fancy_grid"))

    except Exception as e:
        print(f"ERROR: {e}")

"""
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
        
    print(tabulate(table, headers, tablefmt="fancy_grid")) """

# Main Function
def main():

    # Connection Var
    connection  = get_connection("trades.db")
    
    # Main Loop
    try:

        # Calling Table
        create_table(connection)

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

                    # Giving get_connection() and add_trade() --> return
                    trade = add_trade()
                    insert_trade(connection, trade)

                elif user == 2:

                    # Show Trades
                    show_trades(connection)

                elif user == 3:
                    pass

                elif user == 4:
                    pass

                elif user == 5:
                    pass    

                else:
                    print("Goodbye!")
                    break    
                
            except ValueError:
                print("Please Enter Number.")   
    finally:
        connection.close()         
        

# Calling
if __name__ == "__main__":
    main()