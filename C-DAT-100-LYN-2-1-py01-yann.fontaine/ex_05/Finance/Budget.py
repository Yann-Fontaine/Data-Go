import json
class Budget:

    def __init__(self):
        self.balance = 0
        with open("Finance/data.json") as data:
            self.__transactions = json.load(data)
        for transaction in self.__transactions['transactions']:
            self.balance += transaction['value']

    def add_transactions(self, transacs):
        for transac in transacs:
            try:
                self.__transactions['transactions'].append(transac)
                with open('Finance/data.json', 'w') as file:
                    json.dump(self.__transactions, file)
                self.balance += transac['value']
            except ValueError:
                print("Please use array of objects only")
                return False

    def show_transactions(self, category): 
        for transaction in self.__transactions['transactions']:
            if transaction['category']==category:
                if transaction['value'] > 0:
                    print('You received {} euros for {}'.format(transaction['value'], category))
                elif transaction['value'] == 0:
                    print('Your balance is unchanged')
                else:
                    print('You spent {} euros for {}'.format(transaction['value'], category))

    def get_categories(self):
        self.categories=[]
        for transaction in self.__transactions['transactions']:
            self.categories.append(transaction['category'])
        return self.categories

    def action_case(self, choice):
        if choice == '1':
            print('Your balance is {}$'.format(self.balance))
        elif choice == '2':
            amount = input("What is the amount of the transaction ?")
            category = input('In which category do you want to register this amount ?')
            self.add_transactions([{'value': float(amount), 'category': category}])
        elif choice == '3':
            for category in self.get_categories():
                self.show_transactions(category)
        elif choice == '4': 
            exit()    
        else: 
            print("Unvalid Choice")