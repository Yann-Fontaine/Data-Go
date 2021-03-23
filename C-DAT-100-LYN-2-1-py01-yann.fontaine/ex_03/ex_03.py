import json
class Budget:

    def __init__(self, path = None):
        if path == None:
            self.__transactions = {
                'transactions': []
            }
        else:
            with open (path) as data:
                self.__transactions = json.load(data)

    def add_transactions(self, transacs):
        for transac in transacs:
            try:
                self.__transactions['transactions'].append(transac)
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

myBudget = Budget("data.json")
for category in myBudget.get_categories() :
    print(category)
    myBudget.show_transactions(category)