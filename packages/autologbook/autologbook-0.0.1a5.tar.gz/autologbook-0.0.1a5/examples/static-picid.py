# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 21:40:32 2022

@author: Antonio
"""

# usercomment
# imageuniqueid


class Base():
    _used_ids = []
    _next_to_use_id = 1000

    def __init__(self, id):
        self.id = self.assign_unique_ID(id)

    def _is_ID_taken(self, id):
        if id in Base._used_ids:
            return True
        return False

    def assign_unique_ID(self, id):
        if not self._is_ID_taken(id):
            Base._used_ids.append(id)
            return id
        else:
            while self._is_ID_taken(Base._next_to_use_id):
                Base._next_to_use_id += 1
                # print(f'{Base._next_to_use_id} =')
                # print(f'{self._is_ID_taken(Base._next_to_use_id)} = ')
            Base._used_ids.append(Base._next_to_use_id)
            self.id = Base._next_to_use_id
            return Base._next_to_use_id

    def getID(self):
        return self.id


class Advanced(Base):

    def __init__(self, id):
        super().__init__(id)


def main():

    idlist = (1, 2, 3, 4, 5, 1, 5, 7, 1, 10, 22, 8, 9, 20)
    for id in idlist:
        a = Advanced(id)
        print(a.getID())


if __name__ == '__main__':
    main()
