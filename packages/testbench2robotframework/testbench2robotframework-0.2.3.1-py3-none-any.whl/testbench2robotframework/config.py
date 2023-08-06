# pylint: skip-file
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List
from .model import StrEnum


@dataclass
class SubdivisionsMapping:
    libraries: Dict
    resources: Dict

    @classmethod
    def from_dict(cls, dictionary):
        return cls(
            libraries=dictionary.get("libraries", {}), resources=dictionary.get("resources", {})
        )


@dataclass
class ForcedImport:
    libraries: List[str]
    resources: List[str]
    variables: List[str]

    @classmethod
    def from_dict(cls, dictionary):
        return cls(
            libraries=dictionary.get("libraries", []),
            resources=dictionary.get("resources", []),
            variables=dictionary.get("variables", []),
        )


class LogLevel(StrEnum):
    CRITICAL = "CRITICAL"
    FATAL = CRITICAL
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = WARNING
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


@dataclass
class ConsoleLoggerConfig:
    logLevel: LogLevel
    logFormat: str

    @classmethod
    def from_dict(cls, dictionary):
        log_level = dictionary.get("logLevel", "INFO").upper()
        if log_level not in LogLevel.__members__:
            print(
                f"ValueError: {log_level} is not a valid logLevel. "
                f"Available logLevel are: {list(LogLevel.__members__)}"
            )
            log_level = LogLevel.INFO
        return cls(
            logLevel=log_level,
            logFormat=dictionary.get("logFormat", "%(levelname)s: %(message)s"),
        )


@dataclass
class FileLoggerConfig(ConsoleLoggerConfig):
    fileName: str

    @classmethod
    def from_dict(cls, dictionary):
        log_level = dictionary.get("logLevel", "DEBUG").upper()
        if log_level not in LogLevel.__members__:
            print(
                f"ValueError: {log_level} is not a valid logLevel. "
                f"Available logLevel are: {list(LogLevel.__members__)}"
            )
            log_level = LogLevel.DEBUG
        return cls(
            logLevel=log_level,
            logFormat=dictionary.get(
                "logFormat", "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)8s - %(message)s"
            ),
            fileName=dictionary.get("fileName", "testbench2robotframework.log"),
        )


@dataclass
class LoggingConfig:
    console: ConsoleLoggerConfig
    file: FileLoggerConfig

    @classmethod
    def from_dict(cls, dictionary):
        return cls(
            console=ConsoleLoggerConfig.from_dict(dictionary.get("console", {})),
            file=FileLoggerConfig.from_dict(dictionary.get("file", {})),
        )


@dataclass
class Configuration:
    rfLibraryRoots: List[str]
    rfResourceRoots: List[str]
    fullyQualified: bool
    subdivisionsMapping: SubdivisionsMapping
    forcedImport: ForcedImport
    generationDirectory: str
    createOutputZip: bool
    resourceDirectory: str
    logSuiteNumbering: bool
    clearGenerationDirectory: bool
    loggingConfiguration: LoggingConfig
    logCompoundInteractions: bool
    testCaseSplitPathRegEx: str
    phasePattern: str

    @classmethod
    def from_dict(cls, dictionary) -> Configuration:
        return cls(
            rfLibraryRoots=dictionary.get("rfLibraryRoots", []),
            rfResourceRoots=dictionary.get("rfResourceRoots", []),
            fullyQualified=dictionary.get("fullyQualified", False),
            subdivisionsMapping=SubdivisionsMapping.from_dict(
                dictionary.get("subdivisionsMapping", {})
            ),
            forcedImport=ForcedImport.from_dict(dictionary.get("forcedImport", {})),
            generationDirectory=dictionary.get("generationDirectory", "{root}/Generated"),
            createOutputZip=dictionary.get("createOutputZip", False),
            logSuiteNumbering=dictionary.get("logSuiteNumbering", False),
            clearGenerationDirectory=dictionary.get("clearGenerationDirectory", True),
            loggingConfiguration=LoggingConfig.from_dict(
                dictionary.get("loggingConfiguration", {})
            ),
            logCompoundInteractions=dictionary.get("logCompoundInteractions", True),
            resourceDirectory=dictionary.get("resourceDirectory", "{root}/Resources").replace(
                '\\', '/'
            ),
            testCaseSplitPathRegEx=dictionary.get("testCaseSplitPathRegEx", ".*StopWithRestart.*"),
            phasePattern=dictionary.get("phasePattern", "{testcase} : Phase {index}/{length}"),
        )


def write_default_config(config_file):
    with open(config_file, 'w', encoding='utf-8') as file:
        json.dump(
            Configuration.from_dict({}).__dict__,
            file,
            default=lambda o: o.__dict__,
            indent=2,
        )
