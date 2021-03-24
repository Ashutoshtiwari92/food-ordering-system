# food ordering system
# restaurant class
import logging
import enum
import math
import threading

class Orderstatus(enum.Enum):
    ACTIVE , PENDING , COMPLETED = 1, 2, 3

class DB():

    def __init__(self):
        pass

    def fetchingrows():
        pass
    
    def updatingrows():
        pass


class Restaurant(object):

    def __init__(self, restaurant_name, capacity, rating):

        self.restaurant_name = restaurant_name
        self.capacity = capacity
        self.menus = {}
        self.rating = rating

    def add_menus(self, item, price):

        if item not in self.menus:
            self.menus[item] = {
            'item_name' : item,
            'price' : price,
            }

        else:
            self.menus[item]['item_name'] = item
            self.menus[item]['price'] = price


    def display(self):
        print('items in {0} restaurant-------------------{1}'.format(self.restaurant_name, self.menus))


    def  display_menu(self):

        for k, v in self.menus:
            print('Item name ->', v['item_name'])
            print('price ->', v['price'])


class RestaurantSytem(Restaurant):

    def __init__(self):
        self.restaurant = []

    def add_restaurant(self, restaurant_name, capacity, rating):
        res = Restaurant(restaurant_name, capacity, rating)
        self.restaurant.append(res)

    def add_item_menus(self, res_name, item, price):

        for res_obj in self.restaurant:
            if res_obj.restaurant_name == res_name:
                res_obj.add_menus(item, price)

    def display_all_restaurant(self):

        for res_obj in self.restaurant:
            print('Restaurant name ->',res_obj.restaurant_name)
            print('capacity ->',res_obj.capacity)
            print('Menus ->', res_obj.menus)
            print('Rating ->', res_obj.rating)
            print('------------------------------------------')


    def food_order(self, item, rating = 0, low_price = 0, lock = None):
        
        result = []
        mx_rating = 0
        lw_price = float('inf')
        order = None
        if lock:
            lock.acquire()
            # print('lock-----resource')
        for res_obj in self.restaurant:
            if item in res_obj.menus and res_obj.capacity != 0:
                result.append(res_obj)
        
        if len(result) == 0:
            logging.error('our capacity is full please try after sometime')
            lock.release()
            # print('lock release-----resource')
            return

        if rating != 0:
            if len(result) > 0:
                for res_obj in result:
                    x = int(res_obj.rating)
                    if x > mx_rating:
                        mx_rating = x
                        order = res_obj

                if order.capacity !=0:
                    order.capacity -=1
                    print('your order is done ->', item)
                    print('Highest rating res ->',order.restaurant_name)
                    print('-------------\n')
                elif order.capacity == 0:
                    logging.error('Full of capacity-- wait')
                lock.release()
                # print('lock release-----resource')
                return

        if low_price != 0:
            if len(result) > 0:
                for res_obj in result:
                    if item in res_obj.menus:
                        if lw_price > res_obj.menus[item]['price']:
                            lw_price = res_obj.menus[item]['price']
                            order = res_obj

                if order.capacity !=0:
                    order.capacity -=1
                    print('your order is done ->', item)
                    print('low price res ->',order.restaurant_name)
                    print('-------------\n')
                elif order.capacity == 0:
                    logging.error('Full of capacity-- wait')
                lock.release()
                # print('lock release-----resource')
                return


if __name__ == "__main__":

    lock = threading.Lock()
    rs = RestaurantSytem()
   
   # 1)addition of restaurant
    rs.add_restaurant('rajesthani', 3, 4)
    rs.add_restaurant('gurukrupa', 3, 3)
    rs.add_restaurant('pizzahut', 3, 6)
    rs.add_restaurant('dominoz', 3, 2)
    rs.add_restaurant('max', 3, 5)
    rs.add_restaurant('hotel', 3, 7)
    #----------------------------------


    # 2) adding items menu in restaurant
    rs.add_item_menus('pizzahut', 'vegPizza', 100)
    rs.add_item_menus('rajesthani', 'curry', 100)
    rs.add_item_menus('gurukrupa', 'pizza', 100)
    rs.add_item_menus('dominoz', 'vegPizza', 80)
    rs.add_item_menus('max', 'vegPizza', 120)
    rs.add_item_menus('hotel', 'vegPizza', 200)
    # rs.add_menus

    # 3) any random user ordering to our food order sytem
    rs.food_order('vegPizza', 1, 0, lock)
    rs.food_order('vegPizza', 0, 1, lock)
    rs.food_order('vegPizza', 1, 0, lock)
    rs.food_order('vegPizza', 1, 0, lock)
    rs.food_order('vegPizza', 1, 0, lock)

    # 4) capacity should not breach
    
    rs.food_order('curry', 0, 1, lock)
    rs.food_order('curry', 0, 1, lock)
    rs.food_order('curry', 0, 1, lock)
    rs.food_order('curry', 0, 1, lock)

    # 5) concurrent access should not there -- put lock to avoid race condition

    t1 = threading.Thread(target=rs.food_order, args=('vegPizza', 0, 1, lock))
    t2 = threading.Thread(target=rs.food_order, args=('vegPizza', 0, 1, lock))
    t3 = threading.Thread(target=rs.food_order, args=('vegPizza', 0, 1, lock))
    t4 = threading.Thread(target=rs.food_order, args=('vegPizza', 0, 1, lock))

    t5 = threading.Thread(target=rs.food_order, args=('curry', 0, 1, lock))
    t6 = threading.Thread(target=rs.food_order, args=('curry', 0, 1, lock))
    t7 = threading.Thread(target=rs.food_order, args=('curry', 0, 1, lock))
    t8 = threading.Thread(target=rs.food_order, args=('curry', 0, 1, lock))

    # # start threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
  
    # # # wait until threads finish their job
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
  
    rs.display_all_restaurant()


    
