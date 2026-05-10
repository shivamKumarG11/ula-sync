from app.extensions import db
from app.models import City, SavedCity, User
from app.utils.errors import AppError


def get_saved_cities(user: User) -> list:
    return (
        db.session.query(SavedCity, City)
        .join(City, SavedCity.city_id == City.id)
        .filter(SavedCity.user_id == user.id)
        .order_by(SavedCity.saved_at.desc())
        .all()
    )


def save_city(user: User, city_id: str) -> None:
    city = City.query.get(city_id)
    if not city:
        raise AppError("City not found", 404)

    if SavedCity.query.filter_by(user_id=user.id, city_id=city.id).first():
        raise AppError("City already saved", 409)

    db.session.add(SavedCity(user_id=user.id, city_id=city.id))
    db.session.commit()


def unsave_city(user: User, city_id: str) -> None:
    sc = SavedCity.query.filter_by(user_id=user.id, city_id=city_id).first()
    if not sc:
        raise AppError("Saved city not found", 404)
    db.session.delete(sc)
    db.session.commit()
