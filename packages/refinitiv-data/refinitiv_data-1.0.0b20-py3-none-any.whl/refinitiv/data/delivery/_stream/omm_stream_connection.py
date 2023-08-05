# coding: utf-8

from .event import StreamEvent
from .stream_connection import StreamConnection, LOGIN_STREAM_ID
from .stream_cxn_state import StreamCxnState


class OMMStreamConnection(StreamConnection):
    @property
    def subprotocol(self) -> str:
        return "tr_json2"

    def get_login_message(self):
        login_message = {
            "Domain": "Login",
            "ID": LOGIN_STREAM_ID,
            "Key": self._session.get_omm_login_message(),
        }
        return login_message

    def get_close_message(self) -> dict:
        close_message = {
            "Domain": "Login",
            "ID": LOGIN_STREAM_ID,
            "Type": "Close",
        }
        return close_message

    def _handle_login_message(self, message: dict):
        """
        Parameters
        ----------
        message
            {
                'ID': 2,
                'Type': 'Refresh',
                'Domain': 'Login',
                'Key':
                    {
                        'Name': TOKEN_HERE,
                        'Elements': {
                            'AllowSuspectData': 1, 'ApplicationId': '256',
                            'ApplicationName': 'RTO',
                            'AuthenticationErrorCode': 0,
                            'AuthenticationErrorText': {
                                'Type': 'AsciiString', 'Data': None
                            },
                            'AuthenticationTTReissue': 1634562361,
                            'Position': '10.46.188.21/EPUAKYIW3629',
                            'ProvidePermissionExpressions': 1,
                            'ProvidePermissionProfile': 0,
                            'SingleOpen': 1, 'SupportEnhancedSymbolList': 1,
                            'SupportOMMPost': 1,
                            'SupportPauseResume': 0, 'SupportStandby': 0,
                            'SupportBatchRequests': 7,
                            'SupportViewRequests': 1, 'SupportOptimizedPauseResume': 0
                        }
                    },
                'State':
                    {
                        'Stream': 'Open', 'Data': 'Ok',
                        'Text': 'Login accepted by host ads-fanout-lrg-az2-apse1-prd.'
                    }, 'Elements': {'PingTimeout': 30, 'MaxMsgSize': 61426}
            }
        """

        state = message.get("State", {})
        stream_state = state.get("Stream")

        if stream_state == "Open":
            self._state = StreamCxnState.MessageProcessing
            self._connection_result_ready.set()

        elif stream_state == "Closed":
            self.debug(
                f"{self._classname} received a closing message: "
                f"state={self.state}, message={message}"
            )
            self._state = StreamCxnState.Disconnected
            not self.can_reconnect and self._connection_result_ready.set()

        else:
            state_code = state.get("Code", "")
            text = state.get("Text", "")

            if "Login Rejected." in text or state_code == "UserUnknownToPermSys":
                self._config.info_not_available()

                if not self.can_reconnect:
                    self.debug(f"Connection error: {message}")
                    self._state = StreamCxnState.Disconnected
                    self._connection_result_ready.set()

            else:
                raise ValueError(
                    f"{self._classname}._handle_login_message() | "
                    f"Don't know what to do state={self.state}, message={message}"
                )

    def _process_message(self, message: dict) -> None:
        self.debug(f"{self._classname} process message {message}")
        message_type = message.get("Type")
        stream_id = message.get("ID")
        event = StreamEvent.get(stream_id)

        if message_type == "Refresh":
            self._emitter.emit(event.refresh_by_id, self, message)
            message_complete = message.get("Complete", True)
            message_complete and self._emitter.emit(event.complete_by_id, self, message)

        elif message_type == "Update":
            self._emitter.emit(event.update_by_id, self, message)

        elif message_type == "Status":
            self._emitter.emit(event.status_by_id, self, message)

        elif message_type == "Error":
            self._emitter.emit(event.error_by_id, self, message)

        elif message_type == "Ping":
            pong_message = {"Type": "Pong"}
            self.send_message(pong_message)

        else:
            raise ValueError(f"Unknown message {message}")
