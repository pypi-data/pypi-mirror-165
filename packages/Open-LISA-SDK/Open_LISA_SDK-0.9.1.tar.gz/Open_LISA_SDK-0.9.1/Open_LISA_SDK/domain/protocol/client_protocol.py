import base64
import json

from ..decorators.message_protocol_track import with_message_protocol_track

from ..exceptions.invalid_path_exception import InvalidPathException
from ...common.protocol.message_protocol import MessageProtocol
from ..exceptions.sdk_exception import OpenLISAException
from ..exceptions.invalid_command import InvalidCommandException
from ...logging import log

SUCCESS_RESPONSE = "OK"
ERROR_RESPONSE = "ERROR"

COMMAND_DISCONNECT = "DISCONNECT"
COMMAND_GET_INSTRUMENTS = "GET_INSTRUMENTS"
COMMAND_GET_INSTRUMENT = "GET_INSTRUMENT"
COMMAND_GET_DETECTED_PHYSICAL_ADDRESSES = "GET_DETECTED_PHYSICAL_ADDRESSES"
COMMAND_CREATE_INSTRUMENT = "CREATE_INSTRUMENT"
COMMAND_CREATE_INSTRUMENT_COMMAND = "CREATE_INSTRUMENT_COMMAND"
COMMAND_UPDATE_INSTRUMENT = "UPDATE_INSTRUMENT"
COMMAND_DELETE_INSTRUMENT = "DELETE_INSTRUMENT"
COMMAND_DELETE_INSTRUMENT_COMMAND = "DELETE_INSTRUMENT_COMMAND"
COMMAND_GET_INSTRUMENT_COMMANDS = "GET_INSTRUMENT_COMMANDS"
COMMAND_VALIDATE_COMMAND = "VALIDATE_COMMAND"
COMMAND_SEND_COMMAND = "SEND_COMMAND"
COMMAND_GET_FILE = "GET_FILE"
COMMAND_GET_DIRECTORY_STRUCTURE = "GET_DIRECTORY_STRUCTURE"
COMMAND_CREATE_DIRECTORY = "CREATE_DIRECTORY"
COMMAND_DELETE_DIRECTORY = "DELETE_DIRECTORY"
COMMAND_SEND_FILE = "SEND_FILE"
COMMAND_DELETE_FILE = "DELETE_FILE"
COMMAND_EXECUTE_BASH = "EXECUTE_BASH"
# Only available when server is running in test mode
COMMAND_RESET_DATABASES = "RESET_DATABASES"


class ClientProtocol:
    def __init__(self, message_protocol: MessageProtocol):
        self._message_protocol = message_protocol

    def __is_valid_response(self, response):
        if response == SUCCESS_RESPONSE:
            return True
        if response == ERROR_RESPONSE:
            return False

        raise Exception("unknown response type: '{}'".format(response))

    def disconnect(self):
        self._message_protocol.send_msg(COMMAND_DISCONNECT)
        self._message_protocol.disconnect()
        return

    @with_message_protocol_track(output="LOG")
    def create_instrument_as_json_string(self, new_instrument):
        self._message_protocol.send_msg(COMMAND_CREATE_INSTRUMENT)
        self._message_protocol.send_msg(json.dumps(new_instrument))
        response_type = self._message_protocol.receive_msg()
        result_msg = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return result_msg
        else:
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def create_instrument_command_as_json_string(self, instrument_id, command_type, new_command):
        self._message_protocol.send_msg(COMMAND_CREATE_INSTRUMENT_COMMAND)
        self._message_protocol.send_msg(json.dumps(new_command))
        response_type = self._message_protocol.receive_msg()
        result_msg = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return result_msg
        else:
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def delete_instrument_command(self, command_id):
        command_id = str(command_id)
        self._message_protocol.send_msg(COMMAND_DELETE_INSTRUMENT_COMMAND)
        self._message_protocol.send_msg(command_id)
        response_type = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return
        else:
            result_msg = self._message_protocol.receive_msg()
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def update_instrument_as_json_string(self, id, updated_instrument):
        id = str(id)
        self._message_protocol.send_msg(COMMAND_UPDATE_INSTRUMENT)
        self._message_protocol.send_msg(id)
        self._message_protocol.send_msg(json.dumps(updated_instrument))
        response_type = self._message_protocol.receive_msg()
        result_msg = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return result_msg
        else:
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def delete_instrument_as_json_string(self, id):
        id = str(id)
        self._message_protocol.send_msg(COMMAND_DELETE_INSTRUMENT)
        self._message_protocol.send_msg(id)
        response_type = self._message_protocol.receive_msg()
        result_msg = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return result_msg
        else:
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def get_instruments_as_json_string(self):
        self._message_protocol.send_msg(COMMAND_GET_INSTRUMENTS)
        result = self._message_protocol.receive_msg()
        return result

    @with_message_protocol_track(output="LOG")
    def get_instrument_as_json_string(self, id):
        id = str(id)
        self._message_protocol.send_msg(COMMAND_GET_INSTRUMENT)
        self._message_protocol.send_msg(id)
        response_type = self._message_protocol.receive_msg()
        result_msg = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return result_msg
        else:
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def get_detected_physical_addresses(self):
        self._message_protocol.send_msg(
            COMMAND_GET_DETECTED_PHYSICAL_ADDRESSES)
        response_type = self._message_protocol.receive_msg()
        result_msg = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return result_msg
        else:
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def get_instrument_commands_as_json_string(self, id):
        id = str(id)
        self._message_protocol.send_msg(COMMAND_GET_INSTRUMENT_COMMANDS)
        self._message_protocol.send_msg(id)
        response_type = self._message_protocol.receive_msg()
        result_msg = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            return result_msg
        else:
            raise OpenLISAException(result_msg)

    @with_message_protocol_track(output="LOG")
    def validate_command(self, id, command):
        id = str(id)
        self._message_protocol.send_msg(COMMAND_VALIDATE_COMMAND)
        self._message_protocol.send_msg(id)
        self._message_protocol.send_msg(command)
        response_type = self._message_protocol.receive_msg()
        if not self.__is_valid_response(response_type):
            err = self._message_protocol.receive_msg()
            raise InvalidCommandException(
                "command '{}' is not valid: {}".format(command, err))

    @with_message_protocol_track(output="LOG")
    def send_command(self, id, command, command_result_output_file):
        id = str(id)
        json_str = self.send_command_and_result_as_json_string(
            id, command, command_result_output_file)

        if not json_str and command_result_output_file:
            return None

        command_execution_result_dict = json.loads(json_str)
        command_execution_value = command_execution_result_dict["value"]
        command_execution_type = command_execution_result_dict["type"]

        if not command_execution_value:  # output value was saved in server
            return command_execution_result_dict

        # BYTES are sent as a base64 string
        if command_execution_type == "BYTES":
            command_execution_result_dict["value"] = base64.b64decode(
                command_execution_value)
        return command_execution_result_dict

    @with_message_protocol_track(output="LOG")
    def send_command_and_result_as_json_string(self, id, command, command_result_output_file):
        id = str(id)
        self._message_protocol.send_msg(COMMAND_SEND_COMMAND)
        command_execution_request = {
            "instrument_id": id,
            "command_invocation": command,
            "command_result_output_file": command_result_output_file
        }
        self._message_protocol.send_msg(json.dumps(command_execution_request))
        response_type = self._message_protocol.receive_msg()
        if self.__is_valid_response(response_type):
            command_execution_result_json_str = None
            if not command_result_output_file:  # if result was saved in Server this message is not sent
                command_execution_result_json_str = self._message_protocol.receive_msg()

            return command_execution_result_json_str
        else:
            err = self._message_protocol.receive_msg()
            raise InvalidCommandException(
                "command '{}' for instrument {} is not valid: {}".format(command, id, err))

    @with_message_protocol_track(output="LOG")
    def send_file(self, file_bytes, file_target_name):
        self._message_protocol.send_msg(COMMAND_SEND_FILE)
        self._message_protocol.send_msg(file_target_name)
        self._message_protocol.send_msg(file_bytes, encode=False)

        response = self._message_protocol.receive_msg()
        if not self.__is_valid_response(response):
            err = self._message_protocol.receive_msg()
            raise InvalidPathException(err)

        return response

    @with_message_protocol_track(output="LOG")
    def delete_file(self, file_path):
        self._message_protocol.send_msg(COMMAND_DELETE_FILE)
        self._message_protocol.send_msg(file_path)

        response = self._message_protocol.receive_msg()
        if not self.__is_valid_response(response):
            err = self._message_protocol.receive_msg()
            raise InvalidPathException(err)

        return response

    @with_message_protocol_track(output="LOG")
    def get_file(self, remote_file_name):
        self._message_protocol.send_msg(COMMAND_GET_FILE)
        self._message_protocol.send_msg(remote_file_name)
        response_type = str(self._message_protocol.receive_msg())

        if not self.__is_valid_response(response_type):
            error_message = self._message_protocol.receive_msg()
            log.error("Error requesting remote file '{}' : {}".format(
                remote_file_name, error_message))
            raise OpenLISAException(error_message)

        file_bytes = self._message_protocol.receive_msg(decode=False)

        return file_bytes

    @with_message_protocol_track(output="LOG")
    def delete_file(self, remote_file):
        self._message_protocol.send_msg(COMMAND_DELETE_FILE)
        self._message_protocol.send_msg(remote_file)
        response_type = str(self._message_protocol.receive_msg())

        if not self.__is_valid_response(response_type):
            error_message = self._message_protocol.receive_msg()
            log.error("Error deleting remote file '{}' : {}".format(
                remote_file, error_message))
            raise OpenLISAException(error_message)

    @with_message_protocol_track(output="LOG")
    def get_directory_structure_as_json_string(self, remote_path):
        self._message_protocol.send_msg(COMMAND_GET_DIRECTORY_STRUCTURE)
        self._message_protocol.send_msg(remote_path)
        response_type = str(self._message_protocol.receive_msg())

        if not self.__is_valid_response(response_type):
            error_message = self._message_protocol.receive_msg()
            log.error("Error getting remote directory structure '{}' : {}".format(
                remote_path, error_message))
            raise OpenLISAException(error_message)
        else:
            directory_structure_as_json_string = self._message_protocol.receive_msg()
            return directory_structure_as_json_string

    @with_message_protocol_track(output="LOG")
    def create_directory(self, remote_path, new_directory_name):
        self._message_protocol.send_msg(COMMAND_CREATE_DIRECTORY)
        self._message_protocol.send_msg(remote_path)
        self._message_protocol.send_msg(new_directory_name)
        response_type = str(self._message_protocol.receive_msg())

        if not self.__is_valid_response(response_type):
            error_message = self._message_protocol.receive_msg()
            log.error("Error creating remote directory '{}' : {}".format(
                remote_path, error_message))
            raise OpenLISAException(error_message)

    @with_message_protocol_track(output="LOG")
    def delete_directory(self, remote_path):
        self._message_protocol.send_msg(COMMAND_DELETE_DIRECTORY)
        self._message_protocol.send_msg(remote_path)
        response_type = str(self._message_protocol.receive_msg())

        if not self.__is_valid_response(response_type):
            error_message = self._message_protocol.receive_msg()
            log.error("Error deleting remote directory '{}' : {}".format(
                remote_path, error_message))
            raise OpenLISAException(error_message)

    @with_message_protocol_track(output="LOG")
    def execute_bash_command(self, command, capture_stdout, capture_stderr):
        stdout = None
        stderr = None
        self._message_protocol.send_msg(COMMAND_EXECUTE_BASH)
        self._message_protocol.send_msg(command)
        self._message_protocol.send_msg(str(capture_stdout))
        self._message_protocol.send_msg(str(capture_stderr))
        status_code = str(self._message_protocol.receive_msg())
        log.info(
            "Status code after remote bash command execution: {}".format(status_code))

        if capture_stdout:
            stdout = str(self._message_protocol.receive_msg())
            log.debug("Remote execution command stdout: {}".format(stdout))

        if capture_stderr:
            stderr = str(self._message_protocol.receive_msg())
            log.debug("Remote execution command stderr: {}".format(stderr))

        return status_code, stdout, stderr

    def reset_databases(self):
        self._message_protocol.send_msg(COMMAND_RESET_DATABASES)
        return self._message_protocol.receive_msg()
