import streamlit as st
import random

st.set_page_config(layout="wide")

if "wallet" not in st.session_state:
    st.session_state.wallet = 100

player_pool = {
    "Virat Kohli": 10,
    "Rohit Sharma": 9,
    "MS Dhoni": 8,
    "Jasprit Bumrah": 9,
    "KL Rahul": 8,
    "Hardik Pandya": 8,
    "Rishabh Pant": 7,
    "Shubman Gill": 8,
    "Yuzvendra Chahal": 7,
    "Ravindra Jadeja": 9,
    "Shreyas Iyer": 7,
    "Mohammed Shami": 8,
    "Ishan Kishan": 7,
    "Bhuvneshwar Kumar": 8,
    "Deepak Chahar": 7,
    "Suryakumar Yadav": 9,
    "Axar Patel": 7,
    "Prithvi Shaw": 8,
    "Kuldeep Yadav": 7,
    "Sanju Samson": 7,
    "Shardul Thakur": 7,
    "Rahul Tewatia": 6,
    "T Natarajan": 6,
    "Navdeep Saini": 6,
    "Washington Sundar": 7,
    "Mayank Agarwal": 7,
    "Shikhar Dhawan": 8,
    "Varun Chakravarthy": 6,
    "Mohammed Siraj": 7,
    "Manish Pandey": 6
}

betting_options = ["Team A wins", "Team B wins", "Draw"]

def calculate_team_points(selected_players):
    return sum(player_pool[player] for player in selected_players)

def total_players_points(total_points):
    possible_points = [total_points - 10, total_points, total_points + 10] 
    return random.choice(possible_points)

def simulate_result():
    weights = [0.5, 0.4, 0.1]
    result = random.choices(betting_options, weights=weights, k=1)[0]
    return result

st.title("Betting App with Team Selection")
st.write("Choose between Match Winner Prediction or Team Creation!")

st.write(f"### Your Wallet: {st.session_state.wallet} coins")

mode = st.selectbox("Select a mode:", ["Match Winner Prediction", "Make a Team"])

add_amount = st.number_input("Enter amount to add:", min_value=1, step=1)
if st.button("Add Money to Wallet") and add_amount > 0:
    st.session_state.wallet += add_amount
    st.success(f"You've successfully added {add_amount} coins to your wallet. Your new balance is {st.session_state.wallet} coins.")

if mode == "Match Winner Prediction":
    st.write("### Match Winner Prediction")
    selected_option = st.selectbox("Choose your bet:", betting_options)

    if "bet_amount" not in st.session_state:
        st.session_state.bet_amount = 0

    bet_amount = st.number_input("Enter your bet amount:", min_value=1, max_value=st.session_state.wallet, step=1, key="bet_amount")
    
    if bet_amount < 1:
        st.warning("Bet amount must be greater than or equal to 1.")
        
    if st.button("Place Bet"):
    
        if  st.session_state.wallet <= 500:
            result = simulate_result()
            st.write(f"### The result is: {result}!")
            if result==selected_option:
              winnings = bet_amount * 3
              st.session_state.wallet += winnings
              st.success(f"Congratulations! You won {winnings} coins.")

            elif selected_option != result:
              st.session_state.wallet -= bet_amount
              st.error(f"Oops! You lost {bet_amount} coins.")

        elif st.session_state.wallet > 500:
            st.session_state.wallet = max(2, st.session_state.wallet - 5 * bet_amount)
            st.error(f"Oops! You have {st.session_state.wallet} coins left.")

        if st.session_state.wallet < 1:
            st.error("Game Over! Your wallet is empty.")
            add_amount = st.number_input("Enter amount to add:", min_value=1, step=1)
            if st.button("Add Money and Restart Betting"):
                if add_amount > 0:
                    st.session_state.wallet += add_amount
                    st.success(f"You've added {add_amount} coins. Your new balance is {st.session_state.wallet} coins.")
                    st.experimental_rerun()
            else:
                st.stop() 

        st.write(f"### Updated Wallet: {st.session_state.wallet} coins")

elif mode == "Make a Team":
    st.write("### Create Your Team")

    selected_players = st.multiselect("Choose players:", options=list(player_pool.keys()), default=[])

    if len(selected_players) == 11:
        total_points = calculate_team_points(selected_players)
        #st.write(f"### Total Team Points: {total_points}")
    else:
        st.write("Select 11 players")

    if "team_bet" not in st.session_state:
        st.session_state.team_bet = 0

    bet_amount = st.number_input("Enter your bet amount for your team:", min_value=1, max_value=st.session_state.wallet, step=1, key="team_bet")

    if bet_amount < 1:
        st.warning("Bet amount must be greater than or equal to 1.")
        
    if st.button("Submit Team"):
        if len(selected_players) != 11:
            st.error("Please select 11 players to form your team.")
        else:
            if st.session_state.wallet <= 500:
                total_points_result = total_players_points(total_points * 2)
                #st.write(f"### Calculated Total Points Result: {total_points_result}")
                
                if total_points_result > total_points:
                    st.session_state.wallet += bet_amount * 3
                    st.success(f"Congratulations! You won {bet_amount * 3} coins.")
                elif total_points_result < total_points:
                    st.session_state.wallet -= bet_amount
                    st.error(f"Oops! You lost {bet_amount} coins.")
                else:
                    st.warning("No change in points, so no win/loss.")

            elif st.session_state.wallet > 500:
                st.session_state.wallet = max(2, st.session_state.wallet - 5 * bet_amount)
                st.error(f"Oops! You have {st.session_state.wallet} coins left.")

            if st.session_state.wallet < 1:
                st.error("Game Over! Your wallet is empty.")
                add_amount = st.number_input("Enter amount to add:", min_value=1, step=1)
                if st.button("Add Money and Restart Betting"):
                    if add_amount > 0:
                        st.session_state.wallet += add_amount
                        st.success(f"You've added {add_amount} coins. Your new balance is {st.session_state.wallet} coins.")
                        st.experimental_rerun() 
                else:
                    st.stop()

if st.button("Reset Wallet"):
    st.session_state.wallet = 100
    st.success("Your wallet has been reset to 100 coins.")

if st.button("Predict Again"):
    wallet_value = st.session_state.wallet
    st.session_state.clear()  
    st.session_state.wallet = wallet_value
    st.success(f"Next betting Session has been reset to {wallet_value} coins.")
