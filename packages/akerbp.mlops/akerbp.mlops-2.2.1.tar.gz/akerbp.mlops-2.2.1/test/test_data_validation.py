from src.akerbp.mlops.core.helpers import input_data_validation
from typing import List

required_input = ["DEN", "AC", "NEU", "PEF"]


def test_input_data_validation_correct_input_logs_return_true(
    required_input: List = required_input,
):
    input_with_logs = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input, input=input_with_logs
    )
    assert validated


def test_input_data_validation_correct_input_logs_multiple_wells_return_true(
    required_input: List = required_input,
):
    input_with_multiple_logs = {
        "input": [
            {
                "well": "well1",
                "input_logs": {
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
            {
                "well": "well2",
                "input_logs": {
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input, input=input_with_multiple_logs
    )
    assert validated


def test_input_data_validation_wrong_logs_return_false(
    required_input: List = required_input,
):
    input_with_wrong_logs = {
        "input": [
            {
                "well": "well-123",
                "input_logs": {
                    "ACS": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input, input=input_with_wrong_logs
    )
    assert not validated


def test_input_data_validation_wrong_logs_multiple_wells_return_false(
    required_input: List = required_input,
):
    input_with_wrong_logs_multiple_wells = {
        "input": [
            {
                "well": "well1",
                "input_logs": {
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
            {
                "well": "well2",
                "input_logs": {
                    "ACS": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input, input=input_with_wrong_logs_multiple_wells
    )
    assert not validated


def test_input_data_validation_wrongly_specified_input_logs_return_false(
    required_input: List = required_input,
):
    input_wrongly_specified_input_logs = {
        "input": [
            {
                "well": "well-123",
                "required_input": {
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input, input=input_wrongly_specified_input_logs
    )
    assert not validated


def test_input_data_validation_wrongly_specified_input_logs_multiple_wells_return_false(
    required_input: List = required_input,
):
    input_wrongly_specidied_input_logs_multiple_wells = {
        "input": [
            {
                "well": "well-1",
                "input_curves": {
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
            {
                "well": "well-2",
                "required_input_curves": {
                    "DEN": [],
                    "AC": [],
                    "NEU": [],
                    "PEF": [],
                },
                "keyword_arguments": {},
            },
        ]
    }
    validated = input_data_validation(
        required_input=required_input,
        input=input_wrongly_specidied_input_logs_multiple_wells,
    )
    assert not validated


def test_input_data_validation_with_well_and_kwargs_only_return_true(
    required_input: List = required_input,
):
    input_with_well_and_kwargs_only = {
        "input": [{"well": "well-123", "keyword_arguments": {}}]
    }
    validated = input_data_validation(
        required_input=required_input, input=input_with_well_and_kwargs_only
    )
    assert validated


def test_input_data_validation_with_well_only_return_true(
    required_input: List = required_input,
):
    input_with_well_only = {"input": [{"well": "well-123"}]}
    validated = input_data_validation(
        required_input=required_input, input=input_with_well_only
    )
    assert validated
