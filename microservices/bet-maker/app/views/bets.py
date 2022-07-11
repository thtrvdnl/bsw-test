from app.serializers.bets import BetCreate, SuccessResponse, Data, Bet
from app.services import create_bet, get_bets


class BetView:
    @staticmethod
    async def get() -> SuccessResponse:
        resources = await get_bets()
        data = [
            Data(id=resource["uuid"], attributes=Bet(**resource))
            for resource in resources
        ]
        return SuccessResponse(data=data)

    @staticmethod
    async def post(bet: BetCreate) -> SuccessResponse:
        resource = await create_bet(bet)
        data = Data(id=resource["uuid"], attributes=Bet(**resource))
        return SuccessResponse(data=data)


bet_view = BetView

__all__ = ["bet_view"]
