import abc
import calendar
from dataclasses import dataclass
from datetime import datetime
import enum
from getpass import getpass
import locale
import os
import platform
import re
import subprocess
import sys
from typing import Any, Callable, Dict, Generic, List, Tuple, TypeVar
import colorama
from colorama import Back, Style, ansi, Fore
from prettytable import PrettyTable
import win32com.client

# sys.path.append("//pih/facade")
from pih.collection import ActionValue, CommandChainItem, CommandLinkItem, FieldItem, CommandItem, FieldItemList, FullName, LogCommand, LoginPasswordPair, Mark, MarkGroup, MarkGroupStatistics, ParamItem, PasswordSettings, Result, User, UserContainer
from pih.const import CONST, EXECUTOR, FIELD_NAME_COLLECTION, FIELD_COLLECTION, LOG_COMMAND_LIST, PASSWORD, PATHS, USER_PROPERTY, LogChannel, LogCommandName, LogLevel
from pih.rpc_commnads import RPC_COMMANDS
from pih.tools import DataTools, ResultUnpack, ResultTools, FullNameTool, PasswordTools


class NotImplemented(BaseException):
    pass


class NotFound(BaseException):
    pass


class UserInterruption(BaseException):
    pass


class CommandNameIsExistsAlready(BaseException):
    pass


class CommandFullFileNameIsExistAlready(Exception):
    pass


class CommandNameIsNotExists(Exception):
    pass


@dataclass
class Command:
    group: str
    command_name: str
    file: str
    description: str
    section: str
    cyclic: bool
    confirm_for_continue: bool = True


@dataclass
class CommandLink:
    command_name: str
    data_extractor_name: str


@dataclass
class CommandChain:
    name: str
    input_name: str
    description: str
    list: List[CommandLink]
    confirm_for_continue: bool = True
    enable: bool = True

T = TypeVar('T')

class GenericCommandList(Generic[T]):

    def __init__(self):
        self.command_list: List[T] = []
        self.name_dict: Dict[str, T] = {}
        self.index_dict: Dict[int, str] = {}
        self.index = 0

    def length(self) -> int:
        return len(self.command_list)

    def get_by_index(self, index: int) -> T:
        return self.name_dict[self.index_dict[index]]

    def get_by_name(self, name: str) -> T:
        name = name.lower()
        for key in self.name_dict:
            key_lower = key.lower()
            if key_lower == name:
                return self.name_dict[key]
        #raise KeyError
        return None

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index > self.length():
            self.index = 0
            raise StopIteration
        return self.index, self.get_by_index(self.index - 1)


class CommandList(GenericCommandList[Command]):

    def register(self, command: Command) -> None:
        def get_command_file_name(command: Command) -> str:
            return command.group + command.file + command.section
        if command.command_name in map(lambda item: item.command_name, self.command_list):
            raise CommandNameIsExistsAlready()
        if get_command_file_name(command) in map(lambda item: get_command_file_name(item), self.command_list):
            raise CommandFullFileNameIsExistAlready(
                f"{command.command_name}: {get_command_file_name(command)}")
        self.command_list.append(command)
        self.name_dict[command.command_name] = command
        self.index_dict[self.length() - 1] = command.command_name


class CommandChainList(GenericCommandList[CommandChain]):

    def register(self, item: CommandChain) -> None:
        if item.name in map(lambda item: item.name, self.command_list):
            raise CommandNameIsExistsAlready()
        self.command_list.append(item)
        self.name_dict[item.name] = item
        self.index_dict[self.length() - 1] = item.name


class ICommandListStorage(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "get_command_list") and
                callable(subclass.get_command_list) or
                NotImplemented)

    @abc.abstractmethod
    def get_command_list(self) -> CommandList:
        raise NotImplemented

class CommandTools:

    @staticmethod
    def get_command_group_path(command: Command) -> str:
        return f"{CONST.FACADE.PATH}{command.group}{CONST.FACADE.COMMAND_SUFFIX}"

    @staticmethod
    def get_file_extension(file: str) -> str:
        return "" if file.find(".") == -1 else file.split(".")[-1]

    @staticmethod
    def convert_command_to_command_file_path(command: Command) -> str:
        shell = win32com.client.Dispatch("WScript.Shell")
        return shell.CreateShortCut(command.file).Targetpath if CommandTools.get_file_extension(command.file) == "lnk" else command.file

    @staticmethod
    def get_executor_path(path: str) -> str:
        return EXECUTOR.get(CommandTools.get_file_extension(path))

    @staticmethod
    def convert_command_file_path_for_executor(path: str, executor: str) -> str:
        if executor == EXECUTOR.POWERSHELL_EXECUTOR or executor == EXECUTOR.VBS_EXECUTOR:
            path = f".\\{path}"
        return path

    @staticmethod
    def set_cwd(path: str) -> None:
        os.chdir(path)

    @staticmethod
    def check_for_command_paths_exsit(command: Command):
        command_group_directory_path = CommandTools.get_command_group_path(
            command)
        if not os.path.exists(command_group_directory_path):
            return CommandPathExsitsStatus.COMMAND_GROUP_DIRECTORY_IS_NOT_EXSITS
        CommandTools.set_cwd(command_group_directory_path)
        command.file = CommandTools.convert_command_to_command_file_path(
            command)
        if not os.path.exists(command.file):
            return CommandPathExsitsStatus.COMMAND_FILE_IS_NOT_EXSITS
        command.file = CommandTools.convert_command_file_path_for_executor(
            command.file, CommandTools.get_executor_path(command.file))
        return CommandPathExsitsStatus.OK
#


class CommandPathExsitsStatus(enum.Enum):
    OK: int = 0
    COMMAND_GROUP_DIRECTORY_IS_NOT_EXSITS: int = 1
    COMMAND_FILE_IS_NOT_EXSITS: int = 2


class LocalCommandListStorage(ICommandListStorage):

    def __init__(self, command_list_dict: dict):
        self.command_list_dict = command_list_dict
        self.command_list: CommandList = CommandList()
        self.command_chain_list: CommandChainList = CommandChainList()
        for command_name in self.command_list_dict:
            command_item_obj: Any = self.command_list_dict[command_name]
            if isinstance(command_item_obj, CommandItem):
                command_item: CommandItem = command_item_obj
                if command_item.enable:
                    command: Command = self.convert_to_command(
                        command_name, command_item)
                    try:
                        command_paths_exsits_check_status = CommandTools.check_for_command_paths_exsit(
                            command)
                        if command_paths_exsits_check_status == CommandPathExsitsStatus.COMMAND_GROUP_DIRECTORY_IS_NOT_EXSITS:
                            PR.red(
                                f"Command {command.command_name}: group directory is not exsits!")
                        elif command_paths_exsits_check_status == CommandPathExsitsStatus.COMMAND_FILE_IS_NOT_EXSITS:
                            PR.red(
                                f"Command {command.command_name}: file is not exsits!")
                        elif command_paths_exsits_check_status == CommandPathExsitsStatus.OK:
                            self.command_list.register(command)
                    except CommandFullFileNameIsExistAlready:
                        PR.red(
                            f"Command: {command.command_name} is already exsits!")
        for command_name in self.command_list_dict:
            command_item_obj: Any = self.command_list_dict[command_name]
            if isinstance(command_item_obj, CommandChainItem):
                command_chain_item: CommandChainItem = self.command_list_dict[command_name]
                if command_chain_item.enable:
                    if self.command_list.get_by_name(command_name) is None:
                        try:
                            self.command_chain_list.register(
                                self.convert_to_command_chain(command_name, command_chain_item))
                        except CommandNameIsNotExists as error:
                            PR.red(
                                f"Command {command_name}: command link: {error} is not exsits!")
                    else:
                        PR.red(
                            f"Command: {command_chain_item.name} is already exsits!")

    def convert_to_command(self, name: str, command_item: CommandItem) -> Command:
        if name not in self.command_list_dict:
            raise CommandNameIsNotExists
        return Command(command_item.group, name,
                       command_item.file_name,
                       command_item.description,
                       command_item.section,
                       command_item.cyclic)

    def convert_to_command_chain(self, name: str, command_chain_item: CommandChainItem) -> CommandChain:
        if name not in self.command_list_dict:
            raise CommandNameIsNotExists
        list_command_chain: List[CommandChain] = []
        for link_item_obj in command_chain_item.list:
            link_item: CommandLinkItem = link_item_obj
            if self.command_list.get_by_name(link_item.command_name) is not None:
                list_command_chain.append(CommandLink(
                    link_item.command_name, link_item.data_extractor_name))
            else:
                raise CommandNameIsNotExists(link_item.command_name)
        return CommandChain(name,
                            command_chain_item.input_name,
                            command_chain_item.description,
                            list_command_chain,
                            command_chain_item.confirm_for_continue,
                            command_chain_item.enable)

    def get_command_list(self) -> CommandList:
        return self.command_list

    def get_command_chain_list(self) -> CommandChainList:
        return self.command_chain_list


class NamePolicy:

    @staticmethod
    def get_first_letter(name: str) -> str:
        from transliterate import translit
        return translit(name[0], 'ru', reversed=True).lower()

    @staticmethod
    def convert_to_login(full_name: FullName) -> FullName:
        return FullName(
            NamePolicy.get_first_letter(
                full_name.last_name),
            NamePolicy.get_first_letter(
                full_name.first_name),
            NamePolicy.get_first_letter(full_name.middle_name))

    @staticmethod
    def convert_to_alternative_login(login_list: FullName) -> FullName:
        return FullName(login_list.first_name, login_list.middle_name, login_list.last_name)

    @staticmethod
    def convert_to_reverse_login(login_list: FullName) -> FullName:
        return FullName(login_list.middle_name, login_list.first_name, login_list.last_name)


class PIH:

    version: str = "0.93"

    PATH: PATHS = PATHS

    class OS:

        @staticmethod
        def get_login() -> str:
            return os.getlogin()

        @staticmethod
        def get_computer_name() -> str:
            return platform.node()

    class AUTH:

        USE_AUTHENTIFICATION: bool = True

        def authenticate() -> bool:
            if PIH.AUTH.USE_AUTHENTIFICATION:
                import win32security
                PR.head("Аутентификация пользователя")
                login = PIH.OS.get_login()
                if PIH.INPUT.yes_no(f"Использовать пользователя: {login} ?", True):
                    pass
                else:
                    PR.input("Введите логин")
                    login = PIH.INPUT.input()
                PR.input("Введите пароль:")
                password = getpass("")
                try:
                    win32security.LogonUser(
                        login,
                        CONST.AD.DOMAIN_NAME,
                        password,
                        win32security.LOGON32_LOGON_NETWORK,
                        win32security.LOGON32_PROVIDER_DEFAULT
                    )
                    PIH.LOG_COMMAND.loggin()
                    PR.good("Добро пожаловать...")
                    return True
                except win32security.error:
                    PR.alert("Неверный пароль или логин. До свидания...")
                    return False
            else:
                return True

    class MC:

        @staticmethod
        def send_message(phone_number: str, message: str) -> bool:
            import pywhatkit as pwk
            try:
                pwk.sendwhatmsg_instantly(phone_number, message)
            except:
                pass

        def send_message_by_login(login: str, message: str) -> bool:
            user = ResultUnpack.unpack_first_data(
                PIH.RESULT.USER.by_login(login))
            if user:
                PIH.MC.send_message(
                    PIH.RESULT.EXTRACT.telephone(user), message)
            else:
                return False

    class FORMAT:
    
        @staticmethod
        def telephone(value: str) -> str:
            value = value.replace("(", "")
            value = value.replace(")", "")
            value = value.replace(" ", "")
            value = value.replace("-", "")
            if len(value) > 0 and (value[0] == "8" or value[0] == "7"):
                value = "+7" + value[1:]
            return value

        def name(value: str) -> str:
            return value[0].upper() + value[1:].lower()

    class RESULT:

        class EXTRACT:

            @staticmethod
            def parameter(object: dict, name: str) -> str:
                return object[name] if name in object else ""

            @staticmethod
            def tab_number(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.TAB_NUMBER)

            @staticmethod
            def telephone(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.TELEPHONE)

            @staticmethod
            def login(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.LOGIN)

            @staticmethod
            def name(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.NAME)

            @staticmethod
            def dn(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.DN)

            @staticmethod
            def group_name(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.GROUP_NAME)

            @staticmethod
            def as_full_name(mark_object: dict) -> FullName:
                return FullNameTool.from_string(PIH.RESULT.EXTRACT.full_name(mark_object))

            @staticmethod
            def full_name(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.FULL_NAME)

            @staticmethod
            def person_id(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.PERSON_ID)

            @staticmethod
            def mark_id(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.MARK_ID)

            @staticmethod
            def description(object: dict) -> str:
                result = PIH.RESULT.EXTRACT.parameter(
                    object, FIELD_NAME_COLLECTION.DESCRIPTION)
                if isinstance(result, Tuple) or isinstance(result, List):
                    return result[0]

            @staticmethod
            def container_dn(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.container_dn_from_dn(PIH.RESULT.EXTRACT.dn(user_object))

            @staticmethod
            def container_dn_from_dn(dn: str) -> str:
                return ",".join(dn.split(",")[1:])

        class FILTER:

            def users_by_dn(data: List[User], dn: str) -> List:
                return list(filter(lambda x: x.distinguishedName.find(dn) != -1, data))

        class PRINTER:

            @staticmethod
            def list() -> Result[List]:
                return DataTools.to_result(RPC_COMMANDS.AD.printer_list()) 

        class MARK:

            @staticmethod
            def by_tab_number(value: str) -> Result[Mark]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_mark_by_tab_number(value), Mark)

            @staticmethod
            def by_name(value: str) -> Result[List[Mark]]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_mark_by_person_name(value), Mark)

            @staticmethod
            def free_list() -> Result[Mark]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_free_marks(), Mark)

            @staticmethod
            def free_marks_by_group_id(value: int) -> Result[Mark]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_free_marks_by_group_id(value), Mark)

            @staticmethod
            def free_marks_group_statistics() -> Result[MarkGroupStatistics]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_free_marks_group_statistics(), MarkGroupStatistics)

            @staticmethod
            def all_persons() -> Result:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_all_persons())

        class USER:

            @staticmethod
            def by_login(value: str) -> Result[List[User]]:
                return DataTools.to_result(
                    RPC_COMMANDS.USER.get_user_by_login(value), User)

            @staticmethod
            def template_list() -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_template_list(), User)

            @staticmethod
            def containers() -> Result[List[UserContainer]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_containers(), UserContainer)

            @staticmethod
            def by_full_name(value: FullName) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_user_by_full_name(value), User)

            @staticmethod
            def by_name(value: str) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_users_by_name(value), User)

            @staticmethod
            def active_by_name(value: str) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_active_users_by_name(value), User)

            @staticmethod
            def all() -> Result[List[User]]:
                return PIH.RESULT.USER.by_name(CONST.AD.SEARCH_PATTERN_ALL)

            @staticmethod
            def all_active() -> Result[List[User]]:
                return PIH.RESULT.USER.active_by_name(CONST.AD.SEARCH_PATTERN_ALL)

            @staticmethod
            def by_tab_number(value: str) -> Result[User]:
                mark: Mark = PIH.RESULT.MARK.by_tab_number(value).data
                return Result(FIELD_COLLECTION.AD.MAIN, DataTools.if_check(mark, lambda: DataTools.get_first(PIH.RESULT.USER.by_full_name(FullNameTool.from_string(mark.FullName)).data)))

    class INPUT:

        @staticmethod
        def input(caption: str = None) -> str:
            try:
                return input() if caption is None else input(caption)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()

        @staticmethod
        def telephone(format: bool = True) -> str:
            while True:
                PR.input("Номер телефона")
                telehone = PIH.INPUT.input()
                check: bool = None
                if format:
                    telehone_fixed = PIH.FORMAT.telephone(telehone)
                    check = PIH.CHECK.telephone(telehone_fixed)
                    if check and telehone_fixed != telehone:
                        telehone = telehone_fixed
                        PR.notify("Телефон отформатирован")
                if check or PIH.CHECK.telephone(telehone):
                    return telehone
                else:
                    PR.red("Неверный формат номера телефона!")

        @staticmethod
        def email() -> str:
            while True:
                PR.input("Электронная почта")
                email = PIH.INPUT.input()
                if PIH.CHECK.email(email):
                    return email
                else:
                    PR.red("Неверный формат электронной почты!")

        @staticmethod
        def message() -> str:
            PR.input("Сообщение")
            return PIH.INPUT.input()       

        @staticmethod
        def description() -> str:
            PR.input("Введите описание")
            return PIH.INPUT.input()

        @staticmethod
        def login(check_on_exsits: bool = False):
            while True:
                PR.input("Введите логин")
                login = PIH.INPUT.input()
                if PIH.CHECK.login(login):
                    if check_on_exsits and PIH.CHECK.USER.is_exsits_by_login(login):
                        PR.red("Логин занят!")
                    else:
                        return login
                else:
                    PR.red("Неверный формат логина!")

        @staticmethod
        def indexed_list(caption: str, name_list: List[str], caption_list: List[str], by_index: bool = False) -> str:
            return PIH.INPUT.item_by_index(caption, name_list, lambda item, index: caption_list[index if by_index else item])

        @staticmethod
        def indexed_field_list(caption: str, list: FieldItemList) -> str:
            name_list = list.get_name_list()
            return PIH.INPUT.item_by_index(caption, name_list, lambda item, _: list.get_item_by_name(item).caption)

        @staticmethod
        def index(caption: str, data: dict, item_label: Callable = None) -> int:
            selected_index = -1
            length = len(data)
            while True:
                if item_label:
                    for index, item in enumerate(data):
                        PR.index(index + 1, item_label(item, index))
                if length == 1:
                    return 0
                selected_index = PIH.INPUT.input(PR.input_str(caption + f" (от 1 до {length})", "", ":"))
                if selected_index == "":
                    selected_index = 1
                try:
                    selected_index = int(selected_index) - 1
                    if selected_index >= 0 and selected_index < length:
                        return selected_index
                except ValueError:
                    continue

        @staticmethod
        def item_by_index(caption: str, data: List, item_label: Callable = None) -> dict:
            return data[PIH.INPUT.index(caption, data, item_label)]

        @staticmethod
        def tab_number(check: bool = True) -> str:
            tab_number: str = None
            while True:
                PR.input("Введите табельный номер:")
                tab_number = PIH.INPUT.input()
                if check:
                    if PIH.CHECK.tab_number(tab_number):
                        return tab_number
                    else:
                        PR.red("Wrong tab number")
                        return tab_number
                else:
                    return tab_number

        @staticmethod
        def password(secret: bool = True, check: bool = False, settings: PasswordSettings = None) -> str:
            PR.input("Введите новый пароль:")
            while True:
                value = getpass(" ") if secret else PIH.INPUT.input()
                if not check or PIH.CHECK.password(value, settings):
                    return value
                else:
                    PR.red("Пароль не соответствует требованием безопасности")

        @staticmethod
        def same_if_empty(caption: str, src_value: str) -> str:
            value = PIH.INPUT.input(caption)
            if value == "":
                value = src_value
            return value


        @staticmethod
        def name() -> str:
            return PIH.INPUT.input(PR.input("Введите часть имени:"))

        @staticmethod
        def full_name() -> FullName:
            def full_name_part(caption: str) -> str:
                while(True):
                    value: str = PIH.INPUT.input(PR.input(caption))
                    value = value.strip()
                    if PIH.CHECK.name(value):
                        return PIH.FORMAT.name(value)
                    else:
                        pass
            full_name: FullName = FullName()
            full_name.last_name = full_name_part("Введите фамилию")
            full_name.first_name = full_name_part("Введите имя")
            full_name.middle_name = full_name_part("Введите отчество")
            return full_name

        @staticmethod
        def yes_no(text: str = " ", enter_for_yes: bool = False) -> bool:
            answer = PIH.INPUT.input(f"{PR.blue_str(text)} \n{PR.green_str('Да (1 или Ввод)')} {PR.red_str('Нет (Остальное)')}:" if enter_for_yes else
                                     f"{PR.blue_str(text)} \n{PR.red_str('Да (1)')} {PR.green_str('Нет (Остальное или Ввод)')}:")
            answer = answer.lower()
            return answer == "y" or answer == "yes" or answer == "1" or (answer == "" and enter_for_yes)

        class USER:

            def container() -> UserContainer:
                result: Result = PIH.RESULT.USER.containers()
                data = result.data
                PIH.VISUAL.containers_for_result(result, True)
                return PIH.INPUT.item_by_index("Выберите контейнер пользователя, введя индекс", data)

            @staticmethod
            def template() -> dict:
                result = PIH.RESULT.USER.template_list()
                data = result.data
                PIH.VISUAL.template_users_for_result(result, True)
                return PIH.INPUT.item_by_index("Выберите шаблон пользователя, введя индекс", data)

            @staticmethod
            def search_attribute() -> str:
                return PIH.INPUT.indexed_field_list("Выберите по какому критерию искать, введя индекс",
                    FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE)

            @staticmethod
            def search_value(search_attribute: str) -> str:
                field_item = FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE.get_item_by_name(
                    search_attribute)
                return PIH.INPUT.input(PR.input(f"Введите {field_item.caption.lower()}:"))
            
        class MARK:

            @staticmethod
            def free(group: MarkGroup = None) -> Mark:
                while True:
                    if group is None:
                        if PIH.INPUT.yes_no("Выбор группы доступа для карты доступа по имени пользователя из этой группы?"):
                            result = PIH.RESULT.MARK.by_name(
                                PIH.INPUT.name())
                            mark_list: List[Mark] = result.data
                            length = len(mark_list)
                            if length > 0:
                                if length > 1:
                                    PIH.VISUAL.table_with_caption_first_title_is_centered(
                                        result, "Найденные пользователи:", True)
                                group = PIH.INPUT.item_by_index(
                                    "Выберите группу доступа", mark_list)
                            else:
                                PR.red("Пользователь с введенным именем не найден")
                        else:
                            result = PIH.RESULT.MARK.free_marks_group_statistics()
                            data = result.data
                            length = len(data)
                            if length > 0:
                                if length > 1:
                                    PIH.VISUAL.free_marks_group_statistics_for_result(
                                        result, True)
                                group = PIH.INPUT.item_by_index(
                                    "Выберите группу доступа введя индекс", data)
                            else:
                                PR.red("Свободный карт доступа нет!")
                                return None
                    if group is not None:
                        result = PIH.RESULT.MARK.free_marks_by_group_id(group.GroupID)
                        data = result.data
                        length = len(data)
                        if length > 0:
                            if length > 1:
                                PIH.VISUAL.free_marks_by_group_for_result(
                                    group, result, True)
                            return PIH.INPUT.item_by_index(
                                "Выберите карту доступа введя индекс", data)
                        else:
                            PR.red(
                                f"Нет свободных карт для группы доступа '{group.GroupName}'!")
                            return None
                    else:
                        pass

            @staticmethod
            def by_name() -> Mark:
                PR.head2("Введите имя персоны:")
                result = PIH.RESULT.MARK.by_name(PIH.INPUT.name())
                PIH.VISUAL.marks_for_result(result, "Карты доступа", True)
                return PIH.INPUT.item_by_index("Выберите карточку, введя индекс", result.data)


        @staticmethod
        def message_for_user_by_login(login: str) -> str:
            user = ResultUnpack.unpack_first_data(
                PIH.RESULT.USER.by_login(login))
            if user is not None:
                head_string = f"Здравствуйте, {PIH.RESULT.EXTRACT.name(user)}, "
                PR.green(head_string)
                message = PIH.INPUT.input(PR.blue_str("Enter message: "))
                return head_string + message
            else:
                pass

        @staticmethod
        def container_dn_or_template_user_container_dn() -> str:
            container_type = PIH.INPUT.indexed_field_list(
                "Choose type of container:", FIELD_COLLECTION.AD.CONTAINER_TYPE)
            if container_type == FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER:
                return PIH.RESULT.EXTRACT.container_dn(PIH.INPUT.template_user())
            else:
                return PIH.RESULT.EXTRACT.dn(PIH.INPUT.container())

    class CHECK:

        class USER:

            @staticmethod
            def is_exsits_by_login(value: str) -> bool:
                return RPC_COMMANDS.USER.user_is_exsits_by_login(value)

            @staticmethod
            def is_user(user: User) -> bool:
                 return PIH.CHECK.full_name(user.name)

            @staticmethod
            def is_exsits_by_full_name(full_name: FullName) -> bool:
                return ResultTools.data_is_empty(PIH.RESULT.USER.by_full_name(full_name))

            @staticmethod
            def search_attribute(value: str) -> bool:
                return value in CONST.AD.SEARCH_ATTRIBUTES

            @staticmethod
            def property(value: str) -> str:
                if value == "":
                    return USER_PROPERTY.USER_STATUS
                return value

        class MARK:

            @staticmethod
            def is_free(tab_number: str) -> bool:
                return RPC_COMMANDS.MARK.is_mark_free(tab_number)

            @staticmethod
            def is_exsits_by_full_name(full_name: FullName) -> bool:
                result: Result[List[Mark]] = PIH.RESULT.MARK.by_name(
                    FullNameTool.to_string(full_name))
                return ResultTools.data_is_empty(result)

       
        @staticmethod
        def tab_number(value: str) -> bool:
            return re.fullmatch(r"[0-9]+", value) is not None

        @staticmethod
        def login(value: str) -> bool:
            pattern = r"([a-z]{" + \
                str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}[0-9]*)"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def telephone(value: str) -> bool:
            return value is not None and re.fullmatch(r"^\+[0-9]{11,13}$", value) is not None

        @staticmethod
        def email(value: str) -> bool:
            return re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", value) is not None

        @staticmethod
        def name(value: str) -> bool:
            pattern = r"[а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def full_name(value: str) -> bool:
            pattern = r"[а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",} [а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) +",} [а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def password(value: str, settings: PasswordSettings = None) -> bool:
            settings = settings or PASSWORD.SETTINGS.DEFAULT
            return PasswordTools.check_password(value, settings.length, settings.special_characters)

        def ping(host: str) -> bool:
            command = ['ping', "-n", '1', host]
            response = subprocess.call(command)
            return response == 0

    @staticmethod
    def _log(message: str, channel: LogChannel = LogChannel.DEFAULT, level: Any = LogLevel.DEFAULT) -> Any:
        level_value: int = None
        level_list: List[LogLevel] = None
        if isinstance(level, LogLevel) :
            level_list = [level]
        if isinstance(level, int):
            level_value = level
        if level_value is None:
            level_value = 0
            for level_item in level_list:
                level_value = level_value | level_item.value
        return RPC_COMMANDS.LOG.log(message, channel, level_value)
        
    def _log_command(command: LogCommandName, parameters:Tuple = None) -> Any:
        command_list: dict = LogCommandName._value2member_map_
        log_commnad: LogCommand = command_list[command.name.lower()]
        parameter_pattern_list: List = LOG_COMMAND_LIST[log_commnad].params
        parameter_dict: dict = {}
        index: int = 0
        if len(parameter_pattern_list) > len(parameters):
            raise Exception("Income parameter list length is less that parameter list length of command") 
        for parameter_pattern_item in parameter_pattern_list:
            parameter_pattern: ParamItem = parameter_pattern_item
            parameter_dict[parameter_pattern.name] = parameters[index]
            index += 1
        return RPC_COMMANDS.LOG.command(command.name, parameter_dict)

    class LOG_COMMAND:


        @staticmethod
        def login() -> Any:
            return PIH._log_command(LogCommandName.LOG_IN, (PIH.OS.get_login(), PIH.OS.get_computer_name()))


        @staticmethod
        def printer_report(printer_name: str, location: str) -> Any:
            return PIH._log_command(LogCommandName.PRINTER_REPORT, (printer_name, location))

    class LOG:

        @staticmethod
        def debug(message: str, level: Any = LogLevel.DEFAULT) -> Any:
            return PIH._log(message, LogChannel.DEBUG, level)

        @staticmethod
        def backup(message: str, level: Any = LogLevel.DEFAULT) -> Any:
            return PIH._log(message, LogChannel.BACKUP, level)

        @staticmethod
        def notification(message: str, level: Any = LogLevel.DEFAULT) -> Any:
            return PIH._log(message, LogChannel.NOTIFICATION, level)

        @staticmethod
        def printer(message: str, level: Any = LogLevel.DEFAULT) -> Any:
            return PIH._log(message, LogChannel.PRINTER, level)

    class LOG_COMMAND:

        @staticmethod
        def loggin() -> Any:
            return PIH._log_command(LogCommandName.LOG_IN, (PIH.OS.get_login(), PIH.OS.get_computer_name()))

        @staticmethod
        def printer_report(name: str, location: str, report: str) -> Any:
            return PIH._log_command(LogCommandName.PRINTER_REPORT, (name, location, report))


    class VISUAL:

        @staticmethod
        def init() -> None:
            PR.init()

        @staticmethod
        def facade_header() -> None:
            PR.cyan(
                "█▀█ ▄▀█ █▀▀ █ █▀▀ █ █▀▀   █ █▄░█ ▀█▀ █▀▀ █▀█ █▄░█ ▄▀█ ▀█▀ █ █▀█ █▄░█ ▄▀█ █░░   █░█ █▀█ █▀ █▀█ █ ▀█▀ ▄▀█ █░░")
            PR.cyan(
                "█▀▀ █▀█ █▄▄ █ █▀░ █ █▄▄   █ █░▀█ ░█░ ██▄ █▀▄ █░▀█ █▀█ ░█░ █ █▄█ █░▀█ █▀█ █▄▄   █▀█ █▄█ ▄█ █▀▀ █ ░█░ █▀█ █▄▄")
            print(f"Version: {PIH.version}")

        @staticmethod
        def rpc_server_header(server_host: str, server_name: str) -> None:
            PR.blue("PIH")
            PR.blue(f"Version: {PIH.version}")
            PR.green(f"Server host: {server_host}")
            PR.green(f"Server name: {server_name}")

        @staticmethod
        def free_marks(use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                PIH.RESULT.MARK.free_list(), "Free marks:", use_index)

        @staticmethod
        def mark_by_tab_number(value: str) -> None:
            PIH.VISUAL.marks_for_result(
                PIH.RESULT.MARK.by_tab_number(value), "Mark by tab number:")

        @staticmethod
        def marks_for_result(result: Result, caption: str, use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                result, caption, use_index)

        @staticmethod
        def free_marks_group_statistics(use_index: bool = False) -> None:
            PIH.VISUAL.free_marks_group_statistics_for_result(
                PIH.RESULT.MARK.free_marks_group_statistics(), use_index)

        @staticmethod
        def free_marks_by_group(group: dict, use_index: bool = False) -> None:
            PIH.VISUAL.free_marks_by_group_for_result(
                PIH.RESULT.MARK.free_marks_by_group_id(group), group, use_index)

        @staticmethod
        def free_marks_group_statistics_for_result(result: Result, use_index: bool) -> None:
            PIH.VISUAL.table_with_caption_last_title_is_centered(
                result, "Свободные карты доступа:", use_index)

        @staticmethod
        def free_marks_by_group_for_result(group: MarkGroup, result: Result, use_index: bool) -> None:
            group_name = group.GroupName
            PIH.VISUAL.table_with_caption_last_title_is_centered(
                result, f"Свободные карты доступа для группы доступа '{group_name}':", use_index)

        @staticmethod
        def containers_for_result(result: Result, use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption(result, "Подразделение:", use_index)

        @staticmethod
        def table_with_caption_first_title_is_centered(result: Result, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[int(use_index)]] = "c"
            PIH.VISUAL.table_with_caption(
                result, caption, use_index, modify_table, modify_data_handler)

        @staticmethod
        def table_with_caption_last_title_is_centered(result: Result, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[-1]] = "c"
            PIH.VISUAL.table_with_caption(
                result, caption, use_index, modify_table, modify_data_handler)

        @staticmethod
        def table_with_caption(result: Any, caption: str = None, use_index: bool = False, modify_table_handler: Callable = None, modify_data_handler: Callable = None) -> None:
            if caption is not None:
                PR.cyan(caption)
            is_result_type = isinstance(result, Result)
            field_list = result.fields if is_result_type else result["fields"]
            data = result.data if is_result_type else result["data"]
            if DataTools.is_empty(data):
                PR.red("Not found!")
            else:
                if not isinstance(data, list):
                    data = [data]
                if use_index:
                    field_list.list.insert(0, FIELD_COLLECTION.INDEX)
                caption_list: List = field_list.get_caption_list()
                def create_table(caption_list: List[str]) -> PrettyTable:
                    table: PrettyTable = PrettyTable(caption_list)
                    table.align = "l"
                    if use_index:
                        table.align[caption_list[0]] = "c"
                    return table
                table: PrettyTable = create_table(caption_list)
                if modify_table_handler is not None:
                    modify_table_handler(table, caption_list)
                for index, item in enumerate(data):
                    row_data: List = []
                    for field_item_obj in field_list.get_list():
                        field_item: FieldItem = field_item_obj
                        if field_item.visible:
                            if field_item.name == FIELD_COLLECTION.INDEX.name:
                                row_data.append(str(index + 1))
                            elif not isinstance(item, dict):
                                item_data = getattr(item, field_item.name)
                                if modify_data_handler is not None:
                                    modify_item_data = modify_data_handler(
                                        field_item, item)
                                    row_data.append(DataTools.if_check(
                                        item_data, lambda: item_data, "") if modify_item_data is None else modify_item_data)
                                else:
                                    row_data.append(DataTools.if_check(item_data, lambda: item_data, ""))
                            elif field_item.name in item:
                                item_data = item[field_item.name]
                                if modify_data_handler is not None:
                                    modify_item_data = modify_data_handler(
                                        field_item, item)
                                    row_data.append(
                                        item_data if modify_item_data is None else modify_item_data)
                                else:
                                    row_data.append(item_data)
                    table.add_row(row_data)
                print(table)
                table.clear()

        @staticmethod
        def template_users_for_result(data: dict, use_index: bool = False) -> None:
            def data_handler(field_item: FieldItem, item: User) -> Any:
                filed_name = field_item.name
                if filed_name == FIELD_NAME_COLLECTION.DESCRIPTION:
                    return DataTools.get_first(item.description)
                return None
            PIH.VISUAL.table_with_caption(
                data, "Шаблоны для создания аккаунта пользователя:", use_index, None, data_handler)

    class ACTION:

        class PRINTER:

            @staticmethod
            def report() -> bool:
                return RPC_COMMANDS.PRINTER.report()

        class USER:

            @staticmethod
            def create_from_template(container_dn: str,
                                          full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return RPC_COMMANDS.USER.create_from_template(
                    container_dn, full_name, login, password, description, telephone, email)

            @staticmethod
            def create_in_container(container_dn: str,
                                         full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return RPC_COMMANDS.USER.create_in_container(
                    container_dn, full_name, login, password, description, telephone, email)

            @staticmethod
            def set_telephone(user: User, telephone: str) -> bool:
                return RPC_COMMANDS.USER.set_telephone(user.distinguishedName, telephone)

            @staticmethod
            def set_password(user: User, password: str) -> bool:
                return RPC_COMMANDS.USER.set_password(user.distinguishedName, password)

            @staticmethod
            def set_status(user: User, status: str, container: UserContainer) -> bool:
                return RPC_COMMANDS.USER.set_status(user.distinguishedName, status, DataTools.if_check(container, lambda: container.distinguishedName))


        class MARK:

            @staticmethod
            def create(full_name: FullName, tab_number: str, telephone: str = None) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.create(full_name, tab_number, telephone))

            @staticmethod
            def set_full_name_by_tab_number(full_name: FullName, tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.set_full_name_by_tab_number(full_name, tab_number))

            @staticmethod
            def set_telephone_by_tab_number(telephone: str, tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.set_telephone_by_tab_number(telephone, tab_number))

            @staticmethod
            def make_as_free_by_tab_number(tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.make_mark_as_free_by_tab_number(tab_number))

            @staticmethod
            def remove(mark: Mark) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.remove_by_tab_number(mark.TabNumber))

        def create_user_document(path: str, full_name: FullName, tab_number: str, pc: LoginPasswordPair, polibase: LoginPasswordPair, email: LoginPasswordPair) -> bool:
            locale.setlocale(locale.LC_ALL, 'ru_RU')
            date_now = datetime.now().date()
            date_now_string = f"{date_now.day} {calendar.month_name[date_now.month]} {date_now.year}"
            return RPC_COMMANDS.TEMPLATE.create_user_document(path, date_now_string, CONST.SITE, CONST.SITE_PROTOCOL + CONST.SITE, CONST.EMAIL_ADDRESS, full_name, tab_number, pc, polibase, email)

        def generate_login(full_name: FullName) -> str:
            login: FullName = NamePolicy.convert_to_login(full_name)
            login_string: str = FullNameTool.to_string(login, "")
            if PIH.CHECK.USER.is_exsits_by_login(login_string):
                PR.red(f"Login '{login_string}' is not free")
                login_alt = NamePolicy.convert_to_alternative_login(
                    login)
                login_string = FullNameTool.to_string(login_alt, "")
                if PIH.CHECK.USER.is_exsits_by_login(login_string):
                    PR.red(f"Login '{login_string}' is not free")
                    login_reversed = NamePolicy.convert_to_reverse_login(login)
                    login_string = FullNameTool.to_string(login_reversed, "")
                    if PIH.CHECK.USER.is_exsits_by_login(login_string):
                        PR.red(f"Login '{login_string}' is not free")
                        while True:
                            login_string = PIH.INPUT.login()
                            if PIH.CHECK.USER.is_exsits_by_login(login_string):
                                PR.red(f"Login '{login_string}' is not free")
                            else:
                                break
            return login_string

        @staticmethod
        def generate_password(once: bool = False, settings: PasswordSettings = PASSWORD.SETTINGS.DEFAULT) -> str:
            def generate_password_interanal(settings: PasswordSettings = None) -> str:
                return PasswordTools.generate_random_password(settings.length, settings.special_characters,
                                                              settings.order_list, settings.special_characters_count,
                                                              settings.alphabets_lowercase_count, settings.alphabets_uppercase_count,
                                                              settings.digits_count, settings.shuffled)
            while True:
                password = generate_password_interanal(settings)
                if not once:
                    PR.value("Пароль",  password)
                if once or PIH.INPUT.yes_no("Использовать пароль?", True):
                    return password
                else:
                    pass

        @staticmethod
        def generate_email(login: str) -> str:
            return "@".join((login, CONST.SITE))

        @staticmethod
        def generate_user_principal_name(login: str) -> str:
            return "@".join((login, CONST.AD.DOMAIN_MAIN))


class PR:

    TEXT_AFTER: str = ""
    TEXT_BEFORE: str = ""

    @staticmethod
    def init() -> None:
        colorama.init()

    @staticmethod
    def clear_screen() -> None:
        ansi.clear_screen(2)

    @staticmethod
    def color_str(color: int, string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        string = f" {string} "
        return f"{before_text}{color}{string}{Back.RESET}{after_text}"

    @staticmethod
    def color(color: int, string: str, before_text: str = TEXT_BEFORE, after_text: str = " ") -> None:
        PR.write_line(PR.color_str(color, string, before_text, after_text))

    @staticmethod
    def write_line(string: str) -> None:
        print(string)

    @staticmethod
    def index(index: int, string: str) -> None:
        print(f"{index}. {string}")

    @staticmethod
    def input(caption: str) -> None:
        PR.write_line(PR.input_str(caption))

    @staticmethod
    def input_str(caption: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return f"{Fore.BLACK}{PR.color_str(Back.WHITE, caption, before_text, after_text)}{Fore.RESET}"

    @staticmethod
    def value(caption: str, value: str) -> None:
        PR.cyan(caption, "", f" {value}")

    @staticmethod
    def get_action_value(caption: str, value: str, show: bool = True) -> ActionValue:
        if show:
            PR.value(caption, value)
        return ActionValue(caption, value)

    @staticmethod
    def head(caption: str) -> None:
        PR.cyan(caption)
    
    @staticmethod
    def head1(caption: str) -> None:
        PR.magenta(caption)

    @staticmethod
    def head2(caption: str) -> None:
        PR.nl()
        PR.yellow(caption)

    @staticmethod
    def nl() -> None:
        print()

    @staticmethod
    def alert_str(caption: str) -> str:
        return PR.red_str(caption)

    @staticmethod
    def alert(caption: str) -> str:
        PR.write_line(PR.alert_str(caption))

    @staticmethod
    def notify_str(caption: str) -> str:
        return PR.yellow_str(caption)

    @staticmethod
    def notify(caption: str) -> str:
        PR.write_line(PR.notify_str(caption))

    @staticmethod
    def good_str(caption: str) -> str:
        return PR.green_str(caption)

    @staticmethod
    def good(caption: str) -> str:
        PR.write_line(PR.good_str(caption))

    @staticmethod
    def green_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.GREEN, string, before_text, after_text)

    @staticmethod
    def green(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.green_str(string, before_text, after_text))

    @staticmethod
    def yellow_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.YELLOW, string, before_text, after_text)

    @staticmethod
    def yellow(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.yellow_str(string, before_text, after_text))

    @staticmethod
    def black_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.BLACK, string, before_text, after_text)

    @staticmethod
    def black(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.black_str(string, before_text, after_text))

    @staticmethod
    def white_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.WHITE, string, before_text, after_text)

    @staticmethod
    def white(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.white_str(string, before_text, after_text))

    @staticmethod
    def magenta_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.MAGENTA, string, before_text, after_text)

    @staticmethod
    def magenta(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.magenta_str(string, before_text, after_text))

    @staticmethod
    def cyan(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.cyan_str(string, before_text, after_text))

    @staticmethod
    def cyan_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.CYAN, string, before_text, after_text)

    @staticmethod
    def red(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.red_str(string, before_text, after_text))

    @staticmethod
    def red_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.RED, string, before_text, after_text)

    @staticmethod
    def blue(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.blue_str(string, before_text, after_text))

    @staticmethod
    def blue_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.BLUE, string, before_text, after_text)

    @staticmethod
    def bright(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.bright_str(string, before_text, after_text))

    @staticmethod
    def bright_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Style.BRIGHT, string, before_text, after_text)


class ActionStack(List):
    
    def __init__(self, *argv):
        self.acion_value_list: List[ActionValue] = []
        for arg in argv:
            self.append(arg)
        self.start()

    def call_actions_by_index(self, index: int = 0, change: bool = False):
        previous_change: bool = False
        while True:
            try:
                action_value: ActionValue = self[index]()
                if action_value:
                    if change or previous_change:
                        previous_change = False
                        if index in self.acion_value_list:
                            self.acion_value_list[index] = action_value
                        else:
                            self.acion_value_list.append(action_value)
                    else:
                        self.acion_value_list.append(action_value)
                index = index + 1
                if index == len(self) or change:
                    break
            except KeyboardInterrupt:
                PR.red("Повтор предыдущих действия")
                if index > 0:
                    previous_change = True
                    #self.show_action_values()
                    #index = index - 1
                else:
                    continue

    def show_action_values(self) -> None:
        def label(item: ActionValue):
            return item.caption
        self.call_actions_by_index(PIH.INPUT.index(
            "Выберите свойство для изменения, введя индекс", self.acion_value_list, label), True)
        

    def start(self):
        self.call_actions_by_index()
        while True:
            PR.head2("Данные пользователя")
            for action_value in self.acion_value_list:
                PR.value(action_value.caption, action_value.value)
            if PIH.INPUT.yes_no("Данные верны?", True):
                break
            else:
               self.show_action_values()
