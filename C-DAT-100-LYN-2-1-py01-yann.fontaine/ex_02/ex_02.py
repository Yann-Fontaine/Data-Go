class Budget:
    def __init__(self):
        self.__transactions = []

    def add_transactions(self, transacs):
        for number in transacs:
            try:
                self.__transactions.append(float(number))
            except ValueError:
                print("Please use numbers only")
                return False


    def show_transactions(self): 
        print(self.__transactions)
        for value in self.__transactions:
            if value > 0:
                print('You received {} euros'.format(value))
            elif value == 0:
                print('Your balance is unchanged')
            else:
                print('You spent {} euros'.format(value))

myBudget=Budget()
myBudget.add_transactions([512, 42.08, -12, 'kangaroo'])
myBudget.show_transactions()