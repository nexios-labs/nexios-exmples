from nexios.routing import Router
from nexios.http import Request, Response
from nexios import get_application
from task_services import get_all_tasks, create_task, get_task, update_task, delete_task
from csv_helper import ensure_csv_exists
from models import Task
from pydantic import ValidationError

router = Router(prefix="/tasks")
app = get_application()

@app.on_startup
async def run_startup():
    print("App startup")
    await ensure_csv_exists()
# Get all tasks (with optional filters)
@router.get("/all")
async def get_tasks(req: Request, res: Response):
    filters = {}
    if "completed" in req.query_params:
        filters["completed"] = req.query_params["completed"]
    return res.json(await get_all_tasks(filters))


# Get a single task by ID
@router.get("/get/{task_id}")
async def get_task_by_id(req: Request, res: Response):
    task = await get_task(req.path_params["task_id"])
    if task:
        return res.json(task)
    return res.json({"error": "Task not found"}, status=404)


# Create a new task
@router.post("/new")
async def create_new_task(req: Request, res: Response):
    try:
        task_data = Task(**await req.json)
    except ValidationError as err:
        return res.json(err.errors(),status_code=422)
    task = await create_task(task_data)
    return res.json({"message": "Task created", "task": task})


# Update a task
@router.put("/update/{task_id}")
async def update_existing_task(req: Request, res: Response):
    task_id = req.path_params["task_id"]
    update_data = Task(**await req.json)
    task = await update_task(task_id, update_data)
    if task:
        return res.json({"message": "Task updated", "task": task})
    return res.json({"error": "Task not found"}, status=404)


# Delete a task
@router.delete("/delete/{task_id}")
async def delete_existing_task(req: Request, res: Response):
    task_id = req.path_params["task_id"]
    if await delete_task(task_id):
        return res.json({"message": "Task deleted"})
    return res.json({"error": "Task not found"}, status=404)


app.mount_router(router=router)