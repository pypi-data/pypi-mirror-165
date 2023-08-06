import json
import logging
import subprocess
from os import environ
from pathlib import Path
from time import sleep
from typing import Any, Dict, List

import httpx

from .._binary import check_binary
from .._config import config
from . import common
from .errors import (  # UnprocessableEntityError,
    AlreadyConnectedError,
    BaseStartEngineError,
    EngineConnectionError,
    EngineRequestError,
    NotConnectedError,
    StartEngineError,
    handler_error,
)

log: logging.Logger = logging.getLogger()


class SyncEngine:
    __slots__ = (
        "db_uri",
        "db_provider",
        "db_timeout",
        "connect_timeout",
        "url",
        "process",
        "session",
        "connected",
        "_binary_path",
    )

    def __init__(
        self,
        db_uri: str,
        db_provider: str,
        db_timeout: int = 10,
        connect_timeout: int = 10,
        url: str = None,
        process: subprocess.Popen = None,
        session: httpx.Client = None,
    ) -> None:
        self.db_uri = db_uri
        self.db_provider = db_provider
        self.db_timeout = db_timeout
        self.connect_timeout = connect_timeout

        self.url: str = url
        self.process: subprocess.Popen = process
        self.session: httpx.Client = session
        self.connected = False
        self._binary_path: Path = None

    def __del__(self):
        if self.process:
            self.url = None
            self.process.kill()
            self.process = None
            self.connected = False
            self.session = None

    def _close(self):
        if self.session and not self.session.is_closed:
            self.session.close()
        self.session = None

    def connect(self) -> None:
        if self.process:
            raise AlreadyConnectedError("Already connected to the engine")

        self.session: httpx.Client = httpx.Client(timeout=self.db_timeout)
        self._binary_path = check_binary()

        try:
            self.spawn(file=Path(self._binary_path))
        except Exception:
            self._close()
            raise

    def disconnect(self) -> None:
        self._close()
        if not self.process:
            raise NotConnectedError("Not connected")

        self.url = None
        self.process.kill()
        self.process = None
        self.connected = False

    def _try_comunicate(self):
        try:
            stdout, stderr = self.process.communicate(timeout=0.03)

            stderr = stderr.decode()
            stdout = stdout.decode()

            std = stdout or stderr

            try:
                data = json.loads(std)
                self.disconnect()
                raise StartEngineError(error=data)
            except (json.JSONDecodeError, TypeError):
                self.disconnect()
                raise BaseStartEngineError(std)
        except subprocess.TimeoutExpired:
            pass

    def spawn(self, file: Path) -> None:
        port = common.get_open_port()
        log.debug(f"Running engine on port: {port}")

        self.url = f"http://localhost:{port}"

        dml = common.get_dml()

        dml = dml.replace("postgres", self.db_provider)
        dml = dml.replace("DATASOURCE_URL", self.db_uri)

        env = environ.copy()

        env.update(
            PRISMA_DML=dml,
            RUST_LOG="error",
            RUST_LOG_FORMAT="json",
            PRISMA_CLIENT_ENGINE_TYPE="binary",
        )

        args: List[str] = [str(file.absolute()), "-p", str(port), "--enable-raw-queries"]

        log.debug("Starting engine...")
        self.process = subprocess.Popen(
            args,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._try_comunicate()

        self._check_connect()

    def request(
        self, method: config.method, path: str, *, content: Any = None
    ) -> Dict[str, Any]:
        if not self.url:
            raise NotConnectedError("Not connected to the engine")

        kwargs = {
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        }

        if content:
            kwargs["content"] = content

        url = self.url + path
        log.debug(f"Sending {method} request to {url} with content: {content}")

        resp = self.session.request(method=method, url=url, **kwargs)

        if resp.is_success:
            response = resp.json()

            log.debug(f"{method} {url} returned {len(response)} results")

            errors_data = response.get("errors")
            if errors_data:
                handler_error(errors=errors_data)

            return response

        raise EngineRequestError(f"{resp.status_code}: {resp.text}")

    def _check_connect(self) -> None:
        last_err = None
        for _ in range(int(self.connect_timeout / 0.01)):
            try:
                self.request("GET", "/status")
                self.connected = True
                return
            except Exception as err:
                sleep(0.01)
                log.debug(
                    (
                        "Could not connect to engine due to "
                        f"{err.__class__.__name__}; retrying...{err}"
                    )
                )
                last_err = err

        self._try_comunicate()

        self.disconnect()

        raise EngineConnectionError("Could not connect to the engine") from last_err
