

dict1 = {"a": 1, "b": 3}
for i in dict1.copy():
    if i == "a":
        del dict1["a"]