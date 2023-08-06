# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2022 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import subprocess
import sys
import traceback
from subprocess import CompletedProcess, PIPE, CalledProcessError
from typing import Any, TextIO

from pytermor import Styles as StylesStub, Colors, Style, NOOP_STYLE, SgrRenderer


class Styles(StylesStub):
    TEXT_DEFAULT = Style(fg=Colors.XTERM_GREY_62)
    DEBUG = Style(fg=Colors.MAGENTA)
    INFO = NOOP_STYLE


class AppBase:
    VERBOSITY = 2

    LEVEL_ERROR = 1
    LEVEL_WARNING = 2
    LEVEL_INFO = 3
    LEVEL_DEBUG = 4

    @classmethod
    def debug(cls, msg: Any, file: TextIO = sys.stderr):
        if cls.VERBOSITY >= cls.LEVEL_DEBUG:
            print(Styles.DEBUG.render(f'DEBUG: {msg}'), file=file)

    @classmethod
    def info(cls, msg: Any, file: TextIO = sys.stderr):
        if cls.VERBOSITY >= cls.LEVEL_INFO:
            print(Styles.INFO.render(f'INFO: {msg}'), file=file)

    @classmethod
    def warn(cls, msg: Any, file: TextIO = sys.stderr):
        if cls.VERBOSITY >= cls.LEVEL_WARNING:
            print(Styles.WARNING.render(f'WARNING: {msg}'), file=file)

    @classmethod
    def _exception(cls, e: Exception, file: TextIO = sys.stderr):
        if not cls.VERBOSITY >= cls.LEVEL_ERROR:
            return

        error_label = 'ERROR: '
        error_msg = e.__class__.__name__ + ': ' + (str(e) or "<empty>")
        error_trace = ''

        if cls.VERBOSITY >= cls.LEVEL_DEBUG:
            tb_lines = [line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__)]
            error_msg = tb_lines.pop(-1)
            error_trace = '\n'.join(tb_lines) + '\n\n'

        print(Styles.ERROR.render(error_trace) +
              Styles.ERROR.render(error_label) +
              Styles.ERROR_ACCENT.render(error_msg), file=file)

    @classmethod
    def print(cls, msg: Any = '', file=sys.stdout):
        print(msg, file=file)

    @classmethod
    def run_subprocess(cls, *args) -> CompletedProcess:
        cls.debug(f'Running: {" ".join(args)}')

        try:
            return subprocess.run(args, stdout=PIPE, stderr=PIPE, encoding='utf8', check=True)
        except CalledProcessError as e:
            cls.debug(f'Subprocess output stream: -----------------\n{e.stdout}')
            cls.debug(f'Subprocess error stream: ------------------\n{e.stderr}')
            cls.debug(f'Subprocess terminated with code {e.returncode:<3d} -------')
            raise e

    def run(self):
        try:
            self._parse_args()
            self._entrypoint()
        except Exception as e:
            self._exception(e)
            self._print_error(e)
            exit(1)

    def _parse_args(self):
        if '--debug' in sys.argv:
            AppBase.VERBOSITY = 4
        if '--verbose' in sys.argv:
            AppBase.VERBOSITY = 3
        if '--silent' in sys.argv:
            AppBase.VERBOSITY = 0

        if '--raw' in sys.argv:
            SgrRenderer.set_up(None)

        if '--help' in sys.argv:
            self._print_help()
            exit(0)

        if '--test' in sys.argv:
            self._print_test()
            exit(0)

    def _print_help(self): raise NotImplementedError

    def _print_test(self): raise NotImplementedError

    def _print_error(self, e: Exception): raise NotImplementedError

    def _entrypoint(self): raise NotImplementedError
