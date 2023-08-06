from contextlib import contextmanager
import sys, os


def cprint(content, color="red", end="\n", bold=False):
    """
    Colored print.
    :param content: Print content. (str)
    :param color: Color name. (str)
    :param end: End format. (str)
    :param bold: Bold or not. (bool)
    :return:
    """
    if color == "black":
        color = 30
    elif color == "red":
        color = 31
    elif color == "green":
        color = 32
    elif color == "yellow":
        color = 33
    elif color == "blue":
        color = 34
    elif color == "purple":
        color = 35
    elif color == "cyan":
        color = 36
    elif color == "gray":
        color = 37
    elif color == "lightgray":
        color = 38
    else:
        print("\033[0;31m[handyscikit] Error: There isn't this color.\033[0m")
        return None

    bold = 1 if bold else 0

    print("\033[%d;%dm%s\033[0m" % (bold, color, content), end=end)


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout