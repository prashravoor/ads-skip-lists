import pygubu
import tkinter as tk
from tkinter import filedialog
import csv
import logging
from skip_list import SinglyLinkedSkipList, DoublyLinkedSkipList
from argparse import ArgumentParser
import time
from random import randint
import tkinter.simpledialog

logger = logging.getLogger()


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

    def CreateSlList(self):
        result = tk.simpledialog.askstring(
            'Singly Linked Skip List Name', 'Enter Skip List Name', parent=None)
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

    def CreateDlList(self):
        result = tk.simpledialog.askstring(
            'Doubly Linked Skip List Name', 'Enter Skip List Name', parent=None)
        if not result:
            self.appendMessage("No List was Created")
            return None
        try:
            self.CreateListNamed(result, "double")
            self.appendMessage(
                "Successfully created skip list with name {}".format(result))
        except ValueError:
            self.appendMessage(
                "Failed to create skip list {}, it already exists!".format(result))

    def CreateListNamed(self, name, mode="single"):
        try:
            self.lists[name]
            logger.error(
                "There is already a skip list with name: {0}".format(name))
        except KeyError:
            logger.info("Created new Skip List of type {} linked".format(mode))
            if "double" == mode:
                self.lists[name] = DoublyLinkedSkipList(name)
            else:
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
            self.selected_skip_list['text'] = result + ", Type: " + self.selected_list.type
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
        result = int(result)

        t1 = time.clock()
        inserted = self.selected_list.insert(result)
        t2 = time.clock()
        self.setLabels()
        if self.trace_mode:
            if inserted:
                self.appendMessage("{}".format(self.selected_list))
            else:
                self.appendMessage("Skipping duplicate item {}".format(result))
        self.appendMessage("Item {} inserted in {} seconds".format(result, (t2 - t1)))

    def ShowListDiag(self):
        diag = self.builder.get_object('showlist')
        name = self.builder.get_variable('list_name').get()
        from_val = self.builder.get_variable('from_node_val').get()
        show_all_levels = self.builder.get_variable('show_all_levels').get()
        logger.debug("Show All Levels has been set to {}".format(show_all_levels))

        if show_all_levels:
            logger.debug("Show All Levels has been set, returning the full list")
            self.appendMessage("{}".format(self.selected_list))
            diag.close()

        try:
            from_val = int(from_val)
        except:
            self.appendMessage("Invalid value specified for from index")
            diag.close()
            return

        to_val = self.builder.get_variable('to_node_val').get()
        if "END" == to_val:
            to_val = 10000000
        try:
            to_val = int(to_val)
        except:
            self.appendMessage("Invalid value specified for to index")
            diag.close()
            return

        logger.debug("Displaying list {} from index {} to index {}".format(
            name, from_val, to_val))
        try:
            list = self.lists[name]
            self.appendMessage(list.getTraversal(from_val, to_val))
        except KeyError:
            self.appendMessage("List {} does not exist".format(name))
        diag.close()

    def GetList(self):
        diag = self.builder.get_object('showlist')
        self.builder.get_object('showlistbtn').configure(
            command=self.ShowListDiag)
        diag.run()

    def CreateData(self):
        dialog = self.builder.get_object('createdatadiag')
        self.builder.get_object('ok').configure(command=self.CreateDataFile)
        dialog.run()

    def ReadFromCsvFile(self):
        if not self.selected_list:
            self.appendMessage("You need to select a Skip List first")
            return
        filename = filedialog.askopenfilename(
            initialdir=".", title="Select File to read from")
        if not filename:
            self.appendMessage("No values read")
            return
        elif ".csv" not in filename:
            self.appendMessage("Only CSV files are allowed")
            return

        f = open(filename, "r")
        reader = csv.reader(f, delimiter=",")
        keys = []

        logger.info("Reading all integers from file {0}".format(filename))
        for key in reader:
            keys.append(key)

        if not keys or len(keys) <= 0:
            self.appendMessage("No Keys found in the file")
            return

        keys = keys[0]

        logger.info("Found {0} keys in file {1}".format(len(keys), filename))
        logger.debug("Keys: {}".format(keys))

        t1 = time.clock()
        for key in keys:
            try:
                key = int(key)
                inserted = self.selected_list.insert(int(key))
                if self.trace_mode:
                    if inserted:
                        self.appendMessage(
                            "Inserted Key {}, the list is now {}".format(key, self.selected_list))
                    else:
                        self.appendMessage("Skipping duplicate node {}".format(key))
            except:
                logger.error(
                    "Found invalid key {} in file, skipping it".format(key))
        self.setLabels()
        t2 = time.clock()
        self.appendMessage(
            "Total time to insert {} keys: {} seconds".format(len(keys), (t2 - t1)))

    def SetTrace(self):
        self.trace_mode = self.builder.get_variable('set_trace').get()
        print("Set Trace Mode to {}".format(self.trace_mode))

    def CreateDataFile(self):
        logger.info("Creating Data File")
        filename = self.builder.get_variable('create_data_filename').get()
        numKeys = self.builder.get_variable('num_keys_val').get()

        if not filename:
            self.appendMessage("Invalid Filename specified")
            return

        if numKeys < 0:
            self.appendMessage("Invalid integer {}".format(numKeys))
            return

        try:
            f = open(filename, "w", newline="")
            writer = csv.writer(f, delimiter=",")

            logger.info("Creating {0} keys in file {1}".format(
                numKeys, filename))
            keys = []
            i = 0
            while i < numKeys:
                keys.append(randint(1000000000, 9999999999))
                #keys.append(randint(10, 99))
                i += 1

            writer.writerow(keys)
            self.appendMessage(
                "Wrote {} keys to file {}".format(numKeys, filename))
        except Exception as ex:
            self.appendMessage(
                "An Exception has occurred while creating the data file: {}".format(ex))

        dialog = self.builder.get_object('createdatadiag')
        dialog.close()

    def DeleteNode(self):
        if not self.selected_list:
            self.appendMessage("You need to select a skip list first")
            return

        result = tk.simpledialog.askinteger(
            'Delete Node in Skip List', 'Enter Integer Value', parent=None)

        if not result:
            self.appendMessage("No item was deleted")
            return
        result = int(result)

        t1 = time.clock()
        deleted = self.selected_list.delete(result)
        t2 = time.clock()
        if deleted:
            self.appendMessage("Deleted item {} from Skip List {} in {} seconds".format(
                result, self.selected_list.name, (t2 - t1)))
            self.setLabels()
            if self.trace_mode:
                self.appendMessage("{}".format(self.selected_list))
        else:
            self.appendMessage("Item {} was not found in the skip list {}".format(
                result, self.selected_list.name))

    def FindNode(self):
        if not self.selected_list:
            self.appendMessage("You need to select a skip list first")
            return

        result = tk.simpledialog.askinteger(
            'Find Node in Skip List', 'Enter Integer Value', parent=None)

        if not result:
            self.appendMessage("No item was added")
            return
        result = int(result)

        t1 = time.clock()
        node = self.selected_list.find(result)
        t2 = time.clock()
        if not node:
            self.appendMessage("Item {} was not found Skip List {}".format(
                result, self.selected_list.name))
        else:
            self.appendMessage("Item {} was found in the skip list {}, Previous Node: {}, Next Node: {}".format(
                result, self.selected_list.name, node.prev, node.next, node.up, node.down))
        self.appendMessage("Find Node Completed in {} seconds".format((t2 - t1)))

    def DeleteFromFile(self):
        if not self.selected_list:
            self.appendMessage("You need to select a Skip List first")
            return
        filename = filedialog.askopenfilename(
            initialdir=".", title="Select File to read from")
        if not filename:
            self.appendMessage("No values read")
            return
        elif ".csv" not in filename:
            self.appendMessage("Only CSV files are allowed")
            return

        f = open(filename, "r")
        reader = csv.reader(f, delimiter=",")
        keys = []

        logger.info("Reading all integers from file {0}".format(filename))
        for key in reader:
            keys.append(key)

        if not keys or len(keys) <= 0:
            self.appendMessage("No Keys found in the file")
            return

        keys = keys[0]

        logger.info("Found {0} keys in file {1}".format(len(keys), filename))
        logger.debug("Keys: {}".format(keys))

        t1 = time.clock()
        for key in keys:
            try:
                key = int(key)
                deleted = self.selected_list.delete(int(key))
                if self.trace_mode:
                    if deleted:
                        self.appendMessage(
                            "Deleted Key {}, the list is now {}".format(key, self.selected_list))
                    else:
                        self.appendMessage("Key {} was not found in the list".format(key))
            except:
                logger.error(
                    "Found invalid key {} in file, skipping it".format(key))
        self.setLabels()
        t2 = time.clock()
        self.appendMessage(
            "Total time to delete {} keys: {} seconds".format(len(keys), (t2 - t1)))

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
