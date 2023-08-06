from enum import *
import os
from typing import List

from pih.collection import FieldItem, FieldItemList, LogCommand, ParamItem, PasswordSettings


class DATA_EXTRACTOR:

    USER_NAME_FULL: str = "user_name_full"
    USER_NAME: str = "user_name"
    AS_IS: str = "as_is"


class USER_PROPERTY:

    TELEPHONE: str = "telephoneNumber"
    EMAIL: str = "mail"
    DN: str = "distinguishedName"
    USER_ACCOUNT_CONTROL: str = "userAccountControl"
    LOGIN: str = "samAccountName"
    DESCRIPTION: str = "description"
    PASSWORD: str = "password"
    USER_STATUS: str = "userStatus"
    NAME: str = "name"


class SCHEDULER_TEVENT_TYPE:
    MINUTE: int = 5
    HOUR: int = 5


class CONST:

    SITE: str = "pacifichosp.com"
    MAIL_PREFIX: str = "mail"
    SITE_PROTOCOL: str = "https://"
    EMAIL_ADDRESS: str = f"{MAIL_PREFIX}.{SITE}"

    class FILE:

        class EXTENSION:

            EXCEL: str = "xlsx"

    class AD:

        SEARCH_ATTRIBUTES: List[str] = [
            USER_PROPERTY.LOGIN, USER_PROPERTY.NAME]
        SEARCH_ATTRIBUTES_DEFAULT: str = SEARCH_ATTRIBUTES[0]
        DOMAIN_NAME: str = "fmv"
        DOMAIN_ALIAS: str = "pih"
        DOMAIN: str = f"{DOMAIN_NAME}.lan"
        DOMAIN_MAIN: str = DOMAIN
        USER_HOME_FOLDER_DISK: str = "U:"
        DN_ACTIVE_CONTAINER_DN: str = f"OU=Users,OU=Unit,DC={DOMAIN_NAME},DC=lan"
        DN_INACTIVE_CONTAINER_DN: str = f"OU=deadUsers,OU=Unit,DC={DOMAIN_NAME},DC=lan"
        PATH_ROOT: str = f"\\\{DOMAIN_MAIN}"
        SEARCH_PATTERN_ALL: str = "*"
        JOB_POSITIONS_CONTAINER_DN: str = "OU=Job positions,OU=Groups,OU=Unit,DC=fmv,DC=lan"

        class JobPositions(Enum):
            HR:str = auto()


    class NAME_POLICY:

        PARTS_LIST_MIN_LENGTH: int = 3
        PART_ITEM_MIN_LENGTH: int = 3

    class RPC:

        PING_COMMAND: str = "__ping__"
        EVENT_COMMAND: str = "__event__"
        SUBSCRIBE_COMMAND: str = "__subscribe__"

        @staticmethod
        def PORT(add: int = 0) -> int:
            return 50051 + add

    class HOST:

        class PRINTER_SERVER:

            @staticmethod
            def NAME() -> str:
                return "fmvdc1.fmv.lan"

        class PRINTER:

            @staticmethod
            def NAME() -> str:
                return "fmvdc2.fmv.lan"

        class ORION:

            @staticmethod
            def NAME() -> str:
                return "orion"

        class AD:

            @staticmethod
            def NAME() -> str:
                return "fmvdc2.fmv.lan"

        class DOCS:

            @staticmethod
            def NAME() -> str:
                return "fmvdc2.fmv.lan"

        class SCHEDULER:

            @staticmethod
            def NAME() -> str:
                return "ws-735"

        class BACKUP_WORKER:

            @staticmethod
            def NAME() -> str:
                return "backup_worker"

        class LOG:

            @staticmethod
            def NAME() -> str:
                return "worker"


class PATH_SHARE:

    NAME: str = "shares"
    PATH: str = os.path.join(CONST.AD.PATH_ROOT, NAME)


class PATH_IT:

    NAME: str = "5. IT"
    NEW_EMPLOYEES_NAME: str = "New employees"
    ROOT: str = os.path.join(PATH_SHARE.PATH, NAME)

    @staticmethod
    def NEW_EMPLOYEE(name: str) -> str:
        return os.path.join(os.path.join(PATH_IT.ROOT, PATH_IT.NEW_EMPLOYEES_NAME), name)


class PATH_USER:

    NAME: str = "homes"
    HOME_FOLDER: str = os.path.join(CONST.AD.PATH_ROOT, NAME)
    HOME_FOLDER_FULL: str = os.path.join(CONST.AD.PATH_ROOT, NAME)

    @staticmethod
    def document(name: str, login: str = None) -> str:
        return PATH_IT.NEW_EMPLOYEE(name) + (f" ({login})" if login else "") + ".docx"


class PATHS:

    SHARE: PATH_SHARE = PATH_SHARE()
    IT: PATH_IT = PATH_IT()
    USER: PATH_USER = PATH_USER()


class FIELD_NAME_COLLECTION:

    FULL_NAME: str = "FullName"
    GROUP_NAME: str = "GroupName"
    GROUP_ID: str = "GroupID"
    COMMENT: str = "Comment"
    TAB_NUMBER: str = "TabNumber"
    NAME: str = USER_PROPERTY.NAME
    PERSON_ID: str = "pID"
    MARK_ID: str = "mID"

    PORT_NAME: str = "portName"

    SEARCH_ATTRIBUTE_LOGIN: str = "samAccountName"
    SEARCH_ATTRIBUTE_NAME: str = USER_PROPERTY.NAME

    TELEPHONE: str = USER_PROPERTY.TELEPHONE
    EMAIL: str = USER_PROPERTY.EMAIL
    DN: str = USER_PROPERTY.DN
    LOGIN: str = USER_PROPERTY.LOGIN
    DESCRIPTION: str = USER_PROPERTY.DESCRIPTION
    PASSWORD: str = USER_PROPERTY.PASSWORD

    TEMPLATE_USER_CONTAINER: str = "templated_user"
    CONTAINER: str = "container"

    REMOVE: str = "remove"
    AS_FREE: str = "as_free"
    CANCEL: str = "cancel"


class FIELD_COLLECTION:

    INDEX: FieldItem = FieldItem("__Index__", "Index", True)

    class ORION:

        MARK_ACTION: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.REMOVE, "Удалить"),
            FieldItem(FIELD_NAME_COLLECTION.AS_FREE, "Сделать свободной"),
            FieldItem(FIELD_NAME_COLLECTION.CANCEL, "Оставить")
        )

        GROUP_BASE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.GROUP_NAME, "Access Name"),
            FieldItem(FIELD_NAME_COLLECTION.COMMENT, "Description")
        )

        TAB_NUMBER_BASE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.TAB_NUMBER, "Tab Number"),
            GROUP_BASE)

        TAB_NUMBER: FieldItemList = FieldItemList(
            TAB_NUMBER_BASE,
            FieldItem(FIELD_NAME_COLLECTION.TELEPHONE,
                      "Telephone", True),
            FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "Full name")
        ).position(FIELD_NAME_COLLECTION.FULL_NAME, 1).position(FIELD_NAME_COLLECTION.TELEPHONE, 2)

        NAME: FieldItemList = FieldItemList(
            TAB_NUMBER,
            FieldItem(FIELD_NAME_COLLECTION.PERSON_ID, "Person ID", False),
            FieldItem(FIELD_NAME_COLLECTION.MARK_ID, "Mark ID", False)
        ).visible(FIELD_NAME_COLLECTION.COMMENT, True)

        GROUP: FieldItemList = FieldItemList(
            GROUP_BASE,
            FieldItem(FIELD_NAME_COLLECTION.GROUP_ID, "Group id", False)
        )

        GROUP_STATISTICS: FieldItemList = FieldItemList(
            GROUP,
            FieldItem("Count", "Count"),
        ).visible(FIELD_NAME_COLLECTION.COMMENT, False)

        TIME_TRACKING: FieldItemList = FieldItemList(FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "Full name"),
                                                     FieldItem(
                                                         FIELD_NAME_COLLECTION.TAB_NUMBER, "Tab Number"),
                                                     FieldItem(
                                                         "TimeVal", "Time"),
                                                     FieldItem(
                                                         "Remark", "Remark"),
                                                     FieldItem(
                                                         "Mode", "Mode"))

        TIME_TRACKING_RESULT: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.TAB_NUMBER, "Tab Number"),
            FieldItem(FIELD_NAME_COLLECTION.FULL_NAME, "Full name"),
            FieldItem(
                "EnterTime", "Enter time"),
            FieldItem(
                "ExitTime", "Exit time"),
            FieldItem(
                "Duration", "Duration"))

    class AD:

        SEARCH_ATTRIBUTE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_LOGIN, "Логин"),
            FieldItem(FIELD_NAME_COLLECTION.SEARCH_ATTRIBUTE_NAME, "Имя")
        )

        CONTAINER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Name"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Description")
        )

        TEMPLATED_USER: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Description"))

        MAIN: FieldItemList = FieldItemList(CONTAINER,
                                            FieldItem(
                                                FIELD_NAME_COLLECTION.LOGIN, "Login"),
                                            FieldItem(
                                                FIELD_NAME_COLLECTION.TELEPHONE, "Telephone"),
                                            FieldItem(
                                                FIELD_NAME_COLLECTION.EMAIL, "Email"),
                                            FieldItem(
                                                FIELD_NAME_COLLECTION.DN, "Location"),
                                            FieldItem("userAccountControl", "Account Control")).position(FIELD_NAME_COLLECTION.DESCRIPTION, 4)

        CONTAINER_TYPE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER,
                      "By templated user container"),
            FieldItem(FIELD_NAME_COLLECTION.CONTAINER, "By container"))

    class POLICY:

        PASSWORD_TYPE: FieldItemList = FieldItemList(
            FieldItem("PC", "PC"),
            FieldItem("EMAIL", "Email"),
            FieldItem("SIMPLE", "Simple"),
            FieldItem("STRONG", "Strong"))

    class PRINTER:

        MAIN: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Name"),
            FieldItem("serverName", "Server name"),
            FieldItem("portName", "Host name"),
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Description"),
            FieldItem("adminDescription", "Admin description", False),
            FieldItem("driverName", "Driver name")
        )


class FIELD_COLLECTION_ALIAS(Enum):
    TIME_TRACKING: str = FIELD_COLLECTION.ORION.TIME_TRACKING


LINK_EXT = "lnk"


class PrinterCommand(Enum):
    REPORT: str = "report"
    STATUS: str = "status"


class PASSWORD_GENERATION_ORDER:

    SPECIAL_CHARACTER: str = "s"
    LOWERCASE_ALPHABET: str = "a"
    UPPERCASE_ALPHABET: str = "A"
    DIGIT: str = "d"
    DEFAULT_ORDER_LIST: List[str] = [SPECIAL_CHARACTER,
                                     LOWERCASE_ALPHABET, UPPERCASE_ALPHABET, DIGIT]


class PASSWORD:

    class SETTINGS:

        SIMPLE: PasswordSettings = PasswordSettings(
            3, "", PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 0, 3, 0, 0, False)
        NORMAL: PasswordSettings = PasswordSettings(
            8, "!@#", PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 3, 3, 1, 1, False)
        STRONG: PasswordSettings = PasswordSettings(
            10, "#%+\-!=@()_",  PASSWORD_GENERATION_ORDER.DEFAULT_ORDER_LIST, 3, 3, 2, 2, True)
        DEFAULT: PasswordSettings = NORMAL
        PC: PasswordSettings = NORMAL
        EMAIL: PasswordSettings = NORMAL

    def get(name: str) -> SETTINGS:
        return PASSWORD.__getattribute__(PASSWORD.SETTINGS, name)


class LogType(Enum):
    MESSAGE: str = "message"
    COMMAND: str = "command"
    DEFAULT: str = MESSAGE

# TODO: use auto() - no values!
class LogChannel(Enum):
    BACKUP: str = auto()
    NOTIFICATION: str = auto()
    DEBUG: str = auto()
    PRINTER: str = auto()
    SYSTEM: str = auto()
    HR: str = auto()
    DEFAULT: str = NOTIFICATION


class LogLevel(Enum):
    NORMAL: int = 1
    ERROR: int = 2
    EVENT: int = 4
    DEBUG: str = 8
    DEFAULT: str = NORMAL


class LogCommands(Enum):
    DEBUG: LogCommand = LogCommand(
        "It is a debug command", LogChannel.NOTIFICATION, LogLevel.DEBUG.value)
    PRINTER_REPORT: LogCommand = LogCommand("Принтер {printer_name} ({location}):\n {printer_report}", LogChannel.PRINTER, LogLevel.NORMAL.value, (ParamItem(
        "printer_name", "Name of printer"), ParamItem("location", "Location"), ParamItem("printer_report", "Printer report"))),
    #
    LOG_IN: LogCommand = LogCommand(
        "Пользователь {name} вошел с компьютера {computer_name}", LogChannel.SYSTEM, LogLevel.NORMAL.value, (ParamItem("name", "Name of user"), ParamItem("computer_name", "Name of computer"))),
    #
    POLIBASE_DB_BACKUP_START: str = LogCommand(
        "Start Polibase DataBase Dump backup",  LogChannel.BACKUP, LogLevel.NORMAL.value)
    POLIBASE_DB_BACKUP_COMPLETE: str = LogCommand(
        "Complete Polibase DataBase Dump backup",  LogChannel.BACKUP, LogLevel.NORMAL.value)
    #
    HR_NOTIFY_ABOUT_NEW_EMPLOYEE: str = LogCommand("День добрый, {hr_given_name}.\nДокументы для нового сотрудника: {employee_full_name} готовы!\nЕго корпоративная почта: {employee_email}.", LogChannel.HR, LogLevel.NORMAL.value, (ParamItem(
        "hr_given_name", "Имя руководителя отдела HR"), ParamItem("employee_full_name", "ФИО нового сотрудника"), ParamItem("employee_email", "Корпаротивная почта нового сотрудника"))),
