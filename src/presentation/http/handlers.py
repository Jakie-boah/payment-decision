from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.infrastructure.postgres.exceptions import PaymentNotFoundError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(PaymentNotFoundError)
    async def handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"msg": "Payment not found"},
        )
