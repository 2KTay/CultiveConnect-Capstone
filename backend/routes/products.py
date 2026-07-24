"""GET /products — list the product+country entries available in the regulations data."""

from fastapi import APIRouter

from services.embeddings import load_regulations

router = APIRouter()


@router.get("/products")
def list_products():
    regulations = load_regulations()
    items = []
    for country, products in regulations.items():
        if country == "metadata" or not isinstance(products, dict):
            continue
        for product, data in products.items():
            if not isinstance(data, dict):
                continue
            items.append(
                {
                    "country": country,
                    "product": product,
                    "hts_code": data.get("hts_code") or data.get("hs_code"),
                    "base_duty": data.get("base_duty"),
                    "required_docs": data.get("required_docs", []),
                }
            )
    return {"count": len(items), "products": items}
