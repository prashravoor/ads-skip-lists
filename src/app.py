import pygubu
import tkinter as tk
import csv
import logging
from skip_list import SinglyLinkedSkipList
from argparse import ArgumentParser
import time
from random import randint
import tkinter.simpledialog

logger = logging.getLogger()


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
        # master.withdraw()
        builder.add_from_file('../GUI.ui')
        self.toplevel = builder.get_object('toplevel', master)
        # Connect Delete event to a toplevel window
        master.withdraw()
        self.toplevel.master.protocol("WM_DELETE_WINDOW", self.on_close_window)
        builder.connect_callbacks(self)
        self.lists = {}
        self.trace_mode = False
        self.selected_list = None

        self.status_text = builder.get_object("statustext")
        self.num_of_nodes = builder.get_object('numnodes')
        self.num_of_levels = builder.get_object('numlevels')
        self.find_nodes_in_level_in = builder.get_object('findnodesinlevel')
        self.find_nodes_in_level_out = builder.get_object('numnodesinlevel')
        self.selected_skip_list = builder.get_object('selectedskiplist')
        self.set_trace = builder.get_object('tracemode')

        self.clearAll()

    def quit(self, event=None):
        self.toplevel.quit()

    def run(self):
        self.toplevel.mainloop()

    def appendMessage(self, message):
        self.status_text.configure(state="normal")
        self.status_text.insert(tk.END, "{}\n".format(message))
        self.status_text.see(tk.END)
        self.status_text.configure(state="disabled")

    def clearStatus(self):
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", tk.END)
        self.status_text.configure(state="disabled")

    def clearLabels(self):
        self.num_of_nodes['text'] = ''
        self.num_of_levels['text'] = ''
        self.find_nodes_in_level_in.delete('0', tk.END)
        self.find_nodes_in_level_in.insert(tk.END, 0)
        self.find_nodes_in_level_out['text'] = 0
        self.selected_skip_list['text'] = ''
        self.selected_list = None

    def clearAll(self):
        self.clearStatus()
        self.clearLabels()

    def on_close_window(self, event=None):
        print('On close window')
        # Call destroy on toplevel to finish program
        self.toplevel.master.destroy()

    def CreateList(self):
        result = tk.simpledialog.askstring(
            'Skip List Name', 'Enter Skip List Name', parent=None)
        if not result:
            self.appendMessage("No List was Created")
            return None
        try:
            self.CreateListNamed(result)
            self.appendMessage(
                "Successfully created skip list with name {}".format(result))
        except ValueError:
            self.appendMessage(
                "Failed to create skip list {}, it already exists!".format(result))

    def CreateListNamed(self, name, mode="single"):
        try:
            self.GetListNamed(name)
            logger.error(
                "There is already a skip list with name: {0}".format(name))
        except ValueError:
            logger.info("Created new Skip List")
            self.lists[name] = SinglyLinkedSkipList(name)
            return
        raise ValueError

    def ListNames(self):
        self.appendMessage(
            "Currently Available Lists: {}".format(list(self.lists.keys())))

    def DeleteList(self):
        result = tk.simpledialog.askstring(
            'Delete Skip List', 'Enter Skip List Name', parent=None)
        if not result:
            self.appendMessage("No List was Deleted")
            return None
        try:
            self.lists.pop(result)
            self.appendMessage(
                "Successfully deleted skip list with name {}".format(result))
            if self.selected_list.name == result:
                self.clearLabels()
        except KeyError:
            self.appendMessage("Skip List {} does not exist".format(result))

    def getNodesInLevelVal(self):
        level = self.builder.get_variable('nodes_in_level').get()
        try:
            level = int(level)
            if level < 0:
                raise ValueError
            return level
        except ValueError:
            self.appendMessage("Invalid Integer {}".format(level))
            raise ValueError

    def setLabels(self):
        logger.debug("Set Labels called")
        if self.selected_list:
            self.num_of_nodes['text'] = "{}".format(
                self.selected_list.length())
            self.num_of_levels['text'] = "{}".format(self.selected_list.levels)
            try:
                self.find_nodes_in_level_out['text'] = "{}".format(
                    self.selected_list.getNodesInLevel(self.getNodesInLevelVal()))
            except ValueError:
                self.appendMessage("The value entered is not valid")

    def SelectSkipList(self):
        result = tk.simpledialog.askstring(
            'Select Skip List', 'Enter Skip List Name', parent=None)
        if not result:
            self.appendMessage("No List was Selected")
            return None
        try:
            self.selected_list = self.lists[result]
            self.appendMessage("Skip List {} selected".format(result))
            self.selected_skip_list['text'] = result
            self.setLabels()
        except KeyError:
            self.appendMessage("Skip List {} does not exist".format(result))

    def FindNumNodesInLevel(self):
        if not self.selected_list:
            self.appendMessage("You need to select a skip list first")
            return

        self.setLabels()

    def ShowNodesInLevel(self):
        if not self.selected_list:
            self.appendMessage("You need to select a skip list first")
            return

        try:
            level = self.getNodesInLevelVal()
        except ValueError:
            self.appendMessage("The value entered is invalid")
            return

        self.appendMessage("Displaying Nodes in Level {}\n\n{}".format(
            level, self.selected_list.getLevelTraversal(level)))

    def InsertItem(self):
        if not self.selected_list:
            self.appendMessage("You need to select a skip list first")
            return

        result = tk.simpledialog.askinteger(
            'Insert into Skip List', 'Enter Integer Value', parent=None)
        self.appendMessage("Added item {} into Skip List {}".format(
            result, self.selected_list.name))

        if not result:
            self.appendMessage("No item was added")
            return

        self.selected_list.insert(result)
        self.setLabels()
        if self.trace_mode:
            self.appendMessage("{}".format(self.selected_list))

    def GetList(self):
        if not self.selected_list:
            name = tk.simpledialog.askstring("Get List", "List Name")
        else:
            name = self.selected_list.name
        try:
            self.appendMessage(self.GetListNamed(name))
        except ValueError:
            self.appendMessage("List {} does not exist".format(name))

    def GetListNamed(self, name):
        logger.info("Getting list {0}".format(name))
        if not name in self.lists:
            raise ValueError

        return self.lists[name]

    def ShowListNamed(self, name):
        logger.info("Showing list {0}".format(name))
        return "{0}".format(self.GetListNamed(name))

    def CreateData(self, filename, numKeys):
        f = open(filename, "w", newline="")
        writer = csv.writer(f)

        logger.info("Creating {0} keys in file {1}".format(numKeys, filename))
        keys = []
        for i in range(1, numKeys):
            keys.append(randint(1000000000, 9999999999))

        writer.writerows(keys)

    def ReadFromCsvFile(self, filename):
        f = open(filename, "r")
        reader = csv.reader(f)
        keys = []

        logger.info("Reading all integers from file {0}".format(filename))
        for key in reader:
            keys.append(key)

        logger.info("Found {0} keys in file {1}".format(len(keys), filename))
        return keys

    def SetTrace(self):
        self.trace_mode = self.builder.get_variable('set_trace').get()
        print("Set Trace Mode to {}".format(self.trace_mode))


if __name__ == '__main__':
    parser = ArgumentParser()
    logLevel = "DEBUG"
    parser.add_argument('--log')
    args = parser.parse_args()
    logLevel = args.log

    if logLevel != None:
        numLogLevel = getattr(logging, logLevel.upper())
        logging.basicConfig(level=numLogLevel)
        logger.setLevel(numLogLevel)

    root = tk.Tk()
    app = Application(root)
    app.run()
