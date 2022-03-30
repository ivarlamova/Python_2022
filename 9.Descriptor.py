# дескриптор Value для расчета комиссии, который будет использоваться в классе Account

class Value:

    def __get__(self, instance, obj_type):
        return self.result

    def __set__(self, instance, value):
        self.result = value * (1 - instance.commission)

class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
'''
new_account = Account(0.1)
new_account.amount = 3

print(new_account.amount)
'''