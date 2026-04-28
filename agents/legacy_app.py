# legacy_app.py
# A very old script to calculate shipping costs

DATA = [["id1", 100, "express"], ["id2", 50, "standard"], ["id3", 200, "standard"]]

def calc(i, p):
    for x in DATA:
        if x[0] == i:
            # Deep nesting and confusing variable names
            if x[2] == "express":
                if p > 150:
                    res = p * 0.05 # 5% fee
                else:
                    res = p * 0.1 # 10% fee
            else:
                if p > 100:
                    res = p * 0.02
                else:
                    res = 5 # flat fee
            
            print("Total for " + i + " is " + str(p + res))
            return p + res
    return "error"

print(calc("id1", 120))