from fastapi import APIRouter
from fastapi_pagination import Page

from app.serializers.events import Event
from app.serializers.bets import response_201, response_200
from app.views import event_view, bet_view

router = APIRouter(tags=["Bets"])

router.add_api_route(
    "/events",
    event_view.get,
    methods=["GET"],
    summary="Получить список событий, на которые можно совершить ставку",
    response_model=Page[Event],
)
router.add_api_route(
    "/bets",
    bet_view.get,
    methods=["GET"],
    summary="Получить историю всех сделанных ставок",
    responses=response_200,
)
router.add_api_route(
    "/bet",
    bet_view.post,
    methods=["POST"],
    status_code=201,
    summary="Сделать ставку на событие",
    responses=response_201,
)

__all__ = ["router"]
