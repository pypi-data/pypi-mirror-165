import os
import importlib.util

from pih.collection import LogCommand
from pih.const import LOG_CHANNEL_DICT, LogChannel, LogLevel, LogType

telegram_send_library_is_exsits = importlib.util.find_spec(
    "telegram_send") is not None

#path.append("//pih/facade")

if telegram_send_library_is_exsits:
    import telegram_send

    CONFIG_LOCATION: str = "telegram_send_config"

    class Log():

        @staticmethod
        def send(log_type: LogType, message: str, log_channel: LogChannel = LogChannel.DEFAULT, log_level: int = 0) -> None:
            #
            def message_decorattion_for_log_level(message: str, log_level: LogLevel) -> str:
                if (log_level & LogLevel.ERROR.value) == LogLevel.ERROR.value:
                    return f"Error: {message}"
                return message
            #
            def message_decorattion_for_log_type(message: str, log_type: LogType) -> str:
                if log_type == LogType.COMMAND:
                    return f"[{message}]"
                return message
            #
            log_type = log_type or LogType.DEFAULT
            log_channel = log_channel or LogChannel.DEFAULT
            log_level = log_level or LogLevel.DEFAULT
            dir = os.path.dirname(__file__)
            config = os.path.join(dir, CONFIG_LOCATION, LOG_CHANNEL_DICT[log_channel])
            telegram_send.send(messages=[message_decorattion_for_log_type(message_decorattion_for_log_level(message, log_level), log_type)],
                               conf=config)

        def write_to_data_base(log_type: str, message: str, group_name: str, log_level: int) -> int:
            return -1

        @staticmethod
        def write(message: str, log_channel: LogChannel = LogChannel.DEFAULT, log_level: int = 0) -> int:
            Log.send(LogType.MESSAGE, message, log_channel, log_level)
            return Log.write_to_data_base(LogType.MESSAGE, message, log_channel, log_level)

        @staticmethod
        def execute(command: LogCommand, params: dict) -> int:
            log_channel = command.log_channel
            log_level = command.log_level
            if params is not None:
                message = command.message.format(**params)
            else:
                message = command.message
            Log.send(LogType.COMMAND, message, log_channel, log_level)
            return Log.write_to_data_base(LogType.COMMAND, command, log_channel, log_level)
else:
    raise NotImplemented("Telegram send library")
