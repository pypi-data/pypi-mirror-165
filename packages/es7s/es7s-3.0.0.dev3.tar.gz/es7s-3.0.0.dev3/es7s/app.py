# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2022 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.common import BasicApp


class Es7sEntrypointApp(BasicApp):
    def _parse_args(self, *argv):
        super()._parse_args(*argv)

    def _print_help(self):
        pass

    def _print_error(self, e: Exception):
        pass

    def _entrypoint(self):
        pass
