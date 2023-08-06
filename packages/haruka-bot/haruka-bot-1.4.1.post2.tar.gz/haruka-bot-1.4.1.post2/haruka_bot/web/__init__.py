# TODO 检测 driver 必须是 FastAPI
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from nonebot import get_driver
from nonebot.drivers import ReverseDriver

from .api import router

driver = get_driver()

assert isinstance(driver, ReverseDriver) and isinstance(driver.server_app, FastAPI)

app = FastAPI()
app.include_router(router, prefix="/api")
app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent / "build", html=True),
    name="frontend",
)

driver.server_app.mount("/haruka", app)
