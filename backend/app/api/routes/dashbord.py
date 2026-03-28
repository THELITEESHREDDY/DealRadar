from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, func
from urllib.parse import urlparse

from app.database.models import user_db, sites_db, orders_db
from app.database.sessions import get_session
from app.api.deps import get_current_user
from app.schemas.site import SiteResponse
from app.schemas.order import OrderResponse
from app.schemas.user import profile
from app.schemas.site import dashbord_model, url_model

router = APIRouter(prefix="/dashbord")


@router.get("/profile",response_model=profile)
async def profile(current_user: user_db = Depends(get_current_user),):

    return {
    "name": current_user.name,
    "age": current_user.age,
    "email": current_user.email,
    "phone": current_user.phone
}

@router.get("/", response_model=dashbord_model)
async def dashboard(
    current_user: user_db = Depends(get_current_user),
    session=Depends(get_session),
    page: int = 1,
    limit: int = 10
):
    curr_user_id = current_user.id
    offset = (page - 1) * limit

    orders_count = session.exec(
        select(func.count()).where(orders_db.userid == curr_user_id)
    ).one()

    sites = session.exec(
        select(sites_db.name)
        .where(sites_db.userid == curr_user_id)
        .offset(offset)
        .limit(limit)
    ).all()

    return {
        "site_count": len(sites),
        "sites": sites,
        "orders_count": orders_count
    }


@router.get("/myorders",response_model=list[OrderResponse])
async def my_orders(
    current_user: user_db = Depends(get_current_user),session=Depends(get_session)    
):
    
    return session.exec(
        select(orders_db).where(orders_db.userid == current_user.id)
    ).all()



@router.get("/viewsites",response_model=list[SiteResponse])
async def view_sites(
    current_user: user_db = Depends(get_current_user),
    session=Depends(get_session)
):

    sites = session.exec(
        select(sites_db).where(sites_db.userid == current_user.id)
    ).all()

    return sites


@router.post("/addsites")
async def add_sites_to_DB(
    url: url_model,
    current_user: user_db = Depends(get_current_user),
    session=Depends(get_session)
):
    parsed = urlparse(str(url.url))
    name = parsed.hostname or "unknown"

    site = sites_db(
        name=name,
        url=str(url.url),
        userid=current_user.id
    )

    session.add(site)
    session.commit()
    session.refresh(site)

    return site


@router.delete("/sites")
async def delete_site(
    id: int,
    current_user: user_db = Depends(get_current_user),
    session=Depends(get_session)
):
    site = session.exec(
        select(sites_db).where(
            sites_db.id == id,
            sites_db.userid == current_user.id
        )
    ).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    session.delete(site)
    session.commit()

    return {"ok": True}