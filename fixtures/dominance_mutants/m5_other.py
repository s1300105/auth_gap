"""mutant 5 の対になるモジュール。**同名の `Router` にゲートがある。**"""

from _prelude import TOOLS, ApprovalDenied, confirm


class Router:
    def dispatch(self, name, args):
        if not confirm(name):
            raise ApprovalDenied(name)
        return TOOLS[name](args)
