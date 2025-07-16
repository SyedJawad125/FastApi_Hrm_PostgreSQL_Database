from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, get_object_or_404
from fastapi import Body

router = APIRouter(
    prefix="/payslips",
    tags=["Payslips"]
)

# ✅ GET ALL
@router.get("/", response_model=schemas.PayslipListResponse)
def get_payslips(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.Payslip)
        query = filter_payslips(request.query_params, query)

        data = query.all()
        paginated_data, count = paginate_data(data, request)
        serialized_data = [schemas.PayslipOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {"count": count, "data": serialized_data}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PayslipOut)
def create_payslip(
    payslip: schemas.PayslipCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = payslip.dict()
        data["created_by_user_id"] = current_user.id

        new_payslip = models.Payslip(**data)
        db.add(new_payslip)
        db.commit()
        db.refresh(new_payslip)

        return new_payslip
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET BY ID
@router.get("/{id}", response_model=schemas.PayslipOut)
def get_payslip(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    payslip = get_object_or_404(db.query(models.Payslip), id, "Payslip")
    return payslip


# ✅ PATCH UPDATE
@router.patch("/{id}", response_model=schemas.PayslipOut)
def update_payslip(
    id: int,
    payslip_data: schemas.PayslipUpdate = Body(...),  # ✅ fixed
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        payslip = db.query(models.Payslip).filter(models.Payslip.id == id).first()
        if not payslip:
            raise HTTPException(status_code=404, detail=f"Payslip with id {id} not found")

        update_data = payslip_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(payslip, key, value)

        db.commit()
        db.refresh(payslip)

        return payslip
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


# ✅ DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_payslip(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    payslip = get_object_or_404(db.query(models.Payslip), id, "Payslip")

    db.delete(payslip)
    db.commit()

    return {"message": "Payslip deleted successfully"}





