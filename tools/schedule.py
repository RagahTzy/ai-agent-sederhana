import json

SCHEDULE_FILE = "data/schedule.json"

def load_schedule():
    try:
        with open(SCHEDULE_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_schedule(data):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def list_events():
    return load_schedule()

def add_event(name, datetime_str):
    schedule = load_schedule()
    schedule.append({"name": name, "datetime": datetime_str})
    save_schedule(schedule)
    return f"Event '{name}' at {datetime_str} has been added successfully."

def get_event_by_index(index):
    schedule = load_schedule()
    if 0 <= index < len(schedule):
        return schedule[index]
    return None

def delete_event_by_index(index):
    schedule = load_schedule()
    if 0 <= index < len(schedule):
        ev = schedule.pop(index)
        save_schedule(schedule)
        return f"Event '{ev['name']}' has been deleted successfully."
    return "Invalid event number."

def update_event_by_index(index, new_name=None, new_datetime=None):
    schedule = load_schedule()
    if 0 <= index < len(schedule):
        if new_name:
            schedule[index]['name'] = new_name
        if new_datetime:
            schedule[index]['datetime'] = new_datetime
        save_schedule(schedule)
        return f"Event has been updated to '{schedule[index]['name']} ({schedule[index]['datetime']})'."
    return "Invalid event number."