from app.serializers import SuccessResponse
from app.views import event_view
from fastapi import APIRouter

from microservices.settings import generate_response_200, generate_response_201

response_200 = generate_response_200(model=SuccessResponse)
response_201 = generate_response_201(model=SuccessResponse)

router = APIRouter(prefix="/event", tags=["Events"])

router.add_api_route(
    "",
    event_view.post,
    methods=["POST"],
    status_code=201,
    summary="Создать событие",
    responses=response_201,
)
router.add_api_route(
    "/{id}",
    event_view.patch,
    methods=["PATCH"],
    summary="Частично обновить одно событие по uuid",
    responses=response_200,
)

__all__ = ["router"]
