import enum


class ActivityCategoryEnum(str, enum.Enum):
    sightseeing = "sightseeing"
    food = "food"
    adventure = "adventure"
    shopping = "shopping"
    wellness = "wellness"
    cultural = "cultural"
    other = "other"


class PackingCategoryEnum(str, enum.Enum):
    clothing = "clothing"
    documents = "documents"
    electronics = "electronics"
    toiletries = "toiletries"
    medicine = "medicine"
    other = "other"


class ExpenseTypeEnum(str, enum.Enum):
    travel = "travel"
    stay = "stay"
    food = "food"
    activities = "activities"
    local_transport = "local_transport"


class InvoiceStatusEnum(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    paid = "paid"


class InvoiceCategoryEnum(str, enum.Enum):
    hotel = "hotel"
    travel = "travel"
    food = "food"
    activities = "activities"
    other = "other"


class TravelStyleEnum(str, enum.Enum):
    budget_explorer = "budget_explorer"
    comfort_seeker = "comfort_seeker"
    premium_traveller = "premium_traveller"
    backpacker = "backpacker"
