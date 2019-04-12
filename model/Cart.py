import abc
import datetime
import logging

from model import Clinic


class CartInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, clinic: Clinic, start_time: datetime.time, walk_in: bool) -> bool:
        pass

    @abc.abstractmethod
    def remove(self, item_id: int):
        pass

    @abc.abstractmethod
    def get_all(self):
        pass

    @abc.abstractmethod
    def get_item_dict(self):
        pass

    @abc.abstractmethod
    def batch_remove(self, item_list):
        pass

    @abc.abstractmethod
    def batch_mark_booked(self, item_list):
        pass


class Cart(CartInterface):
    def __init__(self):
        self.item_dict = {}
        self.__id_counter = 0  # Internal ID of cart items, analogous to an autoincrementing ID as seen in popular DBs.

    def add(self, clinic: Clinic, start_time: datetime, walk_in: bool) -> bool:
        if not self.__check_if_item_exists(clinic, start_time, walk_in):
            self.item_dict[self.__id_counter] = CartItem(self.__id_counter, clinic, start_time, walk_in, False)
            self.__id_counter += 1
            return True
        return False

    def __check_if_item_exists(self, clinic: Clinic, start_time: datetime, walk_in: bool) -> bool:  # Checks if a cart item already exists.
        for item in self.item_dict.values():
            if clinic == item.clinic and start_time == item.start_time and walk_in == item.walk_in:
                return True
        return False

    def remove(self, item_id: int):
        try:
            self.item_dict.pop(item_id)
            return True
        except KeyError:
            return False

    def get_all(self):
        return list(self.item_dict.values())

    def get_item_dict(self):
        return self.item_dict

    def batch_remove(self, item_list):  # Removes all items in a list of CartItems.
        for item in item_list:
            self.remove(item.item_id)

    def batch_mark_booked(self, item_list):  # Marks all items in a list of CartItems as booked.
        for item in item_list:
            item.is_booked = True


class CartItem:
    def __init__(self, item_id: int, clinic: Clinic, start_time: datetime, walk_in: bool, is_booked: bool):
        self.item_id = item_id  # Internal cart item ID, not unique across multiple users.
        self.clinic = clinic
        self.start_time = start_time  # Stored as string
        self.walk_in = walk_in  # Stored as boolean
        self.is_booked = is_booked  # Stored as boolean

    def __str__(self):
        return "Cart Item ID: " + str(self.item_id) + "\nClinic: " + self.clinic.name + "\nStart time: " + \
               str(self.start_time) + "\nType: " + "Walk-in" if self.walk_in else "Annual" + "\nStatus - Booked: " + \
                                                                                  str(self.is_booked)


class StatisticsProxyCart(CartInterface):
    def __init__(self):
        self.cart = Cart()

    def add(self, clinic: Clinic, start_time: datetime.time, walk_in: bool) -> bool:
        logging.info('Added item to cart with:'
                     ' Clinic: ' + clinic.name +
                     ' Start time: ' + str(start_time) +
                     ' Type: ' + 'Walk-in' if walk_in else 'Annual')
        return self.cart.add(clinic, start_time, walk_in)

    def remove(self, item_id: int):
        logging.info('Removed item from cart with ID: ' + str(item_id))
        return self.cart.remove(item_id)

    def get_all(self):
        return self.cart.get_all()

    def get_item_dict(self):
        return self.cart.get_item_dict()

    def batch_remove(self, item_list):
        self.cart.batch_remove(item_list)

    def batch_mark_booked(self, item_list):
        self.cart.batch_mark_booked(item_list)
