from typing import List
from .itn import number_of_trailing_zeros


def preprocess(tokens: List[str], word2number: dict):
    num_tokens = len(tokens)
    if num_tokens == 1:
        if tokens[0] in word2number and word2number[tokens[0]][:2] == "00":
            return ["one"] + tokens
        else:
            return tokens

    _tokens = []
    for i in range(num_tokens - 1):
        prev_token = tokens[i - 1]
        curr_token = tokens[i]
        next_token = tokens[i + 1]

        # ---- Converts cases such as "hundred and twenty" -> "hundred twenty"
        if (
            i
            and curr_token == "and"
            and next_token in word2number
            and prev_token in word2number
            and word2number[prev_token][:2] == "00"
            and number_of_trailing_zeros(word2number[prev_token])
            > number_of_trailing_zeros(word2number[next_token])
        ):
            continue

        # ---- Converts cases such as "hundred" -> "one hundred"
        elif (
            i
            and (
                not word2number.get(prev_token, [""])[0].isdigit()
                or word2number.get(prev_token, [""]) == "0"
            )
            and curr_token in word2number
            and word2number[curr_token][:2] == "00"
        ) or (
            not i and curr_token in word2number and word2number[curr_token][:2] == "00"
        ):
            _tokens.append("one")
            _tokens.append(curr_token)

        else:
            _tokens.append(curr_token)

    if _tokens:
        if (
            (
                not word2number.get(curr_token, [""])[0].isdigit()
                or word2number.get(curr_token, [""]) == "0"
            )
            and next_token in word2number
            and word2number[next_token][:2] == "00"
        ):
            _tokens.append("one")
        _tokens.append(next_token)

    return _tokens
