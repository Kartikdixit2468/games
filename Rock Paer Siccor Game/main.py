# Rock Paper Siccor game made By Arush
from random import choice

print("..............WELCOME to Rock, Paper,Scissor Game................")
print("..............Score more than 2 to win....................")
chances = 5
choices = ('scissor', 'rock','paper')
score = 0

while chances > 0:
    user_choice = str(input("Entre Your Choice -: \n ")).lower()
    comp_choice = str(choice(choices)).lower()

    if user_choice == comp_choice:
        print("Game Draw")
        print("Computer : ", comp_choice)
        print("score - ", score)

    elif user_choice != comp_choice and user_choice in choices:

        if user_choice == 'rock' and comp_choice == 'paper':
            print("Computer : ", comp_choice)
            print("Computer Win \nScore - ", score)

        elif user_choice == 'rock' and comp_choice == 'scissor':
            score += 1
            print("Computer : ", comp_choice)
            print("You Win \nScore - ", score)

        elif user_choice == 'paper' and comp_choice == 'scissor':
            print("Computer : ", comp_choice)
            print("Computer Win \nScore - ", score)

        elif user_choice == 'paper' and comp_choice == 'rock':
            score += 1
            print("Computer : ", comp_choice)
            print("You Win \nScore - ", score)

        elif user_choice == 'scissor' and comp_choice == 'rock':
            print("Computer : ", comp_choice)
            print("Computer Win \nScore - ", score)

        elif user_choice == 'scissor' and comp_choice == 'paper':
            score += 1
            print("Computer : ", comp_choice)
            print("You Win \nScore - ", score)

    else:
        print("Invalid Input \nTry Again!\n")
        chances += 1
    
    chances -= 1

print("Game Completed! \nYour Score", score)
if score > 2:
    print("You Win!")
else:
    print("Computer Wins!")

# Completed
