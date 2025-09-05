# Python Practice 1: Reviewing all fundamentals

# Background: I am comfortable with like 95 percent of the fundamentals, but there are some that I want to make sure I have completely down. A mini-project with
#             several of the core fundamentals is a nice start to what will likely be a long python learning process.

# Goal: I don't have to think twice about any of the fundamentals in the future, I have them memorized and I will not forget them

# Project: Build a simple console-based budget tracker that:
#          - Asks the user to enter income and expenses
#              - If income is specified, apply a 20 percent tax. Then, apply that tax and state the actual amount of money added.
#          - Stores them in a dictionary or list
#          - Calculates total income, expenses, and net balance
#          - Uses functions and loops
#          - Handles basic errors like invalid input

# Day 1 progress:
# - Generated this practice project, changed a few of the attributes, created the add_transaction and started the view_transaction functions, learned about lists and
#   dictionaries more as well as went back over loops and input statements

# Day 2 progress:
# - Updated add_transaction to include error handling and rounding, debugged the view_transaction function by toying around with the loop and finding what I wanted to
#   loop through, finalized view_transaction by adding the extra statistics at the end, and tested some for edge cases to make sure this runs how I want it to.

# COMPLETED on day 2


def main():

    list_of_transactions = []
    
    def add_transaction():

        income_expense = input('Is this income or an expense? ')

        if income_expense.lower() == 'income':
            income_amt = input('What is your income? ')
            try:
                round(float(income_amt))
            except ValueError:
                raise ValueError("Put a number next time.")
            adj_income_amt = round(float(income_amt), 2) * 0.80
            print(f"Your income after tax is {adj_income_amt}!")
            income_desc = input('What type of income is this? ')
            if any(char.isdigit() for char in income_desc):
                raise ValueError("Put a string next time.")
            list_of_transactions.append({
                'Type': 'Income',
                'Description': income_desc, 
                'Amount': adj_income_amt
            })
        
        elif income_expense.lower() == 'expense':
            expense_amt = input('What is your expense amount? ')
            expense_desc = input('What type of expense is this? ')
            list_of_transactions.append({
                'Type': 'Expense',
                'Description': expense_desc,
                'Amount': round(float(expense_amt), 2)
            })

        else:
            print('You did not specify an expense or income. This program will now quit.')
            quit()
        

    def view_transaction():
        '''
        Test to see if the docstring works as it is supposed to
        '''
        total_income = 0
        total_expenses = 0
        total_sum = 0
        for transaction in list_of_transactions:
            if transaction['Type'] == 'Income':
                print(f"[+ ${transaction['Amount']}] from {transaction['Description']}")
                total_income += transaction['Amount']
                total_sum += transaction['Amount']
                print()
            elif transaction['Type'] == 'Expense':
                print(f"[- ${transaction['Amount']}] from {transaction['Description']}")
                total_expenses += transaction['Amount']
                total_sum -= transaction['Amount']
                print()
        print('\n\n')
        print(f'Total Income: {total_income}')
        print(f'Total Expenses: {total_expenses}')
        print(f'Total Money Saved: {total_sum}')


    while True:        
        action_request = input('Are you going to add a transaction, view your transactions, or quit the program? Please enter either Add, View, or Quit: ')
        if action_request.lower() == 'add':
            add_transaction()
        elif action_request.lower() == 'view':
            view_transaction()
        elif action_request.lower() == 'quit':
            print('Thanks for tracking your finances with this program! The program will now reset and no records will remain.')
            break
        else:
            print('You did not specify an action type. This program will now quit.')
            break
            




if __name__ == '__main__':
    main()





