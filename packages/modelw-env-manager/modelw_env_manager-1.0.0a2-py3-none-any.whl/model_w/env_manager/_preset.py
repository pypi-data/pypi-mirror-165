from typing import TYPE_CHECKING, Any, Iterator, MutableMapping

from ._utils import loose_call

if TYPE_CHECKING:
    from model_w.env_manager import EnvManager


class Preset:
    """
    Implement this class to have a configuration preset
    """

    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """Will be run at the beginning of the context"""

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]):
        """
        Will be run at the end of the context. You can use this to check what
        settings the user has set and to modify them if needed.
        """


class ComposePreset(Preset):
    """
    This helps composing different presets into one preset. Just provide them
    as arguments.
    """

    def __init__(self, *presets: Preset):
        self.presets = presets

    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]) -> None:
        """
        Run all presets in order
        """

        for preset in self.presets:
            preset.pre(env, context)

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]) -> None:
        """
        Run all presets in order
        """

        for preset in self.presets:
            preset.post(env, context)


class AutoPreset(Preset):
    """
    Auto preset inspects itself (well any subclass) in order to provide presets
    more easily by simply yielding them. You can check the docs about this.
    """

    def get_x_functions(self, x: str) -> Iterator[str]:
        """
        Simply listing all methods and determining which one we shoudl call
        """

        for k in dir(self):
            if k.startswith(f"{x}_"):
                yield k

    def run_x(
        self, x: str, env: "EnvManager", context: MutableMapping[str, Any]
    ) -> None:
        """
        Runs either pre or post functions
        """

        for func_name in self.get_x_functions(x):
            for k, v in loose_call(getattr(self, func_name), env=env, context=context):
                context[k] = v

    def pre(self, env: "EnvManager", context: MutableMapping[str, Any]) -> None:
        self.run_x("pre", env, context)

    def post(self, env: "EnvManager", context: MutableMapping[str, Any]) -> None:
        self.run_x("post", env, context)
