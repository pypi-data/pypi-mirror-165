import datetime
import time
import logging
from collections import namedtuple
from typing import Callable, Optional, Dict

from refinitiv.data._core.log_reporter import LogReporter
from refinitiv.data._core.session import Session
from refinitiv.data._errors import SessionError

try:
    from ema import (
        OmmConsumer,
        OmmConsumerConfig,
        AppClient,
        CustomLoggerClient,
        LoggerSeverity,
        MapEntry,
        Msg,
        OmmConsumerEvent,
        RefreshMsg,
        LoginRefresh,
        EmaOmmInvalidHandleException,
        EmaOmmInvalidUsageException,
    )  # noqa

    EMA_INSTALLED = True
except ImportError as e:
    EMA_INSTALLED = False
    _exc_info = e
else:
    from .conversion import json_marketprice_msg_to_ema
    from .ema import (
        ema_login_message,
        create_programmatic_cfg,
        name_type_map,
        generate_login_msg,
    )


if EMA_INSTALLED:

    class EmaPythonLogger(CustomLoggerClient):
        def __init__(self):
            super().__init__(EmaPythonLogger.log)

        severity_logging_map: dict = {
            LoggerSeverity.NoLogMsg: 1000,  # higher than critical to avoid logging
            LoggerSeverity.Error: logging.ERROR,
            LoggerSeverity.Warning: logging.WARNING,
            LoggerSeverity.Success: logging.INFO,
            LoggerSeverity.Verbose: logging.DEBUG,
        }

        @staticmethod
        def log(callback_client_name: str, severity: LoggerSeverity, message: str):
            logging.log(
                EmaPythonLogger.severity_logging_map[severity],
                f"PythonLogger - {callback_client_name}: {message}",
            )


handle_tuple = namedtuple("handle_tuple", ["handle", "msg"])


class RwfSocketClient(LogReporter):
    """Emulating WebsocketApp + WSAPI"""

    def __init__(
        self,
        host: str,
        port: int,
        on_open: Callable,
        on_message: Callable,
        on_close: Callable,
        session: "Session",
        field_dict_path: Optional[str] = None,
        enumtype_path: Optional[str] = None,
        python_logger: bool = True,
    ):
        LogReporter.__init__(self, logger=session.logger())
        if not EMA_INSTALLED:
            self.debug(f"EMA not installed, message: {_exc_info}")
            raise ImportError("You need to install refinitiv-ema to use RwfSocketApp")

        self.host = host
        self.port = port

        self.field_dict_path = field_dict_path
        self.enumtype_path = enumtype_path
        self.on_open = on_open
        self.on_message = on_message
        self.on_close = on_close
        self.id = None
        self.handles: Dict[int, handle_tuple] = {}  # stream_id: (handle, msg)
        self.consumer: Optional[OmmConsumer] = None
        self.keep_running = False
        self._reissue_handle = None
        self._reissue_timestamp = 0

        def refresh_msg_cb(msg: RefreshMsg, event: OmmConsumerEvent):
            # TODO: Ema example has LoginRefresh and reissue timestamp inside,
            #  possibly useful?
            self._reissue_handle = event.get_handle()
            tmp_refresh = LoginRefresh(msg)
            if tmp_refresh.has_authentication_tt_reissue():
                self._reissue_timestamp = tmp_refresh.get_authentication_tt_reissue()
            else:
                self._reissue_timestamp = 0

        def msg_cb(msg: Msg, event: OmmConsumerEvent):
            on_message([msg.to_dict()])

        def nothing_callback(*_, **__):
            pass
            # logger.debug(f"login client message: {msg.json()}")

        self.client = AppClient(
            on_refresh_msg=msg_cb,
            on_update_msg=msg_cb,
            on_status_msg=msg_cb,
        )

        self.login_client = AppClient(
            on_refresh_msg=refresh_msg_cb,
            on_update_msg=nothing_callback,
            on_status_msg=msg_cb,
        )
        if python_logger:
            self.ema_logger = EmaPythonLogger()
        else:
            self.ema_logger = None  # Will use internal OmmLoggerClient

    def close(self, **_):
        self.keep_running = False
        self.on_close(self, -100, "Just Closed")
        # this should normally be done on __del__ automatically, but we have a bug
        if self.consumer:
            del self.consumer

    def run_forever(self):
        self.on_open(self)
        self.keep_running = True

        try:
            while self.keep_running:
                time.sleep(0.2)

        except (Exception, KeyboardInterrupt, SystemExit) as e:
            # self._callback(self.on_error, e)
            if isinstance(e, SystemExit):
                # propagate SystemExit further
                raise
            # teardown()
            return not isinstance(e, KeyboardInterrupt)

    def _init_consumer(self, login_msg: dict):
        admin_msg = ema_login_message(**generate_login_msg(login_msg))
        pgcfg = create_programmatic_cfg(
            field_dict_path=self.field_dict_path,
            enumtype_path=self.enumtype_path,
            host=self.host,
            port=self.port,
        )
        config = OmmConsumerConfig().config(pgcfg).add_admin_msg(admin_msg)
        try:
            self.consumer = OmmConsumer(
                config,
                self.login_client,
                self.ema_logger,
            )
        except EmaOmmInvalidUsageException as e:
            self.close()
            raise SessionError(
                -1,
                "Error establishing connection to RSSL endpoint. "
                "Check the logs for more details",
            ) from e

    def _handle_reissue(self, msg):
        reissue_success = False
        if self._reissue_handle is not None and self._reissue_timestamp >= time.time():
            try:
                admin_msg = ema_login_message(**generate_login_msg(msg))
                self.consumer.reissue(admin_msg, self._reissue_handle)
                reissue_success = True
                self.info(
                    f"Sent reissue with handle {self._reissue_handle}"
                    f" and timestamp {self._reissue_timestamp}"
                )
            except EmaOmmInvalidHandleException:
                self.warning(
                    f"Reissue failed: reissue was valid till "
                    f"{datetime.datetime.fromtimestamp(self._reissue_timestamp)}.\n"
                    f"This is likely because connection was broken "
                    f"for more than 10 minutes."
                )
        return reissue_success

    def _handle_consumer(self, msg):
        self.info("Creating consumer")
        self._init_consumer(msg)
        if len(self.handles) > 0:
            self.info("Re-registering all streams")
            for _, msg in self.handles.copy().values():
                self._send_message(msg)

    def _send_message(self, msg: dict):
        handle = self.consumer.register_client(
            json_marketprice_msg_to_ema(msg, self.consumer.field_id_map),
            self.client,
        )
        self.handles[msg["ID"]] = handle_tuple(handle, msg)

    def send(self, msg: dict):
        msg_type = msg.get("Type", "Request")
        msg_domain = msg.get("Domain", "MarketPrice")

        if msg_type == "Pong":
            # do nothing
            pass

        elif msg_type == "Request":  # open
            if msg_domain == "MarketPrice":
                self._send_message(msg)
                # logger.debug(f"new client registered for {msg['Key']['Name']}")
            elif msg_domain == "Login":
                if not self._handle_reissue(msg):
                    self._handle_consumer(msg)
            else:
                raise ValueError(f"Unknown domain of Request message: {msg_domain}")

        elif msg_type == "Close":
            if msg_domain == "Login":
                self.close()  # TODO: is this right?
            else:
                # logger.debug("RwfSocket received Close message")
                self.consumer.unregister(self.handles[msg["ID"]].handle)

        else:
            raise ValueError(f"Unknown message type: {msg_type}")
