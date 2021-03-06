import logging
import sys

import numpy as np

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)


# copied from day1, only the minus on -np.eye(n) is added
def get_window_matrix_minus(n, w_size):
    res = np.eye(n)
    for i in range(1, w_size):
        shifted = np.roll(-np.eye(n), shift=i, axis=1)
        shifted[:, :i] = 0
        res += shifted
    return res


def get_concurrent_diffs(arr):
    return get_window_matrix_minus(arr.shape[0], 2) @ arr


logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(stream_handler)

closings = np.array(list(map(ord, [")", "]", "}", ">"])))
penalties = dict(zip(closings, np.array([3, 57, 1197, 25137])))
logger.info(f"{penalties=}")

incomplete_penalties = dict(zip(closings, np.arange(1, 5)))
logger.info(f"{incomplete_penalties=}")

total_score = 0
incomplete_score_list = []
for msg in raw_input:
    logger.info(f"Current line: {msg}")
    msg_score = 0

    left_over_msg = np.array(list(msg))
    left_over = np.array(list(map(ord, left_over_msg)))

    while True:
        concurrent_diffs = get_concurrent_diffs(left_over)
        completed_chunks = (concurrent_diffs == -1) | (concurrent_diffs == -2)
        completed_chunks[np.where(completed_chunks)[0] + 1] = True
        left_over = left_over[~completed_chunks]
        left_over_msg = left_over_msg[~completed_chunks]
        if not np.any(completed_chunks):
            break

    logger.debug(f"{left_over=}")
    logger.debug(f"{''.join(left_over_msg)}")

    closing_flag = np.isin(left_over, closings)
    if np.any(closing_flag):
        msg_score = penalties[left_over[closing_flag][0]]

    logger.debug(f"{msg_score=}")
    total_score += msg_score

    if msg_score == 0: # then incomplete line
        logger.info("Incomplete line!")
        logger.debug(left_over)
        logger.debug(left_over_msg)
        missing_parts = left_over[::-1] + 2
        missing_parts[missing_parts == 42] -= 1
        incomplete_score = 0
        for icon in missing_parts:
            incomplete_score *= 5
            incomplete_score += incomplete_penalties[icon]
        logger.info(incomplete_score)
        incomplete_score_list.append(incomplete_score)

print(f"Part 1 Score: {total_score}")
print(f"Part 2 Score: {sorted(incomplete_score_list)[len(incomplete_score_list) // 2]}")
