from app.schemas.activity_schema import (
    ActivityOutputSchema,
    StopActivityInputSchema,
    StopActivityOutputSchema,
    StopActivityUpdateSchema,
)
from app.schemas.ai_schema import (
    ChatInputSchema,
    GenerateItineraryInputSchema,
    PackingAdviceInputSchema,
    RecommendTransportInputSchema,
    ReviewTripInputSchema,
    SuggestActivitiesInputSchema,
)
from app.schemas.city_schema import CityListOutputSchema, CityOutputSchema
from app.schemas.community_schema import (
    CommentInputSchema,
    CommentOutputSchema,
    CommunityPostInputSchema,
    CommunityPostOutputSchema,
    CommunityPostUpdateSchema,
)
from app.schemas.invoice_schema import (
    InvoiceCreateSchema,
    InvoiceItemInputSchema,
    InvoiceItemOutputSchema,
    InvoiceItemUpdateSchema,
    InvoiceOutputSchema,
    InvoiceUpdateSchema,
)
from app.schemas.note_schema import NoteInputSchema, NoteOutputSchema, NoteUpdateSchema
from app.schemas.packing_schema import (
    PackingBatchInputSchema,
    PackingItemInputSchema,
    PackingItemOutputSchema,
    PackingItemUpdateSchema,
)
from app.schemas.stop_schema import (
    ReorderStopsSchema,
    StopInputSchema,
    StopOutputSchema,
    StopUpdateSchema,
)
from app.schemas.trip_schema import (
    TripInputSchema,
    TripListOutputSchema,
    TripOutputSchema,
    TripUpdateSchema,
)
from app.schemas.user_schema import (
    LoginInputSchema,
    RegisterInputSchema,
    UpdateProfileInputSchema,
    UserOutputSchema,
)
