

__all__ = ["Customer","Item"]




class Item():
    def __init__(self, name, price):
        self.name = name
        self.price = price



class Customer():
    def __init__(self,name=None,net=0):
        self.name = name
        self.wallet = net
        self.items = {

        }

    def addToCart(self, item):
        name = item.name
        price = item.price
        obj = {
            "name":name,
            "price":price
        }
        self.items[len(self.items)] = obj

    def checkOut(self):
        totalPrice = 0
        allPrices = list(map(lambda x: int(self.items[x]["price"]), self.items))
        allItems = list(map(lambda x: str(self.items[x]["name"]), self.items))
        totalPrice = sum(allPrices)
        newBalance = self.wallet - totalPrice 
        
        if newBalance >= 0:
            self.wallet -= totalPrice
            print(f"Successfully bought {allItems} worth {totalPrice}")
            return
        else:
            print("You dont have enough money to buy all these items")
            return