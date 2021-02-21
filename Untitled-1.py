for a in range(100):
    b = a /10
    try:
        print(b, "type : ", int(b), a % 10)
    except:
        print(b)