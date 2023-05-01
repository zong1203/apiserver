with open("./server.log", "r") as f:
    text = f.readlines()
    for i in text:
        print(i)