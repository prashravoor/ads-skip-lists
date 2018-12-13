import logging
import random
from math import log2, floor

logger = logging.getLogger()

class SkipListNode(object):
    def __init__(self, value):
        logger.debug(
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

        logger.debug(
            "The Zero Level node was found to be: {0}".format(current))
        return current


class SinglyLinkedSkipList(object):
    def __init__(self, name):
        logger.debug(
            "Creating a new Singly Linked Skip List of name {0}".format(name))
        self.name = name
        self.heads = []
        self.levels = -1
        self.size = 0
        self.type = "Singly Linked"

    def getSimpleTraversal(self, node):
        logger.debug("Starting simple traversal from node {0}".format(node))
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
            logger.debug("Printing level {0}".format(level))
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
        logger.debug("Current length of skip list {0} is {1}".format(
            self.name, self.size))
        return self.size

    def getNodesInLevel(self, level):
        if level < 0 or level > self.levels:
            return -1

        i = 0
        current = self.heads[level]
        while current:
            i += 1
            current = current.next
        logger.debug("Found {} nodes in level {}".format(i, level))
        return i

    def getLevelTraversal(self, level):
        if level < -1 or level > self.levels:
            return "Invalid level {}, current number of levels is {}".format(level, self.levels)

        if level == -1:
            return ""

        return self.getSimpleTraversal(self.heads[level])

    def getTraversal(self, from_val, to_val):
        if self.size == 0 or self.size < from_val:
            return "None"

        logger.debug("Traversal from index {} to index {} in list {}".format(
            from_val, to_val, self.name))
        i = 0
        str = "[ "
        current = self.heads[0]
        while i < from_val:
            i += 1
            current = current.next

        while current and i < self.size and i < to_val:
            str += "{} ".format(current)
            current = current.next
            i += 1
        str += "]"
        return str

    def find_top(self):
        if self.size == 0:
            logger.debug("Find Top returns {0}".format(None))
            return None
        logger.debug("Find Top returns {0}".format(self.heads[self.levels]))
        return self.heads[self.levels]

    def find_pred(self, value, stop_at_level=0):
        logger.debug(
            "Find_Pred for value {0} in Skip List {1} at level {2}".format(value, self.name, stop_at_level))
        node = SkipListNode(value)

        # Start from the head, and keep moving next
        current = self.find_top()
        level = self.levels
        prev = None

        while level >= stop_at_level:
            prev = None
            logger.debug(
                "Traversing level {0} in skip list {1}".format(level, self.name))
            while current and current < node:
                prev = current
                current = current.next

            logger.debug("Stopped at {0} on level {1}, prev is {2}".format(
                current, level, prev))
            if current and current < node:
                logger.debug("Moving down from node {0} at level {1} to node {2}".format(
                    current, level, current.down))
                current = current.down
            elif prev:
                logger.debug("Prev: Moving down from node {0} at level {1} to node {2}".format(
                    prev, level, prev.down))
                current = prev.down
            else:
                # Reset to head of next level
                current = self.heads[level - 1]
            level -= 1

        logger.debug(
            "Returning {0} as predecessor for value {1}".format(prev, value))
        return prev

    def simple_insert(self, startNode, value):
        logger.debug("Simple Insert of value {0} in Skip List {1} starting from node {2}".format(
            value, self.name, startNode))
        node = SkipListNode(value)

        current = startNode
        prev = None
        while current and current < node:
            prev = current
            current = current.next

        if prev == None:
            logger.debug(
                "Value {0} is the least value in the list".format(value))
            node.next = startNode
            startNode = node
        else:
            logger.debug(
                "Found Previous Node to be {0} for value {1}".format(prev, value))
            node.next = prev.next
            prev.next = node

        return startNode

    def insert(self, value):
        logger.debug(
            "Starting Insert on list {0} for value {1}".format(self.name, value))

        # Start from top most level, find where to insert
        current = self.find_top()

        if current == None:
            # First node insert
            self.heads.append(self.simple_insert(current, value))
            self.size = 1
            self.levels = 0
            return True

        if self.find(value):
            logger.info("Found {} in the list, skipping this value as duplicate".format(value))
            return False

        # Find number of levels
        if self.size < 2:
            num_of_levels = 0
        else:
            num_of_levels = random.randint(0, floor(log2(self.size)))

        logger.info("Node {0} will be in {1} levels".format(
            value, num_of_levels))

        level = 0
        prev_node = None
        while level <= num_of_levels:
            prev = self.find_pred(value, level)
            node = SkipListNode(value)
            if not prev:
                logger.debug(
                    "Node {0} is the least value in the list at level {1}".format(value, level))
                # Insert at head of level
                if len(self.heads) <= level:
                    logger.debug("Adding a head node at level {0}")
                    self.heads.append(None)
                    self.levels += 1

                node.next = self.heads[level]
                self.heads[level] = node

                logger.debug("Current Heads: {0}, Levels: {1}".format(
                    self.heads, self.levels))

            else:
                logger.debug(
                    "Node {0} will be inserted after {1} at level {2}".format(value, prev, level))
                node.next = prev.next
                prev.next = node

            node.down = prev_node
            if prev_node:
                prev_node.up = node
            prev_node = node
            level += 1

        self.size += 1
        return True

    def find(self, value):
        logger.debug(
            "Finding value {} in Skip List {}".format(value, self.name))
        node = SkipListNode(value)
        pred = self.find_pred(value)
        if not pred:
            logger.debug("Previous was None, checking for the head value {}".format(self.heads))
            # Check first node at level 0
            if len(self.heads) > 0 and self.heads[0] == node:
                return self.heads[0]
        elif pred.next == node:
            return pred.next

        return None

    def delete(self, value):
        logger.debug(
            "Deleting value {} in Skip List {}".format(value, self.name))
        node = SkipListNode(value)

        level = self.levels
        deleted = False
        while level >= 0:
            pred = self.find_pred(value, level)
            if not pred:
                # Check for head
                if self.heads[level] == node:
                    logger.debug(
                        "Found the node {} at the head of level {}".format(value, level))
                    self.heads[level] = self.heads[level].next
                    deleted = True
                else:
                    logger.debug(
                        "Node {} was not found at level {}".format(value, level))
            else:
                if pred.next == node:
                    logger.debug(
                        "Found node {} at level {}".format(value, level))
                    pred.next = pred.next.next
                    deleted = True
                else:
                    logger.debug(
                        "Node {} was not found at level {}".format(value, level))
            level -= 1

        # Adjust number of levels
        while not self.find_top() and self.levels >= 0:
            logging.debug("Removing head")
            self.heads.pop()
            self.levels -= 1

        if deleted:
            self.size -= 1
            return True
        return False


class DoublyLinkedSkipList(SinglyLinkedSkipList):
    def __init__(self, name):
        SinglyLinkedSkipList.__init__(self, name)
        logger.debug("Created a doubly linked skip list of name: " + name)
        self.type = "Doubly Linked"

    def find_pred(self, value, stop_at_level=0):
        logger.debug(
            "Find_Pred for value {} in Doubly Linked Skip List {} at level {}".format(value, self.name, stop_at_level))
        node = SkipListNode(value)

        # Start from the head, and keep moving next
        current = self.find_top()
        level = self.levels
        prev = None
        while level >= stop_at_level:
            logger.debug(
                "Traversing level {0} in skip list {1}".format(level, self.name))
            while current and current.next and current < node:
                current = current.next

            if current:
                prev = current.prev

            logger.debug("Stopped at {0} on level {1}, prev is {2}".format(
                current, level, prev))
            if current and current < node:
                logger.debug("Moving down from node {0} at level {1} to node {2}".format(
                    current, level, current.down))
                prev = current
                current = current.down
            elif current and current > node:
                logger.debug("Moving back from node {} at level {}".format(current, level))
                while current.prev and current > node:
                    current = current.prev
                logger.debug("Stopped at node {} at level {}".format(current, level))
                if current > node:
                    prev = current.prev
                else:
                    prev = current
                logger.debug("Moving down from current node {} to {}".format(current, current.down))
                current = current.down
            elif current:
                current = current.down

            level -= 1

        logger.debug(
            "Returning {0} as predecessor for value {1}".format(prev, value))
        return prev

    def insert(self, value):
        logger.debug(
            "Starting Insert on Doubly Linked list {0} for value {1}".format(self.name, value))

        # Start from top most level, find where to insert
        current = self.find_top()

        if current == None:
            # First node insert
            self.heads.append(self.simple_insert(current, value))
            self.size = 1
            self.levels = 0
            return True

        if self.find(value):
            logger.info("Found {} in the list, skipping this value as duplicate".format(value))
            return False

        # Find number of levels
        if self.size < 2:
            num_of_levels = 0
        else:
            num_of_levels = random.randint(0, floor(log2(self.size)))

        logger.info("Node {0} will be in {1} levels".format(
            value, num_of_levels))

        level = 0
        prev_node = None
        while level <= num_of_levels:
            prev = self.find_pred(value, level)
            node = SkipListNode(value)
            if not prev:
                logger.debug(
                    "Node {0} is the least value in the list at level {1}".format(value, level))
                # Insert at head of level
                if len(self.heads) <= level:
                    logger.debug("Adding a head node at level {0}")
                    self.heads.append(None)
                    self.levels += 1

                node.next = self.heads[level]
                if self.heads[level]:
                    self.heads[level].prev = node
                self.heads[level] = node

                logger.debug("Current Heads: {0}, Levels: {1}".format(
                    self.heads, self.levels))
            else:
                logger.debug(
                    "Node {0} will be inserted after {1} at level {2}".format(value, prev, level))
                node.next = prev.next
                if prev.next:
                    prev.next.prev = node
                prev.next = node
                node.prev = prev

            node.down = prev_node
            if prev_node:
                prev_node.up = node
            prev_node = node
            level += 1

        self.size += 1
        return True
