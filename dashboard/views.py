# dashboard/views.py
from django.shortcuts import render, redirect
from .firebase_connector import get_latest_sensor_data
from .dsa_structures import (buffer_sensor_data, get_buffered_data, 
                            perform_action, undo_action, redo_action, 
                            BSTNode, insert_bst, inorder_traversal,
                            LinkedList, HashTable, Graph, Queue,bst_root, inorder_traversal)
from datetime import datetime
from .models import SensorReading

# Global variables for DSA concepts
#bst_root = None
# action_stack = []
queue = Queue()
linked_list = LinkedList()
hash_table = HashTable()
graph = Graph()

# Dashboard view to show sensor data, buffered data, and DSA operations
# Dashboard view to show sensor data, buffered data, and DSA operations
from django.shortcuts import render, redirect
from .firebase_connector import get_latest_sensor_data
from .dsa_structures import (
    buffer_sensor_data, get_buffered_data, 
    perform_action, undo_action, redo_action, 
    BSTNode, insert_bst, inorder_traversal,
    LinkedList, HashTable, Graph, Queue, Stack
)
from datetime import datetime

# Global variables for DSA concepts
#bst_root = None
queue = Queue()
linked_list = LinkedList()
hash_table = HashTable()
graph = Graph()

# Dashboard view to show sensor data, buffered data, and DSA operations
def dashboard_view(request):
    # Handle undo/redo actions
    action_result = handle_undo_redo_actions(request)

    # Fetch the latest sensor data
    sensor_data = fetch_sensor_data()

    # Fetch the buffered sensor data
    buffered_data = get_buffered_data()

    # ✅ Get BST schedule (sorted tasks)
    schedule = inorder_traversal(bst_root)

    # Clear the existing graph to avoid duplicate edges on page refresh
    #graph.graph = {}

    # graph.add_edge("Controller", "Zone A")  # example default
    # graph.add_edge("Zone A", "Zone B")
    # graph.add_edge("Zone A", "Zone C")
    # graph.add_edge("Zone B", "Zone D")


    # Render the dashboard page with all necessary data
    return render(request, 'dashboard/dashboard.html', {
        'sensor': sensor_data,
        'buffered_data': buffered_data,
        'action_result': action_result,
        'linked_list': linked_list.display(),
        'hash_table': hash_table.display(),
        'graph': graph.display(),
        'schedule': schedule,
    })


def handle_undo_redo_actions(request):
    if request.GET.get("undo"):
        return undo_action(graph)
    elif request.GET.get("redo"):
        return redo_action(graph)
    elif request.GET.get("action"):
        action = request.GET["action"]
        return perform_action(action, graph)
    return ""



# def fetch_sensor_data():
#     sensor_data = get_latest_sensor_data()

#     if not sensor_data or not isinstance(sensor_data, dict) or "sensor_id" not in sensor_data:
#         return generate_default_sensor_data()

#     # Ensure sensor ID is a timestamp
#     sensor_data['sensor_id'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
#     buffer_sensor_data(sensor_data)
#     linked_list.append(sensor_data)
#     hash_table.insert(sensor_data["sensor_id"], sensor_data)

#     return sensor_data


def fetch_sensor_data():
    sensor_data = get_latest_sensor_data()

    if not sensor_data or not isinstance(sensor_data, dict) or "sensor_id" not in sensor_data:
        return generate_default_sensor_data()

    # Generate timestamp ID for backend
    current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    sensor_data['sensor_id'] = current_time

    # Save in DSA structures
    buffer_sensor_data(sensor_data)
    linked_list.append(sensor_data)
    hash_table.insert(sensor_data["sensor_id"], sensor_data)

    # ✅ Save in backend (Django DB)
    SensorReading.objects.create(
        sensor_id=current_time,
        temperature=float(sensor_data["temperature"]),
        humidity=float(sensor_data["humidity"]),
        soil_moisture=float(sensor_data["soil_moisture"])
    )

    return sensor_data



def generate_default_sensor_data():
    return {
        'sensor_id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'temperature': 0,
        'humidity': 0,
        'soil_moisture': 0
    }

def scheduler_view(request):
    global bst_root

    # Handle form submission to add new schedule
    if request.method == "POST":
        time = request.POST["time"]
        task = request.POST["task"]

        # Create a new BST node for the task and insert it into the BST
        new_node = BSTNode(time, task)
        bst_root = insert_bst(bst_root, new_node)

    # Get the tasks in sorted order
    schedule = inorder_traversal(bst_root)

    return render(request, 'dashboard/scheduler.html', {'schedule': schedule})