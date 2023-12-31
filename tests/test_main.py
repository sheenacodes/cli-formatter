import pytest
import argparse
from unittest.mock import patch
from formatter.main import (
    validate_char_input,
    validate_number_input,
    print_formatted_output,
    main,
)


def test_validate_char_input_valid():
    """
    test that the validate_char_input() function returns input
    when input is valid
    """
    result = validate_char_input("ST")
    assert result == "ST"

    result = validate_char_input("S")
    assert result == "S"

    result = validate_char_input("T")
    assert result == "T"

    result = validate_char_input("STSTTST")
    assert result == "STSTTST"


def test_validate_char_input_invalid():
    """
    test that the validate_char_input() function raises argument type error
    when input is invalid with corresponding error message
    """

    Err_str_char = (
        "Invalid character input: Character input shall contain S's and T's only"
    )
    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_char):
        validate_char_input("gr")

    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_char):
        validate_char_input("AST")

    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_char):
        validate_char_input("ST4")

    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_char):
        validate_char_input("1")

    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_char):
        validate_char_input("s")


def test_validate_number_input_valid():
    """
    test that the validate_number_input() function returns the input
    when input is valid"""
    result = validate_number_input("1")
    assert result == 1

    result = validate_number_input("11")
    assert result == 11


def test_validate_number_input_invalid():
    """
    test that the validate_number_input() function raises argument type error
    when input is invalid with corresponding error message
    """
    Err_str_number = "Invalid number input: Number shall be a positive integer"
    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_number):
        validate_number_input("gr")

    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_number):
        validate_number_input("-1")

    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_number):
        validate_number_input("0")

    with pytest.raises(argparse.ArgumentTypeError, match=Err_str_number):
        validate_number_input("i")


def test_print_formatted_output(capsys):
    """
    test that pattern output with different valid values of char input and number input
    including number = 1 and 2
    """
    char_input = "ST"

    numbers = [1]
    expected_output = "Soft."
    assert_output(char_input, numbers, expected_output, capsys)

    numbers = [3, 2]
    expected_output = "Soft, Tough and Soft.\nSoft and Tough."
    assert_output(char_input, numbers, expected_output, capsys)

    char_input = "STTS"
    numbers = [5]
    expected_output = "Soft, Tough, Tough, Soft and Soft."
    assert_output(char_input, numbers, expected_output, capsys)


def assert_output(char_input, numbers, expected_output, capsys):
    """
    help function to assert formatted pattern
    """
    print_formatted_output(char_input, numbers)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output


def test_main_valid_input(capsys):
    """
    test output from stdout when main is called with valid arguments
    """
    char_input = "ST"
    number_input = [2, 3]

    with patch(
        "sys.argv", ["main.py", char_input] + [str(num) for num in number_input]
    ):
        main()

    expected_output_lines = ["Soft and Tough.", "Soft, Tough and Soft."]
    captured = capsys.readouterr()
    assert captured.out.strip() == "\n".join(expected_output_lines)


def test_main_invalid_input(capsys):
    """
    test output from stderr when main is called with invalid arguments
    """

    char_input = "ST"
    invalid_number_input = ["q", "5"]

    with patch("sys.argv", ["main.py", char_input] + invalid_number_input):
        with pytest.raises(SystemExit) as context_manager:
            main()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
    assert captured.err.strip() == (
        "usage: main.py [-h] [--verbose] char_input number_input [number_input ...]\n"
        "main.py: error: argument number_input: Invalid number input: Number shall be a positive integer"
    )
    assert context_manager.value.code == 2  # ArgumentTypeError

    char_input = "STp"
    invalid_number_input = ["1", "5"]

    with patch("sys.argv", ["main.py", char_input] + invalid_number_input):
        with pytest.raises(SystemExit) as context_manager:
            main()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
    assert captured.err.strip() == (
        "usage: main.py [-h] [--verbose] char_input number_input [number_input ...]\n"
        "main.py: error: argument char_input: Invalid character input: Character input shall contain S's and T's only"
    )
    assert context_manager.value.code == 2  # ArgumentTypeError
