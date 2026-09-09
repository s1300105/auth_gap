"""mutant 1: `ok = confirm(name)` の束縛のみで無条件 dispatch。

期待: **非支配**。承認割り込みの名前は現れるが戻り値が分岐条件として使われて
いないので、A-a（送出）でも A-c（分岐条件）でもない。`confirm` は木内で解決でき
拒否側が raise しないことも分かるので、A-b でもない。したがってゲートしていない。

**1 件でも支配と判定したら B3a 不合格。**
"""

from _prelude import TOOLS, confirm


def dispatch(name, args):
    ok = confirm(name)  # WITNESS
    del ok
    return TOOLS[name](args)  # EFFECT
