import logging
import random
from math import log2, floor


class SkipListNode(object):
    def __init__(self, value):
        logging.debug(
            "Created A new Skip List node with value {0}".format(value))
        self.value = value
        self.prev = None
        self.next = None
        self.up = None
        self.down = None

    def __repr__(self):
        return '{0}'.format(self.value)

    def __eq__(self, other):
        if other == None:
            return False

        return other.value == self.value

    def __lt__(self, other):
        if other == None:
            return False

        return self.value < other.value

    def __ge__(self, other):
        if other == None:
            return False
        return self.value >= other.value

    def __le__(self, other):
        if other == None:
            return False

        return self.value <= other.value

    def getZeroLevelNode(self):
        current = self
        while current.down != None:
            current = current.down

        logging.debug(
            "The Zero Level node was found to be: {0}".format(current))
        return current


class SinglyLinkedSkipList(object):
    def __init__(self, name):
        logging.debug(
            "Creating a new Singly Linked Skip List of name {0}".format(name))
        self.name = name
        self.heads = []
        self.levels = 0
        self.size = 0

    def getSimpleTraversal(self, node):
        logging.debug("Starting simple traversal from node {0}".format(node))
        str = ""
        while node != None:
            str += "{0} ".format(node)
            node = node.next

        return str

    def __str__(self):
        str = "Skip List {0}, Heads {1}, Levels {2}, Length {3}\n".format(
            self.name, self.heads, self.levels, self.size)

        level = 0
        for current in self.heads:
            logging.debug("Printing level {0}".format(level))
            str += "Level {0}: [ ".format(level)
            str += self.getSimpleTraversal(current)
            str += "]\n"
            level = level + 1

        return str

    def __iter__(self):
        if self.heads.count() == 0:
            return None

        self.current = self.heads[1]
        return self

    def __next__(self):
        if self.current == None:
            raise StopIteration
        else:
            tmp = self.current
            self.current = self.current.next
            return tmp

    def length(self):
        logging.debug("Current length of skip list {0} is {1}".format(
            self.name, self.size))
        return self.size

    def find_top(self):
        if self.size == 0:
            logging.debug("Find Top returns {0}".format(None))
            return None

        logging.debug("Find Top returns {0}".format(self.heads[self.levels]))
        return self.heads[self.levels]

    def find_pred(self, value, stop_at_level=0):
        logging.debug(
            "Find_Pred for value {0} in Skip List {1}".format(value, self.name))
        node = SkipListNode(value)

        # Start from the head, and keep moving next
        prev = None
        current = self.find_top()
        level = self.levels

        while current != None:
            if current.next == None and level > stop_at_level:
                logging.debug(
                    "Reached end of level {0}, Going down at node {1}".format(level, current))
                current = current.down
                level = level - 1
            elif current.next == None and level == stop_at_level:
                logging.debug(
                    "Found place to insert at level {0}, after node {1}".format(level, current))
                return (current, None)
            elif current.next < node:
                current = current.next
            elif current.down == None:
                logging.debug(
                    "Found Predecessor node {0} at level {1}".format(prev, level))
                return (prev, current)
            else:
                logging.debug("Node {0} is greater than value of node {1}, going down from level {2}".format(
                    current.next, node, level))
                current = current.down
                level = level - 1

            prev = current

        logging.info(
            "Value {0} was not found in Skip List {1}".format(value, self.name))
        return (None, None)

    def simple_insert(self, startNode, value):
        logging.debug("Simple Insert of value {0} in Skip List {1} starting from node {2}".format(
            value, self.name, startNode))
        node = SkipListNode(value)

        current = startNode
        prev = None
        while current != None and current < node:
            prev = current
            current = current.next

        if prev == None:
            logging.debug(
                "Value {0} is the least value in the list".format(value))
            node.next = startNode
            startNode = node
        else:
            logging.debug(
                "Found Previous Node to be {0} for value {1}".format(prev, value))
            node.next = prev.next
            prev.next = node

        self.size += 1
        return startNode

    def insert(self, value):
        logging.debug(
            "Starting Insert on list {0} for value {1}".format(self.name, value))

        # Start from top most level, find where to insert
        current = self.find_top()

        if current == None:
            # First node insert
            self.heads.append(self.simple_insert(current, value))
            return

        # Find number of levels
        if self.size < 2:
            num_of_levels = 0
        else:
            num_of_levels = random.randint(0, floor(log2(self.size)))

        logging.info("Node {0} will be in {1} levels".format(
            value, num_of_levels + 1))

        top = None
        at_level = num_of_levels
        while at_level >= 0:
            node = SkipListNode(value)
            if self.levels < at_level:
                # Insert node at the head of the missing level
                logging.info("Adding missing level {0}".format(self.levels))
                self.heads.append(node)
                self.levels += 1
            else:
                (prev, next) = self.find_pred(value, at_level)
                logging.debug("Inserting node {0} in between elements {1} and {2} at level {3}".format(
                    value, prev, next, at_level))
                node.next = next
                if prev:
                    prev.next = node
                else:
                    self.heads[at_level] = node

            self.size += 1

            node.up = top
            if node.up:
                node.up.bottom = node
            top = node
            at_level -= 1
