import asyncio
import time
from asyncio import AbstractEventLoop, Future
from threading import Thread
from typing import Callable

from hypercorn.asyncio import serve
from hypercorn.config import Config
from fastapi import FastAPI


app = FastAPI()


@app.route("/ping", methods=["GET"])
async def ping():
    return "pong"


config = Config()
config.bind = ["localhost:8080"]


def run_server(
    loop: AbstractEventLoop,
    shutdown_trigger_future: Future,
):
    async def _serve_until_finished():
        await serve(
            app,
            config,
            shutdown_trigger=lambda: shutdown_trigger_future,
        )

    task = loop.create_task(_serve_until_finished())
    loop.run_until_complete(task)


def main() -> Callable[[], None]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    shutdown_trigger_future = loop.create_future()

    thread = Thread(
        kwargs={
            "loop": loop,
            "shutdown_trigger_future": shutdown_trigger_future,
        },
        target=run_server,
    )
    thread.start()

    # If we don't sleep, we'll complete the future before the server is running
    time.sleep(1)

    shutdown_trigger_future.set_result(None)
    print("SHUTDOWN, BABY!")
    thread.join()


main()
