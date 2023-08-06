# function-burger 🍔 by shinya_sun_sun, MIT license

import datetime
import threading as th
from enum import Enum, auto
from typing import Any, Callable, Dict, Optional


class LogLevel(Enum):
    DEBUG = ("\033[36m", "\033[0m")
    INFO = ("", "")
    WARN = ("\033[33m", "\033[0m")
    ERROR = ("\033[31m", "\033[0m")
    VERBOSE = ("\033[35m", "\033[0m")


class LogPosition(Enum):
    TOP = auto()
    BOTTOM = auto()
    BURGER = auto()


class LogColor(Enum):
    VANILLA_SHAKE = ("", "")
    MUSTARD = ("\033[33m", "\033[0m")
    KETCHUP = ("\033[31m", "\033[0m")
    MINT_CHOCOLATE = ("\033[36m", "\033[0m")
    SODA = ("\033[34m", "\033[0m")
    LETTUCE = ("\033[32m", "\033[0m")
    GRAPE_JUICE = ("\033[35m", "\033[0m")
    COLA = ("\033[30m", "\033[0m")


def _log(
    level: LogLevel = LogLevel.INFO,
    pos: LogPosition = LogPosition.BURGER,
    timestamp: bool = True,
    elapsed_time: bool = False,
    fname: bool = False,
    tid: bool = False,
    inputval: bool = False,
    inputval_func: Optional[Callable] = None,
    retval: bool = False,
    retval_func: Optional[Callable] = None,
    top_word: str = "",
    bottom_word: str = "",
    color: LogColor = LogColor.VANILLA_SHAKE,
) -> Callable:
    def _inner(f: Callable) -> Callable:
        def _wrapper(*args: Any, **keywords: Dict[str, Any]) -> Any:
            time_s = datetime.datetime.now()
            if pos != LogPosition.BOTTOM:
                log_s = []
                log_s.append(f"{level.value[0]}[{level.name}]{level.value[1]}")
                log_s[-1] = log_s[-1] + f"{color.value[0]}"

                if timestamp:
                    log_s.append(f"{time_s}")
                if tid:
                    log_s.append(f"[{th.get_ident()}]")
                if fname:
                    log_s.append(f"func[{f.__name__}]")
                if len(top_word):
                    log_s.append(f"{top_word}")
                if inputval:
                    if inputval_func:
                        log_s.append(
                            f"args[{inputval_func(*args, **keywords)}]"
                        )
                    else:
                        log_s.append(f"args[{args}] keywords[{keywords}]")
                log_s[-1] = log_s[-1] + f"{color.value[1]}"

                print(" ".join(log_s))

            bk_e = None
            try:
                ret = f(*args, **keywords)
            except Exception as e:
                bk_e = e
                raise e
            finally:
                if pos != LogPosition.TOP:
                    time_e = datetime.datetime.now()
                    log_e = []
                    log_e.append(
                        f"{level.value[0]}[{level.name}]{level.value[1]}"
                    )
                    log_e[-1] = log_e[-1] + f"{color.value[0]}"

                    if timestamp:
                        log_e.append(f"{time_e}")
                    if tid:
                        log_e.append(f"[{th.get_ident()}]")
                    if fname:
                        log_e.append(f"func[{f.__name__}]")
                    if len(bottom_word):
                        log_e.append(f"{bottom_word}")
                    if elapsed_time:
                        log_e.append(f"elapsed time[{time_e - time_s}]")
                    if bk_e:
                        log_e.append(f"\033[7m\033[31mexcept[{bk_e}]\033[0m")
                    elif retval:
                        if ret and retval_func:
                            v = retval_func(ret)
                            log_e.append(f"ret[{v}]")
                        else:
                            log_e.append(f"ret[{ret}]")
                    log_e[-1] = log_e[-1] + f"{color.value[1]}"

                    print(" ".join(log_e))

            return ret

        return _wrapper

    return _inner


def burger_log(
    level: LogLevel = LogLevel.INFO,
    timestamp: bool = True,
    elapsed_time: bool = False,
    fname: bool = False,
    tid: bool = False,
    inputval: bool = False,
    inputval_func: Optional[Callable] = None,
    retval: bool = False,
    retval_func: Optional[Callable] = None,
    top_word: str = "",
    bottom_word: str = "",
    color: LogColor = LogColor.VANILLA_SHAKE,
) -> Callable:
    """Output logs before and after each function call.

    Args:
        level (LogLevel, optional): Specify the log level.
        timestamp (bool, optional): Specify timestamp output.
        elapsed_time (bool, optional): Specify elapsed time output.
        fname (bool, optional): Specifies the output of the function name.
        tid (bool, optional): Specifies the output of the thread ID.
        inputval (bool, optional): Specifies the output of the input value.
        inputval_func (Optional[Callable], optional):
            Specifies a function to edit the output format of input values.
        retval (bool, optional): Specifies the output of the return value.
        retval_func (Optional[Callable], optional):
            Specifies a function to edit the output format of the return value.
        word (str, optional): Specifies the string to be output to the log.
        top_word (str, optional):
            Specifies the string to be output to the log
            before the function call.
        bottom_word (str, optional):
            Specifies the string to be output to the log
            after a function call.
        color (LogColor, optional):
            Specifies the text color of the log.

    Returns:
        Callable: log output function.
    """
    return _log(
        level=level,
        pos=LogPosition.BURGER,
        timestamp=timestamp,
        elapsed_time=elapsed_time,
        fname=fname,
        tid=tid,
        inputval=inputval,
        inputval_func=inputval_func,
        retval=retval,
        retval_func=retval_func,
        top_word=top_word,
        bottom_word=bottom_word,
        color=color,
    )


def top_log(
    level: LogLevel = LogLevel.INFO,
    timestamp: bool = True,
    fname: bool = False,
    tid: bool = False,
    inputval: bool = False,
    inputval_func: Optional[Callable] = None,
    word: str = "",
    color: LogColor = LogColor.VANILLA_SHAKE,
) -> Callable:
    """Output log before function call.

    Args:
        level (LogLevel, optional): Specify the log level.
        timestamp (bool, optional): Specify timestamp output.
        fname (bool, optional): Specifies the output of the function name.
        tid (bool, optional): Specifies the output of the thread ID.
        inputval (bool, optional): Specifies the output of the input value.
        inputval_func (Optional[Callable], optional):
            Specifies a function to edit the output format of input values.
        word (str, optional): Specifies the string to be output to the log.
        color (LogColor, optional):
            Specifies the text color of the log.

    Returns:
        Callable: log output function.
    """
    return _log(
        level=level,
        pos=LogPosition.TOP,
        timestamp=timestamp,
        fname=fname,
        tid=tid,
        inputval=inputval,
        inputval_func=inputval_func,
        top_word=word,
        color=color,
    )


def bottom_log(
    level: LogLevel = LogLevel.INFO,
    timestamp: bool = True,
    elapsed_time: bool = False,
    fname: bool = False,
    tid: bool = False,
    retval: bool = False,
    retval_func: Optional[Callable] = None,
    word: str = "",
    color: LogColor = LogColor.VANILLA_SHAKE,
) -> Callable:
    """Output log after function call.

    Args:
        level (LogLevel, optional): Specify the log level.
        timestamp (bool, optional): Specify timestamp output.
        elapsed_time (bool, optional): Specify elapsed time output.
        fname (bool, optional): Specifies the output of the function name.
        tid (bool, optional): Specifies the output of the thread ID.
        retval (bool, optional): Specifies the return output.
        retval_func (Optional[Callable], optional):Specifies the function
            to edit the output value of the return value.
        word (str, optional): Specifies the string to be output to the log.
        color (LogColor, optional):
            Specifies the text color of the log.

    Returns:
        Callable: log output function.
    """
    return _log(
        level=level,
        pos=LogPosition.BOTTOM,
        timestamp=timestamp,
        elapsed_time=elapsed_time,
        fname=fname,
        tid=tid,
        retval=retval,
        retval_func=retval_func,
        bottom_word=word,
        color=color,
    )
