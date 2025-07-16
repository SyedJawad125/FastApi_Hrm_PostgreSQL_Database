from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import paginate_data

router = APIRouter(
    prefix="/salary-structures",
    tags=["Salary Structures"]
)


# ✅ GET ALL with pagination
@router.get("/", response_model=schemas.SalaryStructureListResponse)
def get_salary_structures(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.SalaryStructure)
        query = filter_salary_structures(request.query_params, query)

        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.SalaryStructureOut.from_orm(s) for s in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {"status": "SUCCESSFUL", "result": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SalaryStructureOut)
def create_salary_structure(
    structure: schemas.SalaryStructureCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = structure.dict()
        data["created_by_user_id"] = current_user.id

        new_structure = models.SalaryStructure(**data)
        db.add(new_structure)
        db.commit()
        db.refresh(new_structure)

        return new_structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET BY ID
@router.get("/{id}", response_model=schemas.SalaryStructureOut)
def get_salary_structure(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    structure = db.query(models.SalaryStructure).filter(models.SalaryStructure.id == id).first()
    if not structure:
        raise HTTPException(status_code=404, detail=f"SalaryStructure with id {id} not found")
    return structure


# ✅ PATCH UPDATE
@router.patch("/{id}", response_model=schemas.SalaryStructureOut)
def update_salary_structure(
    id: int,
    updated_structure: schemas.SalaryStructureUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        structure = db.query(models.SalaryStructure).filter(models.SalaryStructure.id == id).first()

        if not structure:
            raise HTTPException(status_code=404, detail=f"SalaryStructure with id {id} not found")

        update_data = updated_structure.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(structure, key, value)

        db.commit()
        db.refresh(structure)

        return structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


# ✅ DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_salary_structure(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    structure_query = db.query(models.SalaryStructure).filter(models.SalaryStructure.id == id)
    structure = structure_query.first()

    if not structure:
        raise HTTPException(status_code=404, detail=f"SalaryStructure with id {id} not found")

    structure_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Salary structure deleted successfully"}
