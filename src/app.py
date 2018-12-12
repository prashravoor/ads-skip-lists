import pygubu
import tkinter as tk
import csv
import logging
from skip_list import SinglyLinkedSkipList
from argparse import ArgumentParser
import time
from random import randint
import tkinter.simpledialog

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


parser = ArgumentParser()
logLevel = "DEBUG"
parser.add_argument('--log')
args = parser.parse_args()
logLevel = args.log

if logLevel != None:
    numLogLevel = getattr(logging, logLevel.upper())
    logging.basicConfig(level=numLogLevel)

#ll = SinglyLinkedSkipList("Test")

#t1 = time.time()
# for i in range(1, 1000):
    #ll.insert(randint(1000000000, 9999999999))
    #ll.insert(randint(-1000, 1000))
    #print("After Insert, LL Is: {0}".format(ll))
#t2 = time.time()
#print("The Linked List is now:")
# print(ll)

#print("Insert Time For Skip List =", (t2-t1))


class Application(pygubu.TkApplication):
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        #master.withdraw()
        builder.add_from_file('../GUI.ui')
        self.mainwindow = builder.get_object('mainwindow', master)
        # Connect Delete event to a toplevel window
        master.protocol("WM_DELETE_WINDOW", self.on_close_window)
        builder.connect_callbacks(self)
        self.lists = {}
        self.trace_mode = False

    def quit(self, event=None):
        self.mainwindow.quit()

    def on_close_window(self, event=None):
        print('On close window')
        # Call destroy on toplevel to finish program
        self.mainwindow.master.destroy()

    def CreateList(self):
        result = tk.simpledialog.askstring('List Name', 'Enter the Name', parent=None)
        self.CreateListNamed(result)

    def CreateListNamed(self, name, mode="single"):
        try:
            self.GetList(name)
            logging.error(
                "There is already a skip list with name: {0}".format(name))
        except ValueError:
            logging.info("Created new Skip List")
            self.lists[name] = SinglyLinkedSkipList(name)
            return
        raise ValueError

    def GetList(self, name):
        logging.info("Getting list {0}".format(name))
        return self.lists[name]

    def ShowList(self, name):
        logging.info("Showing list {0}".format(name))
        return "{0}".format(self.GetList(name))

    def DeleteList(self, name):
        logging.info("Deleting list {0}".format(name))
        self.lists.popitem(name)

    def CreateData(self, filename, numKeys):
        f = open(filename, "w", newline="")
        writer = csv.writer(f)

        logging.info("Creating {0} keys in file {1}".format(numKeys, filename))
        keys = []
        for i in range(1, numKeys):
            keys.append(randint(1000000000, 9999999999))

        writer.writerows(keys)

    def ReadFromCsvFile(self, filename):
        f = open(filename, "r")
        reader = csv.reader(f)
        keys = []

        logging.info("Reading all integers from file {0}".format(filename))
        for key in reader:
            keys.append(key)

        logging.info("Found {0} keys in file {1}".format(len(keys), filename))
        return keys

    def SetTrace(self, value):
        self.trace_mode = value


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
