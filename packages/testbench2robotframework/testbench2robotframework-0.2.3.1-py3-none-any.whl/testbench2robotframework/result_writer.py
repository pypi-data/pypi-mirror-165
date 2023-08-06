import os
import tempfile
import re
import uuid
from datetime import datetime
from distutils.dir_util import copy_tree
from typing import Dict, List, Optional

from robot.result import Keyword, ResultVisitor, TestSuite, TestCase

from .config import Configuration
from .json_reader import TestBenchJsonReader
from .json_writer import write_test_structure_element
from .log import logger
from .model import (
    ActivityStatus,
    ExecutionVerdict,
    InteractionDetails,
    InteractionType,
    InteractionVerdict,
    TestCaseDetails,
    TestCaseExecutionDetails,
    InteractionExecutionSummary,
)
from .utils import directory_to_zip, get_directory


class ResultWriter(ResultVisitor):
    def __init__(self, json_report: str, json_result: str, config: Configuration) -> None:
        self.json_dir = get_directory(json_report)
        self.tempdir = tempfile.TemporaryDirectory(dir=os.curdir)
        if json_result is None:
            self.create_zip = bool(os.path.splitext(json_report)[1].lower() == ".zip")
            self.json_result = self.json_dir
            self.json_result_path = self.json_dir
        else:
            self.json_result_path, result_extension = os.path.splitext(json_result)
            self.create_zip = bool(result_extension.lower() == ".zip")
            self.json_result = self.tempdir.name
            if self.create_zip:
                copy_tree(self.json_dir, self.json_result)
        self.json_reader = TestBenchJsonReader(self.json_dir)
        self.test_suites: Dict[str, TestSuite] = {}
        self.keywords: List[Keyword] = []
        self.itb_test_case_catalog: Dict[str, TestCaseDetails] = {}
        self.phase_pattern = config.phasePattern
        self.test_chain: List[TestCase] = []

    def start_suite(self, suite):
        if suite.metadata:
            self.test_suites[suite.metadata["uniqueID"]] = suite

    def _get_interactions_by_type(
        self, interactions: List[InteractionDetails], interaction_type: InteractionType
    ):
        for interaction in interactions:
            if interaction.interactionType == interaction_type:
                yield interaction
            if interaction.interactionType == InteractionType.Compound:
                yield from self._get_interactions_by_type(
                    interaction.interactions, interaction_type
                )

    def end_test(self, test):
        test_chain = get_test_chain(test.name, self.phase_pattern)
        if test_chain:
            if test_chain.index == 1:
                self.test_chain = [test]
            else:
                self.test_chain.append(test)
            if test_chain.index != test_chain.length:
                return
        else:
            self.test_chain = [test]

        test_uid = test_chain.name if test_chain else test.name
        itb_test_case = self.json_reader.read_test_case(test_uid)  # TODO What if name != UID
        if itb_test_case.exec is None:
            itb_test_case.exec = TestCaseExecutionDetails.from_dict({})
        if itb_test_case.exec.key in ["", "-1"]:
            logger.warning(
                f"Test case {itb_test_case.uniqueID} was not exported based on "
                f"execution and is therefore not importable."
            )
        try:
            atomic_interactions = list(
                self._get_interactions_by_type(itb_test_case.interactions, InteractionType.Atomic)
            )
            compound_interactions = list(
                self._get_interactions_by_type(itb_test_case.interactions, InteractionType.Compound)
            )
            self._set_atomic_interactions_execution_result(atomic_interactions, self.test_chain)
            for interaction in compound_interactions:
                self._set_compound_interaction_execution_result(interaction)
            self._set_itb_testcase_execution_result(itb_test_case, self.test_chain)
        except TypeError:
            logger.error(
                "Could not find an itb testcase that corresponds "
                "to the given Robot Framework testcase."
            )
        self.itb_test_case_catalog[test_uid] = itb_test_case
        write_test_structure_element(self.json_result, itb_test_case)
        logger.debug(
            f"Successfully wrote the result from test "
            f"{itb_test_case.uniqueID} to TestBench's Json Report."
        )

    def _set_itb_testcase_execution_result(self, itb_test_case, test_chain):
        has_failed_chain = list(filter(lambda tc: tc.status.upper() == "FAIL", test_chain))
        passed_keywords = all(tc.status.upper() == "PASS" for tc in test_chain)
        itb_test_case.exec.actualDuration = sum([tc.elapsedtime for tc in test_chain])
        if has_failed_chain:
            self._set_itb_test_case_status(itb_test_case, "fail")
        elif passed_keywords:
            self._set_itb_test_case_status(itb_test_case, "pass")
        else:
            self._set_itb_test_case_status(itb_test_case, "undef")

    def _set_atomic_interactions_execution_result(
        self, atomic_interactions: List[InteractionDetails], test_chain: List[TestCase]
    ):
        test_chain_body = [keyword for test_phase in test_chain for keyword in test_phase.body]
        for index, interaction in enumerate(atomic_interactions):
            if interaction.exec is None:
                interaction.exec = InteractionExecutionSummary.from_dict({})
            if index < len(test_chain_body):
                keyword = test_chain_body[index]
                if not is_normalized_equal(
                    keyword.kwname, interaction.name
                ) and not is_normalized_equal(
                    keyword.kwname, f"{interaction.path.split('.')[-1]}.{interaction.name}"
                ):
                    raise NameError(
                        f"Execution can not be parsed, "
                        f"because keyword name '{keyword.kwname}' does not match with "
                        f"interaction '{interaction.name}' name."
                    )
                interaction.exec.verdict = self._get_interaction_result(keyword.status)
                interaction.exec.time = keyword.endtime
                interaction.exec.duration = keyword.elapsedtime
                interaction.exec.comments = "\n".join(
                    [self._create_itb_exec_comment(message) for message in keyword.messages]
                )
            else:
                interaction.exec.verdict = InteractionVerdict.Undefined

    @staticmethod
    def _create_itb_exec_comment(
        message,
    ) -> str:  # Todo: low prio: pattern für message in config festlegen
        message_time = datetime.strptime(message.timestamp, '%Y%m%d %H:%M:%S.%f').isoformat()
        return f"{message_time}:{message.level}:{message.message}"

    def _set_compound_interaction_execution_result(self, compound_interaction: InteractionDetails):
        atomic_interactions = list(
            self._get_interactions_by_type(
                compound_interaction.interactions, InteractionType.Atomic
            )
        )
        if compound_interaction.exec is None:
            compound_interaction.exec = InteractionExecutionSummary.from_dict({})
        compound_interaction.exec.verdict = InteractionVerdict.Skipped
        for atomic in atomic_interactions:
            if atomic.exec is None:
                logger.debug(
                    f"Atomic interaction {atomic.uniqueID} "
                    f"had no exec details and therefore ignored."
                )
                atomic.exec = InteractionExecutionSummary.from_dict({})
                # continue
            if atomic.exec.verdict is InteractionVerdict.Fail:
                compound_interaction.exec.verdict = InteractionVerdict.Fail
                break
            if atomic.exec.verdict is InteractionVerdict.Pass:
                compound_interaction.exec.verdict = InteractionVerdict.Pass

        compound_interaction.exec.duration = sum(
            [interaction.exec.duration for interaction in atomic_interactions]
        )
        compound_interaction.exec.time = atomic_interactions[-1].exec.time

    @staticmethod
    def _set_itb_test_case_status(itb_test_case: TestCaseDetails, robot_status: str):
        robot_status = robot_status.lower()
        if robot_status == 'pass':
            itb_test_case.exec.status = ActivityStatus.Performed
            itb_test_case.exec.verdict = ExecutionVerdict.Pass
        elif robot_status == 'fail':
            itb_test_case.exec.status = ActivityStatus.Performed
            itb_test_case.exec.verdict = ExecutionVerdict.Fail
        else:
            itb_test_case.exec.status = ActivityStatus.Running
            itb_test_case.exec.verdict = ExecutionVerdict.Undefined

    def end_suite(self, suite):
        if not suite.metadata.get("uniqueID") or len(suite.suites):
            return
        test_case_set = self.json_reader.read_test_case_set(suite.metadata["uniqueID"])
        if not test_case_set:
            return
        test_case_set.exec.verdict = suite.status
        for testcase in test_case_set.testCases:
            current_itb_test_case = self.itb_test_case_catalog.get(testcase.uniqueID)
            if current_itb_test_case is None:
                continue
            testcase.exec.verdict = current_itb_test_case.exec.verdict
            testcase.exec.status = current_itb_test_case.exec.status
            testcase.exec.execStatus = current_itb_test_case.exec.execStatus
            testcase.exec.comments = current_itb_test_case.exec.comments
        write_test_structure_element(self.json_result, test_case_set)
        logger.debug(
            f"Successfully wrote the result from suite "
            f"{test_case_set.uniqueID} to TestBench's Json Report."
        )

    def end_result(self, result):
        tt_tree = self.json_reader.read_test_theme_tree()
        if tt_tree:
            test_suite_counter = 0
            for tse in tt_tree.nodes:
                if self.test_suites.get(tse.baseInformation.uniqueID) is None:
                    continue
                execution_result = self._get_execution_result(
                    self.test_suites[tse.baseInformation.uniqueID].status
                )
                tse.execution.verdict = execution_result["execution_verdict"]
                tse.execution.status = execution_result["activity_status"]
                test_suite_counter += 1
            write_test_structure_element(self.json_result, tt_tree)
            if test_suite_counter and self.itb_test_case_catalog:
                logger.info(f"Successfully read {test_suite_counter} test suites.")
            else:
                logger.warning("No test suites with execution information found.")
            if self.create_zip:
                directory_to_zip(self.json_result, self.json_result_path)
            elif self.json_result != self.json_result_path:
                copy_tree(self.json_dir, self.json_result_path)
                copy_tree(self.json_result, self.json_result_path)
            self.tempdir.cleanup()
        logger.info("Successfully wrote the robot execution results to TestBench's Json Report.")

    @staticmethod
    def _get_execution_result(robot_status: str) -> Dict:
        robot_status = robot_status.lower()
        if robot_status == "pass":
            return {
                "execution_verdict": ExecutionVerdict.Pass,
                "activity_status": ActivityStatus.Performed,
            }
        if robot_status == "fail":
            return {
                "execution_verdict": ExecutionVerdict.Fail,
                "activity_status": ActivityStatus.Performed,
            }
        return {
            "execution_verdict": ExecutionVerdict.Undefined,
            "activity_status": ActivityStatus.Skipped,
        }

    @staticmethod
    def _get_interaction_result(robot_status: str) -> InteractionVerdict:
        robot_status = robot_status.upper()
        if robot_status == "PASS":
            return InteractionVerdict.Pass
        if robot_status == "FAIL":
            return InteractionVerdict.Fail
        if robot_status == "NOT RUN":
            return InteractionVerdict.Undefined
        return InteractionVerdict.Skipped


class TestChain:
    def __init__(self, name, index, length):
        self.name = str(name)
        self.index = int(index)
        self.length = int(length)


def get_test_chain(test_name: str, phase_pattern: str) -> Optional[TestChain]:
    matcher = re.match(get_test_chain_pattern(phase_pattern), test_name)
    if matcher:
        return TestChain(*matcher.groups())
    return None


def get_test_chain_pattern(phase_pattern: str) -> str:
    testcase_placeholder = str(uuid.uuid4().int)
    index_placeholder = str(uuid.uuid4().int)
    length_placeholder = str(uuid.uuid4().int)
    raw_pattern = re.escape(
        phase_pattern.format(
            testcase=testcase_placeholder,
            index=index_placeholder,
            length=length_placeholder,
        )
    )
    return (
        raw_pattern.replace(testcase_placeholder, r"(.+?)")
        .replace(index_placeholder, r"(\d)")
        .replace(length_placeholder, r"(\d)")
    )


def get_normalized_keyword_name(keyword_name: str) -> str:
    return re.sub(r"[\s_]", "", keyword_name.lower())


def is_normalized_equal(kw_one: str, kw_two: str) -> bool:
    norm_kw_one = get_normalized_keyword_name(kw_one)
    norm_kw_two = get_normalized_keyword_name(kw_two)
    return norm_kw_one == norm_kw_two
