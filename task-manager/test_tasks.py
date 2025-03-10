import pytest
from task_services import create_task, get_all_tasks, update_task, delete_task
from models import Task

@pytest.mark.asyncio
async def test_create_task():
    task_data = Task(title="Test Task", description="Testing", completed=False)
    task = await create_task(task_data)
    assert task["title"] == "Test Task"
    assert task["completed"] == "false"

@pytest.mark.asyncio
async def test_get_all_tasks():
    tasks = await get_all_tasks()
    assert isinstance(tasks, list)

@pytest.mark.asyncio
async def test_update_task():
    task_data = Task(title="New Task", description="Testing", completed=False)
    task = await create_task(task_data)
    updated = await update_task(task["id"], Task(title="Updated Task", completed=True))
    assert updated["title"] == "Updated Task"
    assert updated["completed"] == "true"

@pytest.mark.asyncio
async def test_delete_task():
    task_data = Task(title="To be deleted", description="Testing", completed=False)
    task = await create_task(task_data)
    assert await delete_task(task["id"]) == True
