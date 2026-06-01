from fastapi import FastAPI
import logging
from exceptions.handlers import register_exception_handlers
from middleware import configure_middleware

from employees.router import router as employee_router
from addresses.router import router as address_router
from departments.router import router as department_router
from emp_department.router import router as emp_dept_router

from auth.router import router as auth_router
from config import settings

# logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# @asynccontextmanager    #lifespan function to create the database tables when the application starts, using the create_tables function from the database module, and yield to allow the application to run until it is stopped
# async def lifespan(app: FastAPI): #generator function that will be used as the lifespan of the FastAPI application, it will create the database tables when the application starts and then yield to allow the application to run until it is stopped
#     await create_tables()
#     yield

app = FastAPI(
    title="Employee CRUD API",
    description="Simple employee app",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    # lifespan=lifespan
)


# app.add_middleware(RequestLoggingMiddleware)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],    # to allow different ports, like https or http will be allowed
#     allow_credentials=False, # to access cookies etc
#     allow_methods=["*"],  # * means all methods are allowed
#     allow_headers=["*"],
#     expose_headers=["X-Process-Time"],
# )

configure_middleware(app)

register_exception_handlers(app)

app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(address_router)
app.include_router(department_router)
app.include_router(emp_dept_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "env": settings.app_env, "debug": settings.debug}


# @app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
# async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     db_employee = Employee(name=name.strip(), email=email.strip())
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except sqlite3.IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()


# @app.get("/employee", tags=["Employees"])
# async def get_all_employees(db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     return [r.to_api_dict() for r in result.all()]

# @app.delete("/employee/{emp_id}", tags=["Delete Employees"])
# async def delete_employee(emp_id: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where( Employee.id == emp_id, Employee.deleted_at.is_(None))
#     result = await db.scalar(stmt)
#     if result is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Employee with id {emp_id} not found"
#         )
#     result.deleted_at = func.now()
#     try:
#         await db.commit()
#     except Exception:
#         await db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f"Error deleting employee with id {emp_id}"
#         )
#     return {
#         "message": "Employee deleted",
#         # "employee": result.to_api_dict()
#     }

# @app.patch("/employee/{emp_id}", tags=["Update Employees"])
# async def update_employee(emp_id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where( Employee.id == emp_id, Employee.deleted_at.is_(None))
#     result = await db.scalar(stmt)
#     if result is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Employee with id {emp_id} not found"
#         )
#     name = body.get("name")
#     email = body.get("email")
#     if name is not None:
#         if not isinstance(name, str) or not name.strip():
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#         result.name = name.strip()
#     if email is not None:
#         if not isinstance(email, str) or not email.strip():
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#         result.email = email.strip()
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(result)
#     return result.to_api_dict()


"""

_employees: dict[int, dict] = {}
_next_id: int = 1

@dataclass
class EmployeeCreate:
    name : str
    age : int
    email : str
    dept : str
    salary : float

class EmployeeModel(TypedDict):
    id : int
    name : str
    age : int
    email : str
    dept : str
    salary : float


@app.get("/",tags=["Hello"])
def welcome():
    return {"Welcome to employee app"}

@app.post("/", tags=["Create employees"],response_model=EmployeeModel)
async def create_employee(emp: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    global _employees
    global _next_id
    id = _next_id
    _employees[_next_id] = {
        "id" : id,
        "name" : emp.name,
        "age" : emp.age,
        "email" : emp.email,
        "dept" : emp.dept,
        "salary" : emp.salary
    }
    _next_id += 1
    return _employees[id]

@app.get("/employee",tags=["Get all employees"])
def employees():
    return list(_employees.values())

@app.get("/{emp_id}",tags=["Get employee with id"])
def get_employee(emp_id:int):
    if emp_id not in _employees:
        return "id not found"
    return _employees[emp_id]
    


@app.delete("/{emp_id}", tags=["Delete any employee"])
def delete_employees(emp_id:int):
    if emp_id not in _employees:
        return "id not found"
    deleted = _employees.pop(emp_id)
    return {
        "message": "Employee deleted",
        "employee": deleted
    } 

@app.patch("/{emp_id}", tags=["Update any employee"])
def update_employee(emp_id: int,emp: EmployeeCreate):
    if emp_id not in _employees:
        return "id not found"

    _employees[emp_id]["dept"] = emp.dept

    return _employees[emp_id]
    
"""
