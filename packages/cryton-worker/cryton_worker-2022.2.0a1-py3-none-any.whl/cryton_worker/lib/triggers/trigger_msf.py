import time
from copy import deepcopy
from threading import Thread
from multiprocessing import Queue

from cryton_worker.lib.util import logger, util, constants as co, exceptions
from cryton_worker.lib.triggers.trigger_base import Trigger


class MSFTrigger(Trigger):
    def __init__(self, host: str, port: int, main_queue: Queue):
        super().__init__(host, port, main_queue)
        self.msf = util.Metasploit()
        self._stopped = True

    def add_activator(self, details: dict) -> str:
        """
        Add activator to Trigger and start the Trigger.
        :param details: Activator options
            Example:
            {
                'host': str,
                'port': int,
                "reply_to": str,
                "identifiers": {
                    type: 'shell'
                    tunnel_local: '192.168.56.10:555'
                    via_exploit: 'exploit/multi/handler'
                    via_payload: 'payload/python/shell_reverse_tcp'
                    desc: 'Command shell'
                    info: ''
                    workspace: 'false'
                    session_host: '192.168.56.1'
                    session_port: '48584'
                    target_host: ''
                    username: 'vagrant'
                    uuid: 'o3mnfksh'
                    exploit_uuid: 'vkzl8sib'
                    routes: ''
                    arch: 'python'
                }
            }
        :return: ID of the new activator
        """
        logger.logger.debug("Adding activator to MSFTrigger.", host=self._host, port=self._port, details=details)
        if self.any_activator_exists():
            raise exceptions.TooManyActivators(str(self))
        activator_id = str(self._generate_id())
        details.update({co.TRIGGER_ID: activator_id})
        with self._activators_lock:
            self._activators.append(details)
            self.start()
        return activator_id

    def remove_activator(self, activator: dict) -> None:
        """
        Remove activator from Trigger and optionally stop the Trigger.
        :param activator: Desired activator
        :return: None
        """
        logger.logger.debug("Removing activator from MSFTrigger.", host=self._host, port=self._port,
                            activator_id=activator.get(co.TRIGGER_ID))
        with self._activators_lock:
            self._activators.remove(activator)
            if not self.any_activator_exists():
                self.stop()

    def _check_for_session(self) -> None:
        """
        Check regularly for created session and if is found send it.
        :return: None
        """
        details = self._activators[0]
        session_match_conditions = {}

        if (identifiers := details.get(co.IDENTIFIERS)) is not None:
            session_match_conditions = identifiers
        else:
            if via_exploit := details.get(co.EXPLOIT):
                session_match_conditions["via_exploit"] = via_exploit
                if via_payload := details.get(co.PAYLOAD):
                    session_match_conditions["via_payload"] = via_payload
            elif auxiliary := details.get(co.AUXILIARY):
                session_match_conditions["via_exploit"] = auxiliary

        logger.logger.debug("Checking for MSFTrigger's session.", host=self._host, port=self._port,
                            session_conditions=session_match_conditions)
        while not self._stopped and self.msf.is_connected():
            active_sessions = self.msf.get_sessions(**session_match_conditions)
            if active_sessions:
                message_body = {
                    co.EVENT_T: co.EVENT_TRIGGER_STAGE,
                    co.EVENT_V: {co.TRIGGER_ID: details.get(co.TRIGGER_ID), co.TRIGGER_PARAMETERS: active_sessions[-1]}
                }
                time.sleep(3)  # MSF limitation. If we use the session immediately, it may not give output.
                self._notify(self._activators[0].get(co.REPLY_TO), message_body)
                break
            time.sleep(5)

    def start(self) -> None:
        """
        Start the Trigger.
        :return: None
        """
        if self._stopped:
            if not self.msf.is_connected():
                raise exceptions.MsfConnectionError
            print(f"Starting MSFTrigger. host: {self._host} port: {self._port}")

            logger.logger.debug("Starting MSFTrigger.", host=self._host, port=self._port)
            details = deepcopy(self._activators[0])

            if co.EXPLOIT in details:
                self.msf.execute_exploit(details.pop(co.EXPLOIT), details.pop(co.PAYLOAD, None),
                                         details.pop(co.EXPLOIT_ARGUMENTS, None),
                                         details.pop(co.PAYLOAD_ARGUMENTS, None))
            elif co.AUXILIARY in details:
                self.msf.execute_auxiliary(details.pop(co.AUXILIARY), details.pop(co.AUXILIARY_ARGUMENTS, None))
                
            self._stopped = False
            t = Thread(target=self._check_for_session)
            t.start()

    def stop(self) -> None:
        """
        Stop the Trigger.
        :return: None
        """
        if not self._stopped:
            print(f"Stopping MSFTrigger. host: {self._host} port: {self._port}")
            logger.logger.debug("Stopping MSFTrigger.", host=self._host, port=self._port)
            self._stopped = True
