import json
import os
from datetime import datetime
import sys

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return[]
        

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        if filter_status and task['status'] != filter_status:
            continue
        print(f"[{task['id']}] {task['description']} - {task['status']}")

    
def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(task_id):
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully.")
            return
    print("Task ID not found.")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != int(task_id)]
    if len(new_tasks) == len(tasks):
        print("Task ID not found.")
    else:
        save_tasks(new_tasks)
        print("Task deleted successfully.")

def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(task_id):
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}.")
            return
    print("Task ID not found.")


# ---- MAIN CLI LOGIC ----

def main():
    if len(sys.argv) < 2:
        print("Usage: python task_cli.py [action] [arguments]")
        return
    
    action = sys.argv[1]

    if action == "add" and len(sys.argv) > 2:
        add_task(sys.argv[2])
    elif action == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    elif action == "update" and len(sys.argv) > 3:
        update_task(sys.argv[2], sys.argv[3])
    elif action == "delete" and len(sys.argv) > 2:
        delete_task(sys.argv[2], "in-progress")
    elif action == "mark-done" and len(sys.argv) > 2:
        mark_status(sys.argv[2], "done")
    else:
        print("Unknown command or missing arguments.")

if __name__ == "__main__":
    main()
