from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response  # You can add `filter_salaries` if needed
from fastapi.responses import JSONResponse
from app.dependencies.permission import require
from app.utils import filter_employee_salaries

router = APIRouter(
    prefix="/employee-salaries",
    tags=["Employee Salaries"]
)

# ✅ GET ALL with pagination

@router.get("/", response_model=schemas.EmployeeSalaryListResponse)
def get_employee_salaries(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.EmployeeSalary)
        query = filter_employee_salaries(request.query_params, query)

        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.EmployeeSalaryOut.from_orm(s) for s in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeSalaryOut, dependencies=[require("create_employee_salary")])
def create_employee_salary(
    salary: schemas.EmployeeSalaryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        salary_data = salary.dict()
        salary_data["created_by_user_id"] = current_user.id

        # ✅ Calculate gross salary
        gross_salary = (
            salary_data["basic_salary"]
            + salary_data["bonus_amount"]
            + salary_data["housing_allowance"]
            + salary_data["transport_allowance"]
            + salary_data["medical_allowance"]
        )

        # ✅ Calculate total deductions
        total_deductions = (
            salary_data["tax_deduction"]
            + salary_data["insurance_deduction"]
            + salary_data["other_deductions"]
        )

        # ✅ Calculate net salary
        salary_data["net_salary"] = gross_salary - total_deductions

        # ✅ Save to DB
        new_salary = models.EmployeeSalary(**salary_data)
        db.add(new_salary)
        db.commit()
        db.refresh(new_salary)

        return new_salary

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ✅ GET BY ID
@router.get("/{id}", response_model=schemas.EmployeeSalaryOut, dependencies=[require("read_employee_salary")])
def get_employee_salary(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    salary = db.query(models.EmployeeSalary).filter(models.EmployeeSalary.id == id).first()
    if not salary:
        raise HTTPException(status_code=404, detail=f"EmployeeSalary with id {id} not found")
    return salary


# ✅ PATCH UPDATE

@router.patch("/{id}", response_model=schemas.EmployeeSalaryOut, dependencies=[require("update_employee_salary")])
def patch_update_employee_salary(
    id: int,
    updated_salary: schemas.EmployeeSalaryUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        salary_instance = db.query(models.EmployeeSalary).filter(models.EmployeeSalary.id == id).first()

        if not salary_instance:
            raise HTTPException(status_code=404, detail=f"EmployeeSalary with id {id} not found")

        update_data = updated_salary.dict(exclude_unset=True)

        # Apply incoming updates
        for key, value in update_data.items():
            # We skip "net_salary" from update (always override)
            if key != "net_salary":
                setattr(salary_instance, key, value)

        # ✅ Always recalculate net_salary from current values
        gross_salary = (
            salary_instance.basic_salary +
            salary_instance.bonus_amount +
            salary_instance.housing_allowance +
            salary_instance.transport_allowance +
            salary_instance.medical_allowance
        )
        total_deductions = (
            salary_instance.tax_deduction +
            salary_instance.insurance_deduction +
            salary_instance.other_deductions
        )
        salary_instance.net_salary = gross_salary - total_deductions

        db.commit()
        db.refresh(salary_instance)

        return salary_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while updating employee salary: {str(e)}"
        )


# ✅ DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK, dependencies=[require("delete_employee_salary")])
def delete_employee_salary(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    salary_query = db.query(models.EmployeeSalary).filter(models.EmployeeSalary.id == id)
    salary = salary_query.first()

    if not salary:
        raise HTTPException(status_code=404, detail=f"EmployeeSalary with id {id} not found")

    salary_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Employee salary deleted successfully"}
