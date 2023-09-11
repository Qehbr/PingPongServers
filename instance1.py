import asyncio
import time
from fastapi import FastAPI
import requests
import uvicorn


app1 = FastAPI()
pong_time_ms = None  # time between ponging
time_when_pinged = None  # time when server was pinged last time
time_to_resume = None  # time to send next ping if server was paused
paused = False  # if server paused


@app1.get("/ping")
async def ping(pong_time_query):
    """
    Handling ping request from starting server or from Server 2
    :param pong_time_query: Time to wait for sending new ping
    :return: Message to cli
    """
    try:
        global time_when_pinged
        global pong_time_ms
        global time_to_resume
        # if server is not paused and properly got query
        if not paused and pong_time_query:
            # save time when server was pinged for calculating resuming time
            time_when_pinged = time.time()
            pong_time_ms = int(pong_time_query)
            if pong_time_ms is not None:  # server could be paused or stopped
                # if server was resumed
                if time_to_resume:
                    print(f"{time.strftime('%H:%M:%S')} Server 1: Resumed")
                    # send ping in remaining time from stopping
                    asyncio.create_task(new_ping(time_to_resume))
                    time_to_resume = None
                else:
                    print(f"{time.strftime('%H:%M:%S')} Server 1: Got Ping, responding pong")
                    # send ping in default time
                    asyncio.create_task(new_ping(pong_time_ms))
                return {"message": "pong"}
            else:
                return {"message": "Game not started or paused"}
        else:
            return {"message": "Game not started or paused"}
    except ValueError:
        pass


async def new_ping(time_to_wait):
    """
    Function to send ping to other server
    :param time_to_wait: Time to wait for sending new ping
    :return: Message to cli
    """
    global pong_time_ms
    await asyncio.sleep(time_to_wait / 1000)
    # if server is not stopped or paused when waiting
    if pong_time_ms is not None and not paused:
        print(f"{time.strftime('%H:%M:%S')} Server 1: Sending new ping")
        requests.get(f"http://localhost:8001/ping?pong_time_query={pong_time_ms}")


@app1.get("/start")
async def start(pong_time_query):
    """
    Starting new game
    :param pong_time_query: Time between pings
    :return: Message to cli
    """
    global pong_time_ms
    pong_time_ms = int(pong_time_query)
    await ping(pong_time_query)
    return {"message": "Servers are successfully started"}


@app1.get("/stop")
async def stop():
    """
    Stopping the server
    :return: Message to cli
    """
    global pong_time_ms
    pong_time_ms = None
    return {"message": "Server 1 successfully stopped"}


@app1.get("/pause")
async def pause():
    """
    Pausing the server and saving remaining time
    :return: Message to cli
    """
    global pong_time_ms
    global time_when_pinged
    global time_to_resume
    global paused

    paused = True

    if not pong_time_ms:
        return {"message": "Server 1 has not started yet or already paused"}

    # calculate time between pinging
    resume_time = time.time() - time_when_pinged
    print(resume_time)
    print("Server Paused")
    # if this server should send next ping
    if resume_time <= pong_time_ms / 1000:
        time_to_resume = resume_time * 1000
        return {"message": "Server 1 successfully paused"}
    return {"message": "Server 1 was not waiting for new pong and successfully paused"}


@app1.get("/resume")
async def resume():
    """
    Resuming the server
    :return: Message to cli
    """
    global paused
    global pong_time_ms

    if not pong_time_ms or paused:
        return {"message": "Server 1 has not started or paused"}

    paused = False
    # if this server should send next ping
    if time_to_resume:
        await ping(int(pong_time_ms))
    return {"message": "Server 1 successfully resume"}


if __name__ == "__main__":
    uvicorn.run(app1, host="localhost", port=8000)
