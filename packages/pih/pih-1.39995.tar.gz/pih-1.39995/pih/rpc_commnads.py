from dataclasses import dataclass
from typing import List, Tuple
from pih.collection import FullName, LoginPasswordPair

from pih.const import CONST, LogChannel, LogCommandName
from pih.rpc import RPC
from pih.tools import DataTools


@dataclass
class rpcCommand:
    host: str
    port: int
    name: str


class RPC_COMMANDS:

    class MARK:

        @staticmethod
        def create_rpc_command(command_name: str) -> rpcCommand:
            return rpcCommand(CONST.HOST.ORION.NAME(), CONST.RPC.PORT(), command_name)

        @staticmethod
        def ping() -> str:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command(CONST.RPC.PING_COMMAND))

        @staticmethod
        def get_free_marks() -> str:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("get_free_marks"))

        @staticmethod
        def is_mark_free(tab_number: str) -> str:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("is_mark_free"), tab_number)

        @staticmethod
        def get_mark_by_tab_number(value: str) -> dict:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("get_mark_by_tab_number"), value)

        @staticmethod
        def get_mark_by_person_name(value: str) -> dict:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("get_mark_by_person_name"), value)

        @staticmethod
        def get_free_marks_group_statistics() -> str:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("get_free_marks_group_statistics"))

        @staticmethod
        def get_free_marks_by_group_id(value: int) -> str:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("get_free_marks_by_group_id"), value)

        @staticmethod
        def set_full_name_by_tab_number(value: FullName, tab_number: str) -> bool:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("set_full_name_by_tab_number"), (value, tab_number))


        @staticmethod
        def create(full_name: FullName, tab_number: str, telephone: str = None) -> bool:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("create"), (full_name, tab_number, telephone))

        @staticmethod
        def set_telephone_by_tab_number(value: str, tab_number: str) -> bool:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("set_telephone_by_tab_number"), (value, tab_number))

        @staticmethod
        def make_mark_as_free_by_tab_number(tab_number: str) -> bool:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("make_mark_as_free_by_tab_number"), tab_number)

        @staticmethod
        def remove_by_tab_number(tab_number: str) -> bool:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("remove_by_tab_number"), tab_number)

        @staticmethod
        def get_all_persons() -> bool:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command("get_all_persons"))


    class AD:
    
        @staticmethod
        def create_rpc_command(command_name: str) -> rpcCommand:
            return rpcCommand(CONST.HOST.AD.NAME(), CONST.RPC.PORT(), command_name)

        @staticmethod
        def ping() -> str:
            return RPC.call(RPC_COMMANDS.AD.create_rpc_command(CONST.RPC.PING_COMMAND))

        @staticmethod
        def printer_list() -> List:
            return RPC.call(RPC_COMMANDS.AD.create_rpc_command("printer_list"))

    class USER(AD):

        @staticmethod
        def ping() -> str:
            return RPC.call(RPC_COMMANDS.USER.create_rpc_command(CONST.RPC.PING_COMMAND))

        @staticmethod
        def user_is_exsits_by_login(value: str) -> bool:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.USER.create_rpc_command("user_is_exsits_by_login"), value))

        @staticmethod
        def set_telephone(user_dn: str, telephone: str) -> bool:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.USER.create_rpc_command("user_set_telephone"), (user_dn, telephone)))

        @staticmethod
        def set_password(user_dn: str, password: str) -> bool:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.USER.create_rpc_command("user_set_password"), (user_dn, password)))

        @staticmethod
        def set_status(user_dn: str, status: str, container_dn: str) -> bool:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.USER.create_rpc_command("user_set_status"), (user_dn, status, container_dn)))

        @staticmethod
        def get_user_by_full_name(value: FullName) -> dict:
            return RPC.call(RPC_COMMANDS.USER.create_rpc_command("get_user_by_full_name"), value)

        @staticmethod
        def get_users_by_name(value: str) -> dict:
            return RPC.call(RPC_COMMANDS.USER.create_rpc_command("get_users_by_name"), value)

        @staticmethod
        def get_active_users_by_name(value: str) -> dict:
            return RPC.call(RPC_COMMANDS.USER.create_rpc_command("get_active_users_by_name"), value)

        @staticmethod
        def get_user_by_login(value: str) -> dict:
            return RPC.call(RPC_COMMANDS.USER.create_rpc_command("get_user_by_login"), value)

        @staticmethod
        def get_template_list() -> dict:
            return RPC.call(RPC_COMMANDS.USER.create_rpc_command("get_template_list"))

        def get_containers() -> dict:
            return RPC.call(RPC_COMMANDS.USER.create_rpc_command("get_containers"))

        @staticmethod
        def create_from_template(templated_user_dn: str, full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.USER.create_rpc_command("create_user_from_template"), (templated_user_dn, full_name, login, password, description, telephone, email)))

        @staticmethod
        def create_in_container(container_dn: str, full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.USER.create_rpc_command("create_user_in_container"), (container_dn, full_name, login, password, description, telephone, email)))

    class TEMPLATE:

        @staticmethod
        def create_rpc_command(command_name: str) -> rpcCommand:
            return rpcCommand(CONST.HOST.TEMPLATE.NAME(), CONST.RPC.PORT(1), command_name)


        @staticmethod
        def ping() -> str:
            return RPC.call(RPC_COMMANDS.MARK.create_rpc_command(CONST.RPC.PING_COMMAND))

        @staticmethod
        def create_user_document(path: str, date_now_string: str, web_site_name: str, web_site: str, email_address: str, full_name: FullName, tab_number: str, pc: LoginPasswordPair, polibase: LoginPasswordPair, email: LoginPasswordPair) -> rpcCommand:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.TEMPLATE.create_rpc_command("create_user_document"), (path, date_now_string, web_site_name, web_site, email_address, full_name, tab_number, pc, polibase, email)))

    class BACKUP_WORKER:
    
        @staticmethod
        def create_rpc_command(command_name: str) -> rpcCommand:
            return rpcCommand(CONST.HOST.BACKUP_WORKER.NAME(), CONST.RPC.PORT(), command_name)
            

        @staticmethod
        def ping() -> str:
            return RPC.call(RPC_COMMANDS.BACKUP_WORKER.create_rpc_command(CONST.RPC.PING_COMMAND))

    class LOG:
            
        @staticmethod
        def create_rpc_command(command_name: str) -> rpcCommand:
            return rpcCommand(CONST.HOST.LOG.NAME(), CONST.RPC.PORT(1), command_name)
            

        @staticmethod
        def ping() -> str:
            return RPC.call(RPC_COMMANDS.LOG.create_rpc_command(CONST.RPC.PING_COMMAND))


        @staticmethod
        def log(message: str, channel: LogChannel, level: int) -> str:
            return RPC.call(RPC_COMMANDS.LOG.create_rpc_command("log"), (message, channel.name, level))


        @staticmethod
        def command(command: LogCommandName, parameters: dict = None) -> str:
            return RPC.call(RPC_COMMANDS.LOG.create_rpc_command("command"), (command, parameters))

    class PRINTER:

        @staticmethod
        def create_rpc_command(command_name: str) -> rpcCommand:
            return rpcCommand(CONST.HOST.PRINTER.NAME(), CONST.RPC.PORT(2), command_name)
            

        @staticmethod
        def ping() -> str:
            return RPC.call(RPC_COMMANDS.PRINTER.create_rpc_command(CONST.RPC.PING_COMMAND))

        @staticmethod
        def status() -> str:
            return RPC.call(RPC_COMMANDS.PRINTER.create_rpc_command("printers_status"))

        @staticmethod
        def report() -> bool:
            return DataTools.rpc_unrepresent(RPC.call(RPC_COMMANDS.PRINTER.create_rpc_command("printers_report")))

