import enum
from os import path
import os
import sys
from typing import List

from pih.collection import CommandLinkItem, CommandChainItem, FieldItem, FieldItemList, CommandItem, LogCommand, ParamItem, PasswordSettings

class DATA_EXTRACTOR:

    USER_NAME_FULL: str = "user_name_full"
    USER_NAME: str = "user_name"
    AS_IS: str = "as_is"


class USER_PROPERTY:

    TELEPHONE: str = "telephoneNumber"
    DN: str = "distinguishedName"
    USER_ACCOUNT_CONTROL: str = "userAccountControl"
    LOGIN: str = "samAccountName"
    DESCRIPTION: str = "description"
    PASSWORD: str = "password"
    USER_STATUS: str = "userStatus"
    NAME: str = "name"



class CONST:

    SITE: str = "pacifichosp.com"
    MAIL_PREFIX: str = "mail"
    SITE_PROTOCOL: str = "https://"
    EMAIL_ADDRESS: str = f"{MAIL_PREFIX}.{SITE}"

    class AD:

        SEARCH_ATTRIBUTES: List[str] = [USER_PROPERTY.LOGIN, USER_PROPERTY.NAME]
        SEARCH_ATTRIBUTES_DEFAULT: str = SEARCH_ATTRIBUTES[0]
        DOMAIN_NAME: str = "fmv"
        DOMAIN_ALIAS: str = "pih"
        DOMAIN: str = f"{DOMAIN_NAME}.lan"
        DOMAIN_MAIN: str = DOMAIN
        USER_HOME_FOLDER_DISK: str = "U:"
        DN_ACTIVE_UNIT: str = f"OU=Users,OU=Unit,DC={DOMAIN_NAME},DC=lan"
        DN_INACTIVE_UNIT: str = f"OU=deadUsers,OU=Unit,DC={DOMAIN_NAME},DC=lan"
        PATH_ROOT: str = f"\\\{DOMAIN_MAIN}"
        SEARCH_PATTERN_ALL: str = "*"

    class NAME_POLICY:
    
        PARTS_LIST_MIN_LENGTH: int = 3
        PART_ITEM_MIN_LENGTH: int = 3

    class RPC:

        PING_COMMAND: str = "ping"

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

        class TEMPLATE:
    
            @staticmethod
            def NAME() -> str:
                return "fmvdc2.fmv.lan"

        class BACKUP_WORKER:

            @staticmethod
            def NAME() -> str:
                return "backup_worker"

        class LOG:
    
            @staticmethod
            def NAME() -> str:
                return "worker"
    
    class FACADE:
        
        COMMAND_SUFFIX: str = "Core"
        PATH: str = "//pih/facade/" 


class PATH_SHARE:

    NAME: str = "shares"
    PATH: str = os.path.join(CONST.AD.PATH_ROOT, NAME)


class PATH_IT:

    NAME: str = "5. IT"
    NEW_EMPLOYERS_NAME: str = "New employers"
    ROOT: str = os.path.join(PATH_SHARE.PATH, NAME)

    @staticmethod
    def NEW_EMPLOYER(name: str) -> str:
        return os.path.join(os.path.join(PATH_IT.ROOT, PATH_IT.NEW_EMPLOYERS_NAME), name)


class PATH_USER:
    
    NAME: str = "homes"
    HOME_FOLDER: str = os.path.join(CONST.AD.PATH_ROOT, NAME)
    HOME_FOLDER_FULL: str = os.path.join(CONST.AD.PATH_ROOT, NAME)

    @staticmethod
    def document(name: str, login: str = None) -> str:
        return PATH_IT.NEW_EMPLOYER(name) + (f" ({login})" if login else "") + ".docx"

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
    DN: str = USER_PROPERTY.DN
    LOGIN: str = USER_PROPERTY.LOGIN
    DESCRIPTION: str = USER_PROPERTY.DESCRIPTION
    PASSWORD: str = USER_PROPERTY.PASSWORD

    TEMPLATE_USER_CONTAINER: str ="templated_user"
    CONTAINER: str = "container"

    REMOVE: str = "remove"
    AS_FREE: str = "as_free"
    CANCEL: str = "cancel"



class FIELD_COLLECTION:

    INDEX: FieldItem = FieldItem("__Index__", "Index", True)

    class ORION:

        OLD_MARK_ACTION: FieldItemList = FieldItemList(
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
                                                FIELD_NAME_COLLECTION.DN, "Location"),
                                            FieldItem("userAccountControl", "Account Control")).position(FIELD_NAME_COLLECTION.DESCRIPTION, 4)

        CONTAINER_TYPE: FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER, "By templated user container"),
            FieldItem(FIELD_NAME_COLLECTION.CONTAINER, "By container"))

    class POLICY:

        PASSWORD_TYPE: FieldItemList = FieldItemList(
            FieldItem("PC", "PC"),
            FieldItem("EMAIL", "Email"),
            FieldItem("SIMPLE", "Simple"),
            FieldItem("STRONG", "Strong"))

    class PRINTER:

        MAIN:FieldItemList = FieldItemList(
            FieldItem(FIELD_NAME_COLLECTION.NAME, "Name"),
            FieldItem("serverName", "Server name"), 
            FieldItem("portName", "Host name"), 
            FieldItem(FIELD_NAME_COLLECTION.DESCRIPTION, "Description"),
            FieldItem("adminDescription", "Admin Description"),
            FieldItem("driverName", "Driver name")
            )

LINK_EXT = "lnk"


class PrinterCommand(enum.Enum):
    REPORT: str = "report"
    PING: str = "ping"


class EXECUTOR:

    PYTHON_EXECUTOR: str = "python"
    POWERSHELL_EXECUTOR: str = "powershell"
    VBS_EXECUTOR: str = "cscript"
    DEFAULT_EXECUTOR: str = PYTHON_EXECUTOR

    @staticmethod
    def get(ext: str) -> str:
        return {
            "": EXECUTOR.DEFAULT_EXECUTOR,
            "py": EXECUTOR.PYTHON_EXECUTOR,
            "ps1": EXECUTOR.POWERSHELL_EXECUTOR,
            "vbs": EXECUTOR.VBS_EXECUTOR
        }[ext]


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
        

class LogType(enum.Enum):
    MESSAGE: str = "message"
    COMMAND: str = "command"
    DEFAULT: str = MESSAGE


class LogChannel(enum.Enum):
    BACKUP: str = "backup"
    NOTIFICATION: str = "notification"
    DEBUG: str = "debug"
    PRINTER: str = "printer"
    SYSTEM: str = "system"
    DEFAULT: str = NOTIFICATION


class LogLevel(enum.Enum):
    NORMAL: int = 1
    ERROR: int = 2
    EVENT: int = 4
    DEBUG: str = 8
    DEFAULT: str = NORMAL


class LogCommandName(enum.Enum):
    DEBUG: str = "debug"
    PRINTER_REPORT: str = "printer_report"
    LOG_IN: str = "log_in"
    #
    POLIBASE_DB_BACKUP_START: str = "polibase:db_backup_start"
    POLIBASE_DB_BACKUP_COMPLETE: str = "polibase:db_backup_complete"
    #


#: dict[LogCommandName, LogCommand]
LOG_COMMAND_LIST = {
    LogCommandName.DEBUG: LogCommand("It is a debug command", LogChannel.NOTIFICATION, LogLevel.DEBUG.value),
    #
    LogCommandName.LOG_IN: LogCommand(
        "Пользователь {name} ({computer_name}) вошел", LogChannel.SYSTEM, LogLevel.NORMAL.value, (ParamItem("name", "Name of user"), ParamItem("computer_name", "Name of computer"))),
    #
    LogCommandName.PRINTER_REPORT: LogCommand("Прмнтер {printer_name} ({location}):\n {printer_report}", LogChannel.PRINTER, LogLevel.NORMAL.value, (ParamItem("printer_name", "Name of printer"), ParamItem("location", "Location"), ParamItem("printer_report", "Printer report"))),
    #
    LogCommandName.POLIBASE_DB_BACKUP_START: LogCommand(
        "Start Polibase DataBase Dump backup",  LogChannel.BACKUP, LogLevel.NORMAL.value),
    LogCommandName.POLIBASE_DB_BACKUP_COMPLETE: LogCommand(
        "Complete Polibase DataBase Dump backup",  LogChannel.BACKUP, LogLevel.NORMAL.value)
    #
}
