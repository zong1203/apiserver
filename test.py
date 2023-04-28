import datetime

test = ["A","B","C","D","E"]
for i,j in enumerate(test):
    print(f"{i},{j}")
    test[i] = ''
print(test)