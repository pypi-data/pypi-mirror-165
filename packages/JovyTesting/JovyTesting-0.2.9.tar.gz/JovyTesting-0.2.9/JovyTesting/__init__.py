

__all__ = ["Customer","Item"]


#The customer Class
class Customer():
    def __init__(self,name=None,wallet=0):
        self.name = name
        self.wallet = wallet
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


    def __str__(self):
        return f"This is our dear Customer {repr(self.name)} "

    def __repr__(self):
        return f"Item(name={self.name},wallet={self.wallet})"



#The Item class
class Item():
    def __init__(self, name, price):
        self.name = name
        self.price = price


    def __str__(self):
        return f"This is a {repr(self.name)} Item"

    def __repr__(self):
        return f"Customer({self.name},{self.price})"

