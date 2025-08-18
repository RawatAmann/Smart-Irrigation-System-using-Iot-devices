# dashboard/dsa_structures.py

from collections import deque

# ========== SENSOR DATA BUFFER ==========
sensor_data_buffer = deque()
action_stack = []  # Stack to store performed actions
redo_stack = []    # Stack to store undone actions

def buffer_sensor_data(data):
    if len(sensor_data_buffer) >= 10:
        sensor_data_buffer.popleft()
    sensor_data_buffer.append(data)
    action_stack.append(('buffer', data))

def get_buffered_data():
    return list(sensor_data_buffer)

# ========== UNDO & REDO FUNCTIONS ======== ==
def undo_action(graph=None):
    while action_stack:
        action, data = action_stack.pop()
        redo_stack.append((action, data))

        if action == 'action' and graph:
            words = data.lower().split()
            if len(words) >= 3 and words[1] == 'zone':
                zone = words[2].capitalize()

                if "Controller" in graph.graph and zone in graph.graph["Controller"]:
                    graph.graph["Controller"].remove(zone)

                if zone in graph.graph:
                    del graph.graph[zone]

                return f"Undo: removed zone '{zone}' from graph"

        elif action == 'buffer':
            if sensor_data_buffer:
                sensor_data_buffer.pop()
            # keep looping to find an 'action'

    return "Nothing to undo"


def redo_action(graph=None):
    if redo_stack:
        action, data = redo_stack.pop()
        action_stack.append((action, data))

        if action == 'buffer':
            # buffer_sensor_data already manages buffer size
            buffer_sensor_data(data)
            return "Redo: buffer"

        elif action == 'action' and graph:
            # Re-perform the graph update action
            return perform_action(data, graph)

        return f"Redo: {action}"
    return "Nothing to redo"




# ========== PERFORM ACTION ==========
from datetime import datetime

# Track BST root globally
bst_root = None

def perform_action(action, graph):
    global bst_root
    action_stack.append(('action', action))

    action = action.lower()
    words = action.split()

    # ✅ Handle "water zone A at 18:00" format → insert into BST
    if "at" in words and len(words) >= 5:
        try:
            zone = words[2].capitalize()
            time_index = words.index("at") + 1
            schedule_time = words[time_index]
            datetime.strptime(schedule_time, "%H:%M")  # validate format

            task_text = f"{words[0].capitalize()} {zone}"
            new_node = BSTNode(schedule_time, task_text)
            bst_root = insert_bst(bst_root, new_node)
            print(f"[BST] Inserted: {task_text} at {schedule_time}")


            return f"Scheduled '{task_text}' at {schedule_time} in BST"
        except Exception as e:
            return f"Error scheduling task: {e}"

    # ✅ Otherwise treat it as graph operation
    if len(words) >= 3 and words[1] == 'zone':
        zone_name = words[2].capitalize()
        if zone_name not in graph.graph:
            graph.graph[zone_name] = []
        graph.add_edge("Controller", zone_name)
        return f"Action performed and graph updated: {action}"

    return f"Action performed: {action}"




# ========== BINARY SEARCH TREE ==========
from datetime import datetime

# ========== BINARY SEARCH TREE ==========
class BSTNode:
    def __init__(self, time, task):
        self.time = time
        self.task = task
        self.left = None
        self.right = None

def insert_bst(root, node):
    if root is None:
        return node
    if node.time < root.time:
        root.left = insert_bst(root.left, node)
    else:
        root.right = insert_bst(root.right, node)
    return root

def inorder_traversal(root):
    result = []
    if root:
        result.extend(inorder_traversal(root.left))
        result.append((root.time, root.task))
        result.extend(inorder_traversal(root.right))
    return result




# ========== QUEUE ==========
class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        return None

    def is_empty(self):
        return len(self.items) == 0

# ========== STACK ==========
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

# ========== LINKED LIST ==========
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def display(self):  # Added display method
        return self.to_list()

# ========== HASH TABLE ==========
class HashTable:
    def __init__(self, max_size=10):
        self.table = {}
        self.max_size = max_size

    def insert(self, key, value):
        # If size exceeds max_size, remove the oldest inserted key
        if len(self.table) >= self.max_size:
            # Use FIFO order: get the first inserted key
            oldest_key = next(iter(self.table))
            del self.table[oldest_key]
        self.table[key] = value
    
    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def get(self, key):
        return self.table.get(key, None)

    def display(self):
        return self.table


# ========== GRAPH ==========
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph[u]:  # prevent duplicates
            self.graph[u].append(v)

    def get_neighbors(self, u):
        return self.graph.get(u, [])

    def display(self):  # Added display method
        return self.graph