import asyncio
import datetime
import gc
import logging
import enum

from . import exceptions

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    for handler in logging.getLogger().handlers:
        logger.addHandler(handler)

import json
from .HTTPHelper import Socket

listeners = []

global socket

def call(name=None, *args):
    if name == None:
        name = "before_expire"
    for i in listeners:
        if i.__name__ == name:
            try:
                asyncio.get_event_loop().create_task(i(args))
            except:
                asyncio.get_event_loop().create_task(i())

class Client:

    class User:
        class _Token():
            text: str = ""
            call = None

            def __init__(self, call):
                self.call = call

            def __str__(self):
                return self.text

            def update(self, text: str, time: int, update_now=True):
                self.text = text
                if update_now:
                    asyncio.get_event_loop().call_later(time, self.call, "before_expire")

        token: _Token = None
        username: str = ""
        keyEnabled: bool = False

        def __init__(self, username, keyEnabled):
            self.username = username
            self.keyEnabled = keyEnabled

            logger.debug("User object has been created")

        class Attr:
            Password = "password"
            Username = "username"
            Key_Enabled = "keyEnabled"

        def edit(self, key: str, value):
            print(host)
            socket.Send_Request(
                url=host + "/api/account/edit",
                data=({
                    "token": str(self.token),
                    key: value
                }),
                method=socket.Methods.POST
            )

    host: None = ""
    port: int = 80
    allow_unsecure: bool = False
    keep_alive: bool = True

    user: User = User

    async def before_expire(self):
        r = socket.Send_Request(
            method=socket.Methods.POST,
            url=host + "/api/refresh-token",
            data=json.dumps({
                "token": str(self.user.token)
            })
        )

        self.user.token.update(str(r), int(r.headers["lifetime"]))
        logger.info("Token refreshed")

    def __init__(self, server="https://cry-vs.herokuapp.com", port=80, allow_unsecure=False, keep_alive=True):
        global socket
        global host
        host = server
        socket = Socket(host, port, self)
        self.port = port
        self.allow_unsecure = allow_unsecure
        self.keep_alive = keep_alive
        listeners.append(self.before_expire)

    def listen(self, func):
        listeners.append(func)

    def login(self, *args):
        server = host

        if not server.lower().startswith("https://cry-vs.herokuapp.com") and not server.lower().startswith(
                "https://beta-cry-vs.herokuapp.com"):
            logger.warning("This is not an official Crypto Versus host. Please proceed with caution")

        if server.lower().startswith("https://beta-cry-vs.herokuapp.com"):
            logger.warning(
                "This is the domain for the beta branch. Please switch to the main branch "
                "'https://cry-vs.herokuapp.com' if you don't know what you're doing. "
            )

        if server.lower().startswith("http://") and self.allow_unsecure is False:
            logger.critical(
                f"{server} could not be loaded as it is http. please change it to https or set allowUnsecure to True "
                f"in the class parameters.")
            return

        def complete(r):
            self.User.token = self.User._Token(call)

            try:
                event_loop = args[2]
            except IndexError:
                event_loop = True

            logger.debug(r.headers)
            logger.debug(listeners)
            self.user.token.update(
                text=r.text,
                time=int(r.headers["lifetime"])
            )

            self.get_user_info()
            call("on_ready", int(r.headers["lifetime"]))

            try:  # test if the 3rd argument has been passed
                if not event_loop:
                    logger.info(
                        "You have disabled the event loop, but the client will still work.")
                else:
                    try:
                        asyncio.get_event_loop().run_forever()  # runs the event loop. this is an infinite function so anything that needs to be done should be done before this
                    except KeyboardInterrupt:
                        logger.info("KeyboardInterrupt")

            except IndexError:  # if the 3rd argument is not passed, default to True and start the event loop
                try:
                    asyncio.get_event_loop().run_forever()  # runs the event loop. this is an infinite function so anything that needs to be done should be done before this
                except KeyboardInterrupt:
                    logger.info("KeyboardInterrupt")

        if len(args) == 0:
            logger.critical("No auth data provided. please provide a username and password, or an API token")
        elif len(args) == 1:
            logger.info("using API key")
            r = socket.Send_Request(
                method=socket.Methods.POST,
                url=server + "/api/login",
                data=json.dumps({
                    "key": args[0]
                })
            )
            if r.status_code == 401:
                raise exceptions.AuthFailed("Invalid credentials. the server returned 401")
            else:
                complete(r)
        elif len(args) == 2:
            logger.info("using username and password")
            r = socket.Send_Request(
                method=socket.Methods.POST,
                url=server + "/api/login",
                data=json.dumps({
                    "username": args[0],
                    "password": args[1]
                })
            )
            if r.status_code == 401:
                raise exceptions.AuthFailed("Invalid credentials. the server returned 401")
            else:
                complete(r)



    def get_user_info(self):
        r = json.loads(socket.Send_Request(
            method=socket.Methods.POST,
            url=host + "/api/account/info",
            data=json.dumps({
                "token": str(self.user.token)
            })
        ).content)

        print(r)

        self.user = self.User(
            username=r["user"],
            keyEnabled=r["keyEnabled"]
        )
