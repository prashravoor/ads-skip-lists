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
        self.levels = -1
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
            "Find_Pred for value {0} in Skip List {1} at level {2}".format(value, self.name, stop_at_level))
        node = SkipListNode(value)

        # Start from the head, and keep moving next
        current = self.find_top()
        level = self.levels
        prev = None

        while level >= stop_at_level:
            prev = None
            logging.debug(
                "Traversing level {0} in skip list {1}".format(level, self.name))
            while current and current < node:
                prev = current
                current = current.next

            logging.debug("Stopped at {0} on level {1}, prev is {2}".format(
                current, level, prev))
            if current and current < node:
                logging.debug("Moving down from node {0} at level {1} to node {2}".format(current, level, current.down))
                current = current.down
            elif prev:
                logging.debug("Prev: Moving down from node {0} at level {1} to node {2}".format(prev, level, prev.down))
                current = prev.down
            else:
                # Reset to head of next level
                current = self.heads[level - 1]
            level -= 1

        logging.debug(
            "Returning {0} as predecessor for value {1}".format(prev, value))
        return prev

    def simple_insert(self, startNode, value):
        logging.debug("Simple Insert of value {0} in Skip List {1} starting from node {2}".format(
            value, self.name, startNode))
        node = SkipListNode(value)

        current = startNode
        prev = None
        while current and current < node:
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

        return startNode

    def insert(self, value):
        logging.debug(
            "Starting Insert on list {0} for value {1}".format(self.name, value))

        # Start from top most level, find where to insert
        current = self.find_top()

        if current == None:
            # First node insert
            self.heads.append(self.simple_insert(current, value))
            self.size = 1
            self.levels = 0
            return

        # Find number of levels
        if self.size < 2:
            num_of_levels = 0
        else:
            num_of_levels = random.randint(0, floor(log2(self.size)))

        logging.info("Node {0} will be in {1} levels".format(
            value, num_of_levels))

        level = 0
        prev_node = None
        while level <= num_of_levels:
            prev = self.find_pred(value, level)
            node = SkipListNode(value)
            if not prev:
                logging.debug(
                    "Node {0} is the least value in the list at level {1}".format(value, level))
                # Insert at head of level
                if len(self.heads) <= level:
                    logging.debug("Adding a head node at level {0}")
                    self.heads.append(None)
                    self.levels += 1

                node.next = self.heads[level]
                self.heads[level] = node

                logging.debug("Current Heads: {0}, Levels: {1}".format(self.heads, self.levels))

            else:
                logging.debug(
                    "Node {0} will be inserted after {1} at level {2}".format(value, prev, level))
                node.next = prev.next
                prev.next = node

            node.down = prev_node
            if prev_node:
                prev_node.up = node
            prev_node = node
            level += 1

        self.size += 1
