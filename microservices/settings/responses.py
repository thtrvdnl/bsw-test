descriptions = {
    200: "Успешный запрос.",
    201: "Успешное создание ресурса.",
}


def generate_response_200(model: object):
    return _generate_response(status=200, model=model)


def generate_response_201(model: object):
    return _generate_response(status=201, model=model)


def _generate_response(status: int, model: object):
    return {status: {"model": model, "description": descriptions[status]}}


__all__ = [
    "generate_response_200",
    "generate_response_201",
]
