import anyio
import csv
import io
from typing import List, Dict

TASKS_FILE = "tasks.csv"

async def ensure_csv_exists():
    """Ensure that the tasks CSV file exists with headers."""
    path = anyio.Path(TASKS_FILE)
    if not await path.exists():
        async with await anyio.open_file(TASKS_FILE, "w", newline="") as file:
            await file.write("id,title,description,completed\n")  # Write headers


async def read_tasks() -> List[Dict]:
    """Read tasks from CSV file asynchronously."""
    path = anyio.Path(TASKS_FILE)
    if not await path.exists():
        return []

    async with await anyio.open_file(TASKS_FILE, "r") as file:
        content = await file.read()

    lines = content.splitlines()
    if len(lines) < 2:  # No tasks (only header or empty file)
        return []

    reader = csv.DictReader(lines)
    return list(reader)


async def write_tasks(tasks: List[Dict]):
    """Write tasks to CSV file asynchronously using csv.DictWriter."""
    buffer = io.StringIO()  # ✅ Fix: Use an in-memory file-like object
    writer = csv.DictWriter(buffer, fieldnames=["id", "title", "description", "completed"])
    writer.writeheader()
    writer.writerows(tasks)

    async with await anyio.open_file(TASKS_FILE, "w", newline="") as file:
        await file.write(buffer.getvalue())  # ✅ Write the buffered CSV content to the file


# ✅ Ensure CSV file exists at startup

