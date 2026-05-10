import math
from typing import Any

from flask import jsonify
from flask_sqlalchemy.pagination import Pagination


def make_response_envelope(data: Any, message: str | None = None, status_code: int = 200):
    body: dict = {"data": data}
    if message:
        body["message"] = message
    return jsonify(body), status_code


def paginate_response(pagination: Pagination, schema):
    return jsonify(
        {
            "data": schema.dump(pagination.items),
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }
    )


def paginate_query(query, page: int, per_page: int, max_per_page: int = 100):
    per_page = min(per_page, max_per_page)
    return query.paginate(page=page, per_page=per_page, error_out=False)
