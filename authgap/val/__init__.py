"""val エンジン（§2.6）。

`val` は各制御位置の値を誰が決めるかを推論する。**等級は付けない** —
strong / weak の判定は Def 5 のゲート採点器（`authgap.gate`）が単独で行う。
"""

from .engine import (
    AliasFact,
    CallEvent,
    Env,
    Options,
    ValEngine,
    ValResult,
    access_path,
    env_join,
    seed_model_param,
)

__all__ = [
    "AliasFact",
    "CallEvent",
    "Env",
    "Options",
    "ValEngine",
    "ValResult",
    "access_path",
    "env_join",
    "seed_model_param",
]
