from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any

from app.dependencies.permission import permission_required, require
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response, filter_ranks
from fastapi.responses import JSONResponse



router = APIRouter(
    prefix="/ranks",
    tags=['Ranks']
)


@router.get("/", response_model=schemas.RankListResponse, dependencies=[require("read_rank")])
def get_ranks(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Rank)
        query = filter_ranks(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        # ✅ Convert ORM to Pydantic
        serialized_data = [schemas.Rank.from_orm(rnk) for rnk in paginated_data]

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




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Rank, dependencies=[require("create_rank")])
def create_rank(
    rank: schemas.RankCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        
        rank_data = rank.dict()
        rank_data["created_by_user_id"] = current_user.id  # ✅ Correct field name

        new_rank = models.Rank(**rank_data)
        db.add(new_rank)
        db.commit()
        db.refresh(new_rank)

        
        return new_rank

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{id}", response_model=schemas.Rank, dependencies=[require("read_rank")])
def get_rank(id: int, db: Session = Depends(database.get_db), 
                  current_user: models.User = Depends(oauth2.get_current_user)):
    rank = db.query(models.Rank).filter(models.Rank.id == id).first()
    if not rank:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Rank with id {id} not found")
    return rank

@router.patch("/{id}", response_model=schemas.Rank, dependencies=[require("update_rank")])
def patch_update_rank(
    id: int,
    updated_rank: schemas.RankUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        
        rank_instance = db.query(models.Rank).filter(models.Rank.id == id).first()

        if not rank_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rank with id {id} not found"
            )

        update_data = updated_rank.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(rank_instance, key, value)

        db.commit()
        db.refresh(rank_instance)

        return rank_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while patching the rank: {str(e)}"
        )



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_rank(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    _: None = Depends(permission_required(["delete_rank"]))
):
    rank_query = db.query(models.Rank).filter(models.Rank.id == id)
    rank = rank_query.first()

    if not rank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rank with id {id} not found"
        )

    rank_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Rank deleted successfully"}




# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from app.database import get_db
# from app.models.rank import Rank
# from app.schemas.rank import RankCreate, RankUpdate, Rank as RankSchema
# from app.dependencies.get_current_user import get_current_user
# from app.models.user import User

# router = APIRouter(
#     prefix="/ranks",
#     tags=["ranks"]
# )

# @router.post("/", response_model=RankSchema)
# def create_rank(
#     rank: RankCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     db_rank = Rank(
#         **rank.model_dump(),
#         created_by_user_id=current_user.id
#     )
#     db.add(db_rank)
#     db.commit()
#     db.refresh(db_rank)
#     return db_rank

# @router.get("/", response_model=List[RankSchema])
# def get_ranks(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     ranks = db.query(Rank).offset(skip).limit(limit).all()
#     return ranks

# @router.get("/{rank_id}", response_model=RankSchema)
# def get_rank(
#     rank_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     rank = db.query(Rank).filter(Rank.id == rank_id).first()
#     if rank is None:
#         raise HTTPException(status_code=404, detail="Rank not found")
#     return rank

# @router.put("/{rank_id}", response_model=RankSchema)
# def update_rank(
#     rank_id: int,
#     rank_update: RankUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     db_rank = db.query(Rank).filter(Rank.id == rank_id).first()
#     if db_rank is None:
#         raise HTTPException(status_code=404, detail="Rank not found")
    
#     for key, value in rank_update.model_dump(exclude_unset=True).items():
#         setattr(db_rank, key, value)
    
#     db.commit()
#     db.refresh(db_rank)
#     return db_rank

# @router.delete("/{rank_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_rank(
#     rank_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     db_rank = db.query(Rank).filter(Rank.id == rank_id).first()
#     if db_rank is None:
#         raise HTTPException(status_code=404, detail="Rank not found")
    
#     db.delete(db_rank)
#     db.commit()
#     return None 