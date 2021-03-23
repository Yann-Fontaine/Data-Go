def show_transaction(list): 
    for value in list:
        if value > 0:
            print('You received {} euros'.format(value))
        elif value == 0:
            print('Your balance is unchanged')
        else:
            print('You spent {} euros'.format(value))

show_transaction([512 , 42.08 , -12])