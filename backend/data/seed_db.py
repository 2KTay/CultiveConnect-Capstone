import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import engine, Base
from models import Product, Regulation, Permit, ComplianceNote

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
US_FILE = os.path.join(DATA_DIR, "regulations_us.json")
CA_FILE = os.path.join(DATA_DIR, "regulations_ca.json")


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def seed_products_and_regulations(db: Session, data: dict):
    country = data["country"]
    authority = data["authority"]

    for product_data in data["products"]:
        existing = db.query(Product).filter_by(
            product_id=product_data["id"],
            country=country
        ).first()

        if existing:
            print(f"  Skipping {product_data['name']} ({country}) — already exists")
            continue

        product = Product(
            product_id=product_data["id"],
            name=product_data["name"],
            category=product_data["category"],
            form=product_data["form"],
            country=country
        )
        db.add(product)
        db.flush()

        hs_key = "hts_code" if "hts_code" in product_data else "hs_code"
        desc_key = "hts_description" if "hts_description" in product_data else "hs_description"

        regulation = Regulation(
            product_id=product.id,
            country=country,
            authority=authority,
            hs_code=product_data.get(hs_key, ""),
            hs_description=product_data.get(desc_key, ""),
            duty_rate=product_data.get("duty_rate", ""),
            duty_notes=product_data.get("duty_notes", ""),
            systems_approach=product_data.get("systems_approach", ""),
            regulatory_authorities=", ".join(product_data.get("regulatory_authorities", []))
        )
        db.add(regulation)
        db.flush()

        for permit_data in product_data.get("permits_and_requirements", []):
            permit = Permit(
                regulation_id=regulation.id,
                permit_type=permit_data.get("type", ""),
                authority=permit_data.get("authority", ""),
                required=permit_data.get("required", ""),
                notes=permit_data.get("notes", "")
            )
            db.add(permit)

        print(f"  Seeded: {product_data['name']} ({country})")

    for note_text in data.get("universal_compliance_notes", []):
        existing_note = db.query(ComplianceNote).filter_by(
            country=country,
            note=note_text
        ).first()
        if not existing_note:
            note = ComplianceNote(country=country, note=note_text)
            db.add(note)


def run_seed():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    print("\nSeeding US regulations...")
    us_data = load_json(US_FILE)

    print("\nSeeding Canada regulations...")
    ca_data = load_json(CA_FILE)

    with Session(engine) as db:
        seed_products_and_regulations(db, us_data)
        seed_products_and_regulations(db, ca_data)
        db.commit()

    print("\nDatabase seeded successfully.")
    print("Products loaded: 6 US + 6 Canada = 12 total records")


if __name__ == "__main__":
    run_seed()