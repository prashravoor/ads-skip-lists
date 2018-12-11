class SingleLinkNode(object):
    def __init__(self, value):
        self.value = value
        self.next = None

class DoubleLinkNode(SingleLinkNode):
    def __init__(self, value):
        super(value)
        self.prev = None

class LinkedList(object):
    def __init(self, name):
        self.name = name
        self.head = None
        self.current = None # For the iterator
