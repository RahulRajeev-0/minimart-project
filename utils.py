
def get_discounted_price(price, discount):
    return price - (price * discount / 100)



def logger(data):
    with open("logfile.txt", "a") as f:
        f.write(str(data) + "\n")

