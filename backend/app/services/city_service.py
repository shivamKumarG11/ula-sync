from app.extensions import db
from app.models import Activity, City, CityCostBreakdown
from app.utils.errors import AppError
from app.utils.helpers import paginate_query


def search_cities(
    q: str | None,
    country: str | None,
    country_code: str | None,
    region: str | None,
    sort: str,
    order: str,
    page: int,
    per_page: int,
):
    sort_col_map = {
        "name": City.name,
        "popularity_score": City.popularity_score,
        "cost_index_usd": City.cost_index_usd,
    }
    col = sort_col_map.get(sort, City.popularity_score)
    col = col.desc() if order == "desc" else col.asc()

    query = City.query
    if q:
        query = query.filter(
            db.or_(
                City.name.ilike(f"%{q}%"),
                City.country.ilike(f"%{q}%"),
            )
        )
    if country:
        query = query.filter(City.country.ilike(f"%{country}%"))
    if country_code:
        query = query.filter(City.country_code == country_code.upper())
    if region:
        query = query.filter(City.region.ilike(f"%{region}%"))

    query = query.order_by(col)
    return paginate_query(query, page, per_page, max_per_page=100)


def get_city_by_slug(slug: str) -> City:
    city = City.query.filter_by(slug=slug).first()
    if not city:
        raise AppError("City not found", 404)
    return city


def search_activities(
    city: City,
    q: str | None,
    category: str | None,
    min_cost: float | None,
    max_cost: float | None,
    max_duration: float | None,
    booking_required: bool | None,
    page: int,
    per_page: int,
):
    query = Activity.query.filter_by(city_id=city.id)
    if q:
        query = query.filter(
            db.or_(
                Activity.name.ilike(f"%{q}%"),
                Activity.description.ilike(f"%{q}%"),
            )
        )
    if category:
        query = query.filter(Activity.category == category)
    if min_cost is not None:
        query = query.filter(Activity.cost_usd >= min_cost)
    if max_cost is not None:
        query = query.filter(Activity.cost_usd <= max_cost)
    if max_duration is not None:
        query = query.filter(Activity.duration_hours <= max_duration)
    if booking_required is not None:
        query = query.filter(Activity.booking_required == booking_required)

    return paginate_query(query, page, per_page)


def get_activity_by_id(activity_id: str) -> Activity:
    activity = Activity.query.get(activity_id)
    if not activity:
        raise AppError("Activity not found", 404)
    return activity
