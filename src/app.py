import time
from random import randint


class Node(object):
    def __init__(self, value=None):
        self.val = value
        self.next = None
        self.prev = None

    def __str__(self):
        return "{0}".format(self.val)


class SinglyLinkedList(object):
    def __init__(self):
        self.head = None
        self.current = None
        self.tail = None

    def __str__(self):
        str = "["
        for node in self:
            str = "{0} {1}".format(str, node)

        str += " ]"
        return str

    def __iter__(self):
        self.current = self.head
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration

        cur = self.current
        self.current = cur.next
        return cur

    def insert_end(self, value):
        if(self.head == None):
            self.head = Node(value)
            self.tail = self.head
        else:
            tailN = Node(value)
            self.tail.next = tailN
            self.tail = tailN

    def find(self, value):
        for node in self:
            if value == node.val:
                return node

        return None

    def find_prev(self, value):
        prev = None
        for node in self:
            if value == node.val:
                return prev

            prev = node


ll = SinglyLinkedList()
t1 = time.time()

for i in range(1, 10000):
    ll.insert_end(randint(1000000000, 9999999999))

t2 = time.time()
print("Insert Time =", (t2-t1))

t1 = time.time()
print(ll)

print("Find time: ", (t1-t2))
