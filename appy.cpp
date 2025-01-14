#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cstdlib>
#include <ctime>
#include <algorithm>
using namespace std;

map<string, int> playerPool = {
    {"Virat Kohli", 10}, {"Rohit Sharma", 9}, {"MS Dhoni", 8}, {"Jasprit Bumrah", 9}, {"KL Rahul", 8},
    {"Hardik Pandya", 8}, {"Rishabh Pant", 7}, {"Shubman Gill", 8}, {"Yuzvendra Chahal", 7}, {"Ravindra Jadeja", 9},
    {"Shreyas Iyer", 7}, {"Mohammed Shami", 8}, {"Ishan Kishan", 7}, {"Bhuvneshwar Kumar", 8}, {"Deepak Chahar", 7},
    {"Suryakumar Yadav", 9}, {"Axar Patel", 7}, {"Prithvi Shaw", 8}, {"Kuldeep Yadav", 7}, {"Sanju Samson", 7},
    {"Shardul Thakur", 7}, {"Rahul Tewatia", 6}, {"T Natarajan", 6}, {"Navdeep Saini", 6}, {"Washington Sundar", 7},
    {"Mayank Agarwal", 7}, {"Shikhar Dhawan", 8}, {"Varun Chakravarthy", 6}, {"Mohammed Siraj", 7}, {"Manish Pandey", 6}
};


string simulateResult() {
    vector<string> outcomes = {"Team A wins", "Team B wins", "Draw"};
    vector<double> weights = {0.5, 0.4, 0.1};
    double randomValue = (double)rand() / RAND_MAX;
    double cumulativeWeight = 0.0;

    for (size_t i = 0; i < outcomes.size(); ++i) {
        cumulativeWeight += weights[i];
        if (randomValue <= cumulativeWeight) {
            return outcomes[i];
        }
    }
    return outcomes[0];
}

int calculateTeamPoints(const vector<string>& selectedPlayers) {
    int totalPoints = 0;
    for (const string& player : selectedPlayers) {
        totalPoints += playerPool[player];
    }
    return totalPoints;
}

int main() {
    srand(time(0));
    int wallet = 100;
    int betAmount;
    string mode;

    cout << "Welcome to the Betting App!\n";
    while (true) {
        cout << "\nCurrent Wallet Balance: " << wallet << " coins\n";
        cout << "Choose a mode: \n1. Match Winner Prediction\n2. Make a Team\n3. Reset Wallet\n4. Exit\n";
        int choice;
        cin >> choice;

        if (choice == 1) { 
            cout << "### Match Winner Prediction ###\n";
            cout << "Choose your bet: \n1. Team A wins\n2. Team B wins\n3. Draw\n";
            int betChoice;
            cin >> betChoice;
            string selectedOption = (betChoice == 1) ? "Team A wins" : (betChoice == 2) ? "Team B wins" : "Draw";

            if (wallet > 0) {
                cout << "Enter your bet amount (1 to " << wallet << "): ";
                cin >> betAmount;

                if (betAmount < 1 || betAmount > wallet) {
                    cout << "Invalid bet amount.\n";
                    continue;
                }

                if (wallet <= 500) {
                    string result = simulateResult();
                    cout << "The result is: " << result << "!\n";

                    if (result == selectedOption) {
                        int winnings = betAmount * 3;
                        wallet += winnings;
                        cout << "Congratulations! You won " << winnings << " coins.\n";
                    } else {
                        wallet -= betAmount;
                        cout << "Oops! You lost " << betAmount << " coins.\n";
                    }
                } else {
                    wallet = max(2, wallet - 5 * betAmount);
                    cout << "Oops! You have " << wallet << " coins left.\n";
                }
            } else {
                cout << "Please add coins to your wallet.\n";
            }

        } else if (choice == 2) { 
            cout << "### Create Your Team ###\n";
            vector<string> selectedPlayers;
            string player;

            cout << "Select 11 players from the pool (type player names, one per line):\n";
            for (auto it = playerPool.begin(); it != playerPool.end(); ++it) {
            cout << it->first << " (" << it->second << " points)\n";
            }


            while (selectedPlayers.size() < 11) {
            cout << "Enter player name: ";
            getline(cin, player); 
            if (playerPool.find(player) != playerPool.end() &&
            find(selectedPlayers.begin(), selectedPlayers.end(), player) == selectedPlayers.end()) {
            selectedPlayers.push_back(player);
            cout << player << " added to your team.\n"; }
            else {
            cout << "Invalid or duplicate player. Try again.\n";
            }
}


            int totalPoints = calculateTeamPoints(selectedPlayers);
            cout << "Your team's total points: " << totalPoints << "\n";

            if (wallet > 0) {
                cout << "Enter your bet amount for your team (1 to " << wallet << "): ";
                cin >> betAmount;

                if (wallet <= 500) {
                    int opponentPoints = totalPoints + (rand() % 21 - 10); 
                    cout << "Opponent team's points: " << opponentPoints << "\n";

                    if (totalPoints > opponentPoints) {
                        int winnings = betAmount * 3;
                        wallet += winnings;
                        cout << "Congratulations! You won " << winnings << " coins.\n";
                    } else {
                        wallet -= betAmount;
                        cout << "Oops! You lost " << betAmount << " coins.\n";
                    }
                } else {
                    wallet = max(2, wallet - 5 * betAmount);
                    cout << "Oops! You have " << wallet << " coins left.\n";
                }
            } else {
                cout << "Please add coins to your wallet.\n";
            }

        } else if (choice == 3) {  
            wallet = 100;
            cout << "Your wallet has been reset to 100 coins.\n";

        } else if (choice == 4) {
            cout << "Exiting the app. Goodbye!\n";
            break;

        } else {
            cout << "Invalid choice. Try again.\n";
        }
    }

    return 0;
}
