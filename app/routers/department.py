# from fastapi import APIRouter, Depends, status, Request, HTTPException
# from sqlalchemy.orm import Session
# from typing import List, Optional, Any

# from app.dependencies.permission import permission_required, require
# from .. import database, schemas, models, oauth2
# from app.utils import paginate_data, create_response, filter_departments
# from fastapi.responses import JSONResponse
# # from app.schemas import DepartmentListResponse
# from fastapi import APIRouter, Depends, HTTPException, Query
# from fastapi.responses import StreamingResponse
# from sqlalchemy.orm import Session
# from io import StringIO, BytesIO
# import pandas as pd

# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
# from sqlalchemy.orm import Session
# import pandas as pd
# from app import database, models
# import re


from fastapi import APIRouter, Depends, status, Request, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from io import StringIO, BytesIO
import pandas as pd
import re

from app import database, models
from .. import schemas, oauth2
from app.dependencies.permission import permission_required, require
from app.utils import paginate_data, create_response, filter_departments



router = APIRouter(
    prefix="/departments",
    tags=['Departments']
)

# @router.get("/", response_model=List[schemas.Department])

# @router.get("/", response_model=Any)
@router.get("/", response_model=schemas.DepartmentListResponse, dependencies=[require("read_department")])
def get_departments(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Department)
        query = filter_departments(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        # ✅ Convert ORM to Pydantic
        serialized_data = [schemas.Department.from_orm(dept) for dept in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {
            "status": "SUCCESSFUL",
            "result": response_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Department, dependencies=[require("create_department")])
# @router.post("/", status_code=status.HTTP_201_CREATED)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        
        department_data = department.dict()
        department_data["created_by_user_id"] = current_user.id  # ✅ Correct field name

        new_department = models.Department(**department_data)
        db.add(new_department)
        db.commit()
        db.refresh(new_department)

        
        return new_department

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# router = APIRouter(prefix="/departments",
#     tags=['Departments'])
# Url is ,   http://127.0.0.1:8000/departments/download-departments?format=csv
@router.get("/download-departments", dependencies=[require("read_department")])
def download_departments(
    format: str = Query("csv", description="File format (csv or xlsx)"),
    download: bool = Query(False, description="Force file download"),
    db: Session = Depends(database.get_db)
):
    departments = db.query(models.Department).all()
    data = [{"id": d.id, "name": d.name, "location": d.location} for d in departments]
    df = pd.DataFrame(data)

    # CSV Format
    if format == "csv":
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        headers = {}
        if download:
            headers = {
                "Content-Disposition": "attachment; filename=departments.csv",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers=headers
        )

    # Excel (XLSX) Format
    elif format == "xlsx":
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Departments")
        output.seek(0)
        
        headers = {}
        if download:
            headers = {
                "Content-Disposition": "attachment; filename=departments.xlsx",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )

    # Invalid format
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'csv' or 'xlsx'.")



@router.get("/{id}", response_model=schemas.Department, dependencies=[require("read_department")])
def get_department(id: int, db: Session = Depends(database.get_db), 
                  current_user: models.User = Depends(oauth2.get_current_user)):
    department = db.query(models.Department).filter(models.Department.id == id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Department with id {id} not found")
    return department

@router.patch("/{id}", response_model=schemas.Department, dependencies=[require("update_department")])
def patch_update_department(
    id: int,
    updated_department: schemas.DepartmentUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:

        department_instance = db.query(models.Department).filter(models.Department.id == id).first()

        if not department_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with id {id} not found"
            )

        update_data = updated_department.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(department_instance, key, value)

        db.commit()
        db.refresh(department_instance)

        return department_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while patching the department: {str(e)}"
        )


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_department(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    _: None = Depends(permission_required(["delete_department"]))
):
    department_query = db.query(models.Department).filter(models.Department.id == id)
    department = department_query.first()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {id} not found"
        )

    department_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Department deleted successfully"}




# Url is http://127.0.0.1:8000/departments/upload-departments
# ✅ Helper validation functions
def is_valid_name(value):
    return (
        isinstance(value, str) and
        value.strip() and
        re.match(r'^[a-zA-Z\s]+$', value.strip())  # only letters and spaces
    )

def is_valid_location(value):
    return (
        isinstance(value, str) and
        value.strip() and
        not value.strip().isdigit()  # reject if only digits
    )

@router.post("/upload-departments", dependencies=[require("create_department")])
async def upload_departments(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    try:
        filename = file.filename or ""
        if filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        elif filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            raise HTTPException(status_code=400, detail="Only .xlsx and .csv files are supported.")

        added_count = 0
        skipped_rows = []

        for i in range(len(df)):
            try:
                row = df.iloc[i]
                name = row.get("name")
                location = row.get("location")

                # ✅ Apply full validation
                if not is_valid_name(name) or not is_valid_location(location):
                    skipped_rows.append(i + 2)  # +2: zero-based + header
                    continue

                department = models.Department(
                    name=name.strip(),
                    location=location.strip()
                )
                db.add(department)
                added_count += 1

            except Exception:
                skipped_rows.append(i + 2)
                continue

        db.commit()

        return {
                "status": "PARTIAL_SUCCESS" if skipped_rows else "SUCCESS",
                "message": f"{added_count} departments added.",
                "Total skipped Rows": len(skipped_rows) if skipped_rows else 0,
                "skipped_rows": skipped_rows or None
}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/test")
def test_route():
    return {"message": "Employee router is working"}