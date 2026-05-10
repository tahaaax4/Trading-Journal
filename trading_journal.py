from tabulate import tabulate
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
        timeframe = input("Timeframe: ").upper().strip()

    # Result
    while True:
        result = input("Result (Win/Loss): ").lower().strip()

        if result and result[0] == "w":
            result = "win"
            break
        elif result and result[0] == "l":
            result = "loss"
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

    if result == "loss":
        profit_loss = -abs(profit_loss)

    elif result == "win":
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
        print("--------------------------------")
        print("Trade Added successfully.")
        print("--------------------------------")
    
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
            if not rows:
                print("No trades found.")
                return

            # Combine: Tabulate
            print(tabulate(rows, headers=headers, tablefmt = "fancy_grid"))

    except Exception as e:
        print(f"ERROR: {e}")

# Reset All Trades 
def delete_trade(connection):

    # Asking 
    print("1. Delete Trade")
    print("2. Reset")

    # Choice Input Delete Or Reset
    while True:
        try:
            choice = int(input("Enter Number: "))
            if choice != 1 and choice != 2:
                print("Enter 1 or 2.")
            else:
                break
        except ValueError:
            print("Enter number")

    # If Choice Is 1
    if choice == 1:

        while True:

            # Get Id For Trade Delete
            try:
                trade_id = int(input("Enter Trade id: "))
                break
            except ValueError:
                print("Enter id")

        # Query: Delete
        del_query = "DELETE FROM trades WHERE id = ?"

        # Execute Query
        try:
            with connection:
                connection.execute(del_query, (trade_id,))
                print("--------------------------------------")
                print(f"Trade id '{trade_id} id deleted'")
                print("--------------------------------------")
        except Exception as e:
            print(f"ERROR: {e}")

    # If Choice Is 2
    if choice == 2:

        # Query: Reset
        reset_query = "DELETE FROM trades"

        # Execute Query
        try:
            with connection:
                connection.execute(reset_query)
                print("----------------------------")
                print("Journal Has Been Reset")
                print("----------------------------")
        except Exception as e:
            print(f"ERROR: {e}")

# Show Trading Summary
def show_summary(connection):

    # Query: Get all trades from database
    query = "SELECT * FROM trades"

    try:
        with connection:

            # Create cursor object
            cursor = connection.cursor()

            # Execute SQL query
            cursor.execute(query)

            # Fetch all rows from database
            rows = cursor.fetchall()

            # If no trades exist
            if not rows:
                print("No trades in database.")
                return

            # VARIABLES FOR CALCULATIONS
            win = 0
            loss = 0

            total_profit = 0

            total_win_amount = 0
            total_loss_amount = 0

            total_rr = 0
            total_risk = 0

            total_long = 0
            total_short = 0

            long_wins = 0
            short_wins = 0

            total_trades = len(rows)

            # LOOP THROUGH EACH TRADE
            for each_trade in rows:

                # INDEX MAP
                # 0 = id
                # 1 = date
                # 2 = pair
                # 3 = position
                # 4 = entry_price
                # 5 = exit_price
                # 6 = timeframe
                # 7 = result
                # 8 = risk_percent
                # 9 = total_rr
                # 10 = profit_loss
                # 11 = emotion
                # 12 = strategy
                # 13 = rule
                # 14 = notes

                result = each_trade[7]
                rr = each_trade[9]
                profit = each_trade[10]
                risk = each_trade[8]
                position = each_trade[3]

                # Count wins/losses
                if result == "win":
                    win += 1
                    total_win_amount += profit

                elif result == "loss":
                    loss += 1
                    total_loss_amount += abs(profit)

                if position == "Long":
                    total_long += 1

                elif position == "Short":
                    total_short += 1

                # Wins Longs/Shorts
                if position == "Long" and result == "win":
                    long_wins += 1

                elif position == "Short" and result == "win":
                    short_wins += 1



                # Add totals
                total_profit += profit
                total_rr += rr
                total_risk += risk

            # -----------------------------
            # FINAL CALCULATIONS
            # -----------------------------

            # Winrate %
            winrate = (win / total_trades) * 100

            # Biggest winning trade
            biggest_win = max(
                t[10] for t in rows
                if t[7].lower() == "win")

            # Biggest losing trade
            biggest_loss = min(
                t[10] for t in rows
                if t[7].lower() == "loss")

            # Average calculations
            avg_risk = total_risk / total_trades
            avg_rr = total_rr / total_trades

            avg_win = total_win_amount / win if win else 0
            avg_loss = total_loss_amount / loss if loss else 0

            # Long/Short Winrate
            if total_long:
                long_winrate = (long_wins / total_long) * 100
            else:
                long_winrate = 0
            
            if total_short:
                short_winrate = (short_wins / total_short) * 100
            else:
                short_winrate = 0

            # Expectancy formula
            expectancy = (
                (win / total_trades) * avg_win) - ((loss / total_trades) * avg_loss)

            # Profit Factor
            profit_factor = (
                total_win_amount / total_loss_amount
                if total_loss_amount != 0
                else 0
            )

            # PRINT SUMMARY
            print("------------------------------------------")
            print(f"📝 Total Trades = {total_trades}")

            print(f"✔️ Total Wins = {win}")
            print(f"✖️ Total Losses = {loss}")

            print(f"📈 Winrate = {winrate:.2f}%")

            print(f"💰 Total Profit = {total_profit:.2f}")

            print(f"📈 Total Long Trades = {total_long}")
            print(f"📉 Total Short Trades = {total_short}")

            print(f"📊 Average Win = {avg_win:.2f}")
            print(f"📊 Average Loss = {avg_loss:.2f}")

            print(f"📊 Average Risk = {avg_risk:.2f}%")
            print(f"📊 Average RR = {avg_rr:.2f}")

            print(f"🏆 Biggest Win = {biggest_win:.2f}")
            print(f"📉 Biggest Loss = {biggest_loss:.2f}")

            print(f"📈 Long Winrate = {long_winrate}")
            print(f"📉 Short Winrate = {short_winrate}")

            print(f"⚡ Profit Factor = {profit_factor:.2f}")

            print(f"⌛ Expectancy Per Trade = {expectancy:.2f}")

            print("------------------------------------------")

    except Exception as e:
        print(f"ERROR: {e}")

# Display Query For Filetered Object
def display_query(connection, query, values=()):

    try:
        with connection:
            # Cursor: Description for headers Data
            cursor = connection.cursor()
            cursor.execute(query, values)

            # Headers
            headers = [description[0] for description in cursor.description]

            # Row
            rows = cursor.fetchall()
            if not rows:
                print("No trades found.")
                return

            # Combine: Tabulate
            print(tabulate(rows, headers=headers, tablefmt = "fancy_grid"))

    except Exception as e:
                    print(f"ERROR: {e}")

# Filtering Trdes
def filtered_trades(connection):

    while True:
        print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        print("🗓️ Filter By:")
        print("💡 1. Pair")
        print("📉 2. Win/Loss")
        print("📈 3. Long/Short")
        print("💡 4. Strategy (Breakout, Ranging, Continutaion, Reversal)")
        print("⚠️ 5. Rule")
        print("📆 6. Date")
        print("🔺 7. Profitability")
        print("🔻 8. Losing trades")
        print("💰 9. RR")
        print("👋 0. Exit")
        print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
    
        try:
            choice = int(input("Enter a Pair: "))

            # Break
            if choice == 0:
                print("👋 GoodBye..")
                break

            # Pair
            if choice == 1:
                pair_choice = input("Enter Pair Name: ")

                query = "SELECT * FROM trades WHERE pair = ?"

                display_query(connection, query, (pair_choice,))

            # Result
            elif choice == 2:
                result_choice = input("Enter Win/Loss: ").lower().strip()
                query = "SELECT * FROM trades WHERE result = ?"
                display_query(connection, query, (result_choice,))

            # Position
            elif choice == 3:
                position_choice = input("Enter Long/Short: ").capitalize().strip()
                query = "SELECT * FROM trades WHERE position = ?"
                display_query(connection, query, (position_choice,))

            # Strategy
            elif choice == 4:
                strategy_choice = input("Enter Strategy: ").capitalize().strip()
                query = "SELECT * FROM trades WHERE strategy = ?"
                display_query(connection, query, (strategy_choice,))

            # Rule
            elif choice == 5:
                rule_choice = input("Followed Rules? (Yes/No): ").capitalize().strip()
                query = "SELECT * FROM trades WHERE rule = ?"
                display_query(connection, query, (rule_choice,))

            # Date
            elif choice == 6:
                date_choice = input("Enter Date: ").strip()
                query = "SELECT * FROM trades WHERE date = ?"
                display_query(connection, query, (date_choice,))

            # Profitability
            elif choice == 7:
                query = "SELECT * FROM trades WHERE profit_loss > 0"
                display_query(connection, query)

            # Losing Trades
            elif choice == 8:
                query = "SELECT * FROM trades WHERE profit_loss < 0"
                display_query(connection, query)

            # RR
            elif choice == 9:
                rr_choice = float(input("Enter Minimum RR: "))
                query = "SELECT * FROM trades WHERE total_rr >= ?"
                display_query(connection, query, (rr_choice,))

            else:
                print("Invalid Input")

        except ValueError:      
            print("Enter Valid Number.")

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
            print("🏳️ 5.Delete Trades")
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
                    show_summary(connection)

                elif user == 4:
                    filtered_trades(connection)
                
                # Delete Or Reset Trades
                elif user == 5:
                    delete_trade(connection)  

                # Break
                elif user == 6:
                    print("Goodbye!")
                    break

                else:
                    print("Invalid Input")  

            except ValueError:
                print("Please Enter Number.")   
    finally:
        connection.close()         
        

# Calling
if __name__ == "__main__":
    main()