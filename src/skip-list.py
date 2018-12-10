class SkipListNode(object):
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
        self.up = None
        self.down = None

    def __str__(self):
        return ''.join(self.value)

    def __eq__(self, other):
        return other.value == self.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value

    def getZeroLevelNode(self):
        current = self
        while current.down != None:
            current = current.down

        return current

class SinglyLinkedSkipList(object):
    def __init__(self, name):
        self.name = name
        self.head = None # Head node always appears in all levels
        self.levels = 0
        self.size = 0

    def __str__(self):
        str = "Skip List ".join(self.name).join(" [")
        for node in self:
            str += '{0} '.format(node)
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
        return self.size

    def find_prev(self, value):
        node = SkipListNode(value)

        # Start from the head, and keep moving next
        prev = None
        current = self.head

        while current != None and current.up != None:
            current = current.up

        while current != None:
            if current == node:
                return prev

            prev = current

            if current.next == None:
                current = current.down
            elif current.next <= node:
                current = current.next
            else:
                current = current.down

        return None

