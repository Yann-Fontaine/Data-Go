from Finance import Budget

myBudget = Budget()
myBudget.add_transactions([{'value': 512, 'category': 'transport'}, {'value': 42.08, 'category': 'salary'}])
for category in myBudget.get_categories() :
    print(category)
    myBudget.show_transactions(category)