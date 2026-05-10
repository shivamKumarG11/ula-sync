import secrets

from app.extensions import db
from app.models import PackingItem, Trip
from app.models.enums import PackingCategoryEnum
from app.utils.errors import AppError

_DEFAULT_ITEMS = [
    ("Passport", PackingCategoryEnum.documents, True),
    ("Visa / travel permits", PackingCategoryEnum.documents, True),
    ("Travel insurance documents", PackingCategoryEnum.documents, True),
    ("Phone charger", PackingCategoryEnum.electronics, False),
    ("Power bank", PackingCategoryEnum.electronics, False),
    ("Toothbrush & toothpaste", PackingCategoryEnum.toiletries, False),
    ("Sunscreen", PackingCategoryEnum.toiletries, False),
    ("Basic medicines (paracetamol, antacid)", PackingCategoryEnum.medicine, False),
    ("Comfortable walking shoes", PackingCategoryEnum.clothing, False),
    ("Light jacket / layer", PackingCategoryEnum.clothing, False),
]


def get_packing_items(trip: Trip) -> dict:
    items = PackingItem.query.filter_by(trip_id=trip.id).order_by(
        PackingItem.category, PackingItem.is_compulsory.desc(), PackingItem.name
    ).all()
    grouped: dict[str, list] = {}
    for item in items:
        key = item.category.value if hasattr(item.category, "value") else item.category
        grouped.setdefault(key, []).append(item)
    return grouped


def add_item(trip: Trip, data: dict) -> PackingItem:
    item = PackingItem(
        trip_id=trip.id,
        name=data["name"],
        category=data["category"],
        is_compulsory=data.get("is_compulsory", False),
    )
    db.session.add(item)
    db.session.commit()
    return item


def add_items_batch(trip: Trip, items_data: list[dict]) -> list[PackingItem]:
    created = []
    for d in items_data:
        item = PackingItem(
            trip_id=trip.id,
            name=d["name"],
            category=d["category"],
            is_compulsory=d.get("is_compulsory", False),
        )
        db.session.add(item)
        created.append(item)
    db.session.commit()
    return created


def get_item(item_id: str, trip: Trip) -> PackingItem:
    item = PackingItem.query.filter_by(id=item_id, trip_id=trip.id).first()
    if not item:
        raise AppError("Packing item not found", 404)
    return item


def update_item(item: PackingItem, data: dict) -> PackingItem:
    for key in ("name", "category", "is_packed", "is_compulsory"):
        if key in data:
            setattr(item, key, data[key])
    db.session.commit()
    return item


def delete_item(item: PackingItem) -> None:
    db.session.delete(item)
    db.session.commit()


def seed_default_items(trip: Trip) -> int:
    existing_names = {
        i.name.lower()
        for i in PackingItem.query.filter_by(trip_id=trip.id).all()
    }
    added = 0
    for name, category, is_compulsory in _DEFAULT_ITEMS:
        if name.lower() not in existing_names:
            db.session.add(
                PackingItem(
                    trip_id=trip.id,
                    name=name,
                    category=category,
                    is_compulsory=is_compulsory,
                )
            )
            added += 1
    db.session.commit()
    return added


def reset_checklist(trip: Trip) -> None:
    PackingItem.query.filter_by(trip_id=trip.id).update({"is_packed": False})
    db.session.commit()


def generate_checklist_share_token(trip: Trip) -> str:
    if not trip.checklist_share_token:
        trip.checklist_share_token = secrets.token_urlsafe(32)
        db.session.commit()
    return trip.checklist_share_token
