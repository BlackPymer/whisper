import uvicorn

from .api import app
from .config import settings


def run_server() -> None:
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=False,
        access_log=True,
    )


if __name__ == "__main__":
    run_server()
