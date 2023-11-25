# The objective of this exercise is to write clean, documented, possible verbose (logging), and
# testable code. All functions, excluding main, should be tested. Return all required
# commands to compile, test, and execute your code.
# Please also include your thoughts on this exercise. What parts did you find easy or difficult?
# How much time did you spend on the exercise?

# Write a command line application that takes at least two arguments as input.
# The first argument is a random pattern consisting of characters S and T. For example 'STTTS'.
# The following arguments are N (N >= 1) number of integers. For example 1 5 8. Each integer is
# separated from previous one with a space.
# The application must validate input arguments.
# There needs to be enough arguments given
# Pattern must consist only of valid characters
# Numbers need to be integers
# The application needs to convert each character in the pattern into human readable text
# and output the corresponding text. The length of the output is defined by the integer
# argument. For each input integer, the output needs to follow given pattern.
# Character mapping to text.
# S = soft
# T = tough
# Example run:
# Input:
# SST 5 2
# Output:
# Soft, Soft, Tough, Soft and Soft.
# Soft and Soft.
# Note! Pay attention to the output formatting!

import argparse
import re
from typing import List
import logging

logging.getLogger().setLevel(logging.INFO)


def validate_char_input(value: str) -> str:
    """
    argparse validation function to check if
    character argument consists only of S's and T's
    """
    if not re.match(r"[ST]+$", value):
        raise argparse.ArgumentTypeError(
            "Invalid character input: Character input shall contain S's and T's only"
        )
    return value


def validate_number_input(value: str) -> int:
    """
    argparse validation function to check if
    numbers argument is a positive integer
    """
    # ivalue = int(value)
    if not value.isdigit() or int(value) < 1:
        raise argparse.ArgumentTypeError(
            "Invalid number input: Number shall be a positive integer"
        )
    return int(value)


def print_formatted_output(char_input: str, numbers: List[int]) -> None:
    """
    prints formatted string from the input arguments
    """
    word = {"S": "Soft", "T": "Tough"}
    for number in numbers:
        max_k = len(char_input)
        # char_indices = [i%max_k for i in range(number)]
        # formatted_words = [words[char_input[i]] for i in char_indices]
        formatted_words = [word[char_input[i % max_k]] for i in range(number)]
        formatted_line = ""
        if number > 1:
            formatted_line = (
                ", ".join(formatted_words[0 : number - 1])
                + f" and {formatted_words[number-1]}."
            )
        else:
            formatted_line = f"{formatted_words[0]}."

        print(formatted_line)


def main():
    parser = argparse.ArgumentParser(description="character formatter app")
    parser.add_argument(
        "char_input", help="character input to be formatted", type=validate_char_input
    )
    parser.add_argument(
        "number_input",
        help="number input for formatting",
        nargs="+",
        type=validate_number_input,
    )
    parser.add_argument("--verbose", help="enable verbose logging", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.debug(f"Pattern Input: {args.char_input}")
    logging.debug(f"Number Input: {args.number_input}")
    print_formatted_output(args.char_input, args.number_input)


if __name__ == "__main__":
    main()
