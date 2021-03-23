#!/usr/bin/env python
from Finance import Budget

myBudget = Budget()
for category in myBudget.get_categories() :
    myBudget.show_transactions(category)

print('Choose between :\n1 - consult my balance\n2 - add new transaction\n3 - consult your transaction history\n4 - quit')
choice = input()
myBudget.action_case(choice)