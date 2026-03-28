from fastapi import APIRouter, BackgroundTasks
from app.service.scrapping_service import scrape_all_sites

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/")
async def search_product(product_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_all_sites, product_name)

    return {
        "message": f"Searching for '{product_name}' across all registered sites."
    }