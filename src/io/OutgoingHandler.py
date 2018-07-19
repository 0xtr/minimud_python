from enum import Enum


class OutgoingDefs(Enum):
    BUFFER_LENGTH = 1024
    PRINT_LINE_WIDTH = 80
    NAMES_MIN = 5
    HASH_LENGTH = 70
    SALT_LENGTH = 50


def outgoing_handler(player):
    expected = buffer_pos = 0

    if (1 + len(player.buffer)) <= OutgoingDefs.PRINT_LINE_WIDTH.value:
        # TODO: prompt chars again
        # expected += add_prompt_chars(player)
        return send_and_handle_errors(player, expected)

    lines_required = get_buffer_split_by_line_width(player.buffer) + num_of_newlines(player)
    processedBuf = ''

    for i in range(0, lines_required):
        stop_at_char = find_reasonable_line_end(player, buffer_pos)
        processedBuf = player.buffer[buffer_pos:stop_at_char]
        processedBuf += "\n"

        buffer_pos += stop_at_char + 1
        if buffer_pos >= expected:
            break

    if processedBuf.rfind("\n") != len(processedBuf):
        processedBuf += "\n"

    player.buffer = processedBuf
    return send_and_handle_errors(player, expected)


def num_of_newlines(player):
    newlines = 0
    for i in range(0, len(player.buffer)):
        if player.buffer[i] == '\n':
            newlines += 1

    return newlines


def find_reasonable_line_end(player, buffer_pos):
    """Find the last space or newline in the next LINE_WIDTH chars"""
    line_width_val = OutgoingDefs.PRINT_LINE_WIDTH.value

    substr = player.buffer[buffer_pos:(buffer_pos + line_width_val)]
    print("find line end in: " + substr)

    if len(substr) < line_width_val:
        return len(substr)

    last_value = len(substr)
    find_match = substr.rfind(" ")
    if find_match is not -1:
        last_value = find_match

    find_match = substr.rfind("\n")
    if find_match is not -1:
        last_value = find_match

    if (float((last_value / line_width_val) * 100)) < 70:
        return line_width_val

    print("last value: " + last_value)
    return last_value


def get_buffer_split_by_line_width(expected):
    lines = float(expected / OutgoingDefs.PRINT_LINE_WIDTH.value)
    if not lines.is_integer():
        lines += 1

    return lines


def send_and_handle_errors(player, expected):
    returned = total = 0

    while returned < expected:
        returned = player.socket_num.send(player.buffer[total])
        if returned == 0:
            player.buffer = ''
            return 1

    player.buffer = ''
    return 0
