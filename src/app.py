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

from argparse import ArgumentParser
from skip_list import SinglyLinkedSkipList
import logging

parser = ArgumentParser()
logLevel = "DEBUG"
parser.add_argument('--log')
args = parser.parse_args()
logLevel = args.log

if logLevel != None:
    numLogLevel = getattr(logging, logLevel.upper())
    logging.basicConfig(level=numLogLevel)

ll = SinglyLinkedSkipList("Test")
t1 = time.time()

for i in range(0, 1000000):
    ll.head = ll.simple_insert(ll.head, randint(1000000000, 9999999999))

t2 = time.time()
print("Insert Time =", (t2-t1))

t1 = time.time()
print("Node Output: {0}".format(ll))

print("Find time: ", (t1-t2))
