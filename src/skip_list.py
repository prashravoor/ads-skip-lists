import logging


class SkipListNode(object):
    def __init__(self, value):
        logging.debug(
            "Created A new Skip List node with value {0}".format(value))
        self.value = value
        self.prev = None
        self.next = None
        self.up = None
        self.down = None

    def __str__(self):
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
        self.head = None  # Head node always appears in all levels
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
        logging.debug("entered string rep")
        str = "Skip List {0}\n".format(self.name)
        current = self.head
        level = 0
        while current != None:
            logging.debug("Printing level {0}".format(level))
            str += "Level {0}: [ ".format(level)
            str += self.getSimpleTraversal(current)
            str += "]\n"
            current = current.up
            level = level + 1

        logging.debug("Levels: {0}".format(level))
        return str

    def __iter__(self):
        self.current = self.head
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

    def simple_find(self, node):
        logging.debug(
            "Running simple find for {0} in Skip List {1}".format(node, self.name))
        current = self.head
        while current != None and current != node:
            current = current.next

        logging.debug("Found node to be: {0}".format(current))
        return current

    def find_pred(self, value):
        logging.debug(
            "Find_Pred for value {0} in Skip List {1}".format(value, self.name))
        node = SkipListNode(value)

        # Start from the head, and keep moving next
        prev = None
        current = self.head

        level = 0
        while current != None and current.up != None:
            current = current.up
            level = level + 1

        while current != None:
            # if current == node:
            #    logging.debug("Found node at level {0}".format(level))
            #    return prev

            prev = current
            if current.next == None:
                logging.debug(
                    "Reached end of level {0}, Going down at node {1}".format(level, current))
                current = current.down
                level = level - 1
            elif current.next <= node:
                current = current.next
            elif current.down == None:
                logging.debug(
                    "Found Predecessor node {0} at level {1}".format(prev, level))
                return prev
            else:
                logging.debug("Node {0} is greater than value of node {1}, going down from level {2}".format(
                    current.next, node, level))
                current = current.down
                level = level - 1

        logging.info(
            "Value {0} was not found in Skip List {1}".format(value, self.name))
        return None

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
            return node
        else:
            logging.debug(
                "Found Previous Node to be {0} for value {1}".format(prev, value))
            node.next = prev.next
            prev.next = node

        return startNode
