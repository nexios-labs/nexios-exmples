import uuid
from csv_helper import read_tasks, write_tasks

async def get_all_tasks(filters=None):
    tasks = await read_tasks()
    
    # Filter by completion status
    if filters and "completed" in filters:
        tasks = [t for t in tasks if t["completed"] == str(filters["completed"]).lower()]
    
    # Filter by date range (assuming task has "created_at")
    if filters and "date_range" in filters:
        start, end = filters["date_range"]
        tasks = [t for t in tasks if start <= t["created_at"] <= end]

    return tasks


async def create_task(task_data):
    task = {
        "id": str(uuid.uuid4()),
        "title": task_data.title,
        "description": task_data.description or "",
        "completed": str(task_data.completed).lower()
    }
    tasks = await read_tasks()
    tasks.append(task)
    await write_tasks(tasks)
    return task


async def get_task(task_id):
    tasks = await read_tasks()
    return next((t for t in tasks if t["id"] == task_id), None)


async def update_task(task_id, update_data):
    tasks = await read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = update_data.title or task["title"]
            task["description"] = update_data.description or task["description"]
            task["completed"] = str(update_data.completed).lower()
            await write_tasks(tasks)
            return task
    return None


async def delete_task(task_id):
    tasks = await read_tasks()
    filtered_tasks = [t for t in tasks if t["id"] != task_id]
    if len(filtered_tasks) == len(tasks):
        return False
    await write_tasks(filtered_tasks)
    return True
