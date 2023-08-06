import json
import os
import re
from dataclasses import dataclass
from typing import List

from testbench2robotframework.config import Configuration
from testbench2robotframework.model import TestCaseDetails, TestCaseSetDetails, TestStructureTree


@dataclass
class TestCaseSet:
    details: TestCaseSetDetails
    test_cases: List[TestCaseDetails]


TEST_CASE_SET_REGEX = "^itb(.*)-TC-([0-9]*).json$"
TEST_CASE_REGEX = "(.*)-PC-([0-9]*).json$"
TEST_STRUCTURE_TREE_REGEX = "TestThemeTree.json$"


def get_test_cases(test_case_set_details, test_cases_details):
    return [
        test_case_details
        for test_case_details in test_cases_details
        if test_case_set_details.uniqueID in test_case_details.uniqueID
    ]


def read_json(filepath: str):
    with open(filepath, encoding='utf-8') as json_file:
        return json.load(json_file)


def get_test_case_sets(json_dir: str):
    test_case_sets = read_json_files(json_dir, TEST_CASE_SET_REGEX)
    test_cases = read_json_files(json_dir, TEST_CASE_REGEX)

    test_case_sets_details = [
        TestCaseSetDetails.from_dict(test_case_set) for test_case_set in test_case_sets
    ]
    test_cases_details = [TestCaseDetails.from_dict(test_case) for test_case in test_cases]

    return [
        TestCaseSet(
            test_case_set_details, get_test_cases(test_case_set_details, test_cases_details)
        )
        for test_case_set_details in test_case_sets_details
    ]


def read_json_files(json_dir: str, file_name_regex: str):
    return [
        read_json(os.path.join(json_dir, file))
        for file in os.listdir(json_dir)
        if re.match(file_name_regex, file, flags=re.IGNORECASE)
    ]


def get_test_theme_tree(json_dir: str):
    test_structure_tree = read_json_files(json_dir, TEST_STRUCTURE_TREE_REGEX)
    test_theme_tree = TestStructureTree.from_dict(test_structure_tree[0])
    return test_theme_tree
