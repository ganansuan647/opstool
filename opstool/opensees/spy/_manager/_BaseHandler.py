from abc import ABC, abstractmethod
from typing import Any, Union


class BaseHandler(ABC):
    # ---------------------------------------------------------------------
    # Abstract Property - MUST be implemented by subclasses
    # ---------------------------------------------------------------------
    @property
    @abstractmethod
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        """
        A set of parsing rules for the most commonly used OpenSeesPy
        commands.  Each entry describes how positional arguments should be mapped
        and what optional *flag*-style arguments exist.  A trailing ``*`` on the
        key name indicates that the value can contain an arbitrary number of
        tokens which will be returned as a :class:`list`.

        Example(OpenSeesPy Commands):
            node(nodeTag, *crds, '-ndf', ndf, '-mass', *mass, '-disp', ...)
            mass(nodeTag, *massValues)
            element(typeName, tag, *args)
            uniaxialMaterial(matType, matTag, *matArgs)
            timeSeries(typeName, tag, *args)
            load(tag, *args)

        Example(rule set dict): {
            "node": {
                "positional": ["tag", "coords*"],
                "options": {
                    "-ndf": "ndf",
                    "-mass": "mass*",
                    "-disp": "disp*",
                    "-vel": "vel*",
                    "-accel": "accel*",
                },
            },
            "mass": {
                "positional": ["tag", "mass*"],
            },
            "element": {
                "positional": ["typeName", "tag", "args*"],
            },
            "uniaxialMaterial": {
                "positional": ["matType", "matTag", "args*"],
            },
            "timeSeries": {
                "positional": ["typeName", "tag", "args*"],
            },
            "load": {
                "positional": ["tag", "args*"],
            },
        }
        """
        raise NotImplementedError

    # ---------------------------------------------------------------------
    # Abstract API - MUST be implemented by subclasses
    # ---------------------------------------------------------------------
    @abstractmethod
    def handles(self) -> list[str]:
        """Return a list of function names this handler can process."""
        raise NotImplementedError

    @abstractmethod
    def handle(self, func_name: str, arg_map: dict[str, Any]):
        """Process the function *func_name* using the already parsed *arg_map*."""
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        """Reset internal data maintained by a concrete handler."""
        raise NotImplementedError


    # ------------------------------------------------------------------
    # Generic helpers shared by all handlers
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_args_by_str(lst: list[Any], target_keys: Union[str, list, tuple, set]) -> list[Any]:
        """Return the values *following* any of *target_keys* until the next
        string token is encountered.

        Parameters
        ----------
        lst : list[Any]
            The full argument list.
        target_keys : Union[str, list, tuple, set]
            A single key or an iterable of keys that should be searched for.

        Returns
        -------
        list[Any]
            List of non-string values following any target key until the next string.

        Notes
        -----
        - If lst is None or empty, returns an empty list
        - If target_keys is None, treats it as an empty collection
        - If no target key is found, returns an empty list
        """
        if lst is None or len(lst) == 0:
            return []

        result: list[Any] = []
        found = False

        if target_keys is None:
            target_keys = set()
        elif isinstance(target_keys, str):
            target_keys = {target_keys}
        else:
            try:
                target_keys = set(target_keys)
            except (TypeError, ValueError):
                target_keys = {target_keys}

        for item in lst:
            if found:
                if isinstance(item, str):
                    break
                result.append(item)
            elif item in target_keys:
                found = True

        return result

    @staticmethod
    def _parse_generic_command(args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
        """Parse command arguments without a specific rule."""
        generic: dict[str, Any] = {}

        # First parse flags so we can remove them from positional slice
        consumed: set[int] = set()
        for i, token in enumerate(args):
            if isinstance(token, str) and token.startswith("-"):
                flag = token.lstrip("-")
                values = BaseHandler._extract_args_by_str(args[i:], token)
                generic[flag] = values if len(values) > 1 else (values[0] if values else True)
                # Mark consumed indices (flag itself plus its values)
                consumed.add(i)
                for j in range(1, len(values) + 1):
                    if i + j < len(args):
                        consumed.add(i + j)

        # Remaining tokens are considered positional
        positional_tokens = [tok for idx_, tok in enumerate(args) if idx_ not in consumed]
        generic["args"] = positional_tokens

        # Merge with kwargs; kwargs has priority
        generic.update(kwargs)
        return generic

    @staticmethod
    def _parse_rule_based_command(
        rule: dict[str, Any], args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Parse command arguments according to a specific rule."""
        result: dict[str, Any] = {}
        arg_list: list[Any] = [x for x in list(args) if x != {} and x is not None]

        # Parse positional arguments
        result.update(BaseHandler._parse_positional_args(rule, arg_list))

        # 记录解析选项标志前的args
        orig_args = result.get("args", [])

        # Parse option flags
        option_result = BaseHandler._parse_option_flags(rule, arg_list)
        result.update(option_result)

        # 如果有解析出选项标志, 并且存在args字段, 则清理args中的选项标志及其值
        if option_result and "args" in result and orig_args:
            # 获取所有选项标志
            option_flags = rule.get("options", {}).keys()
            # 清理args中的选项标志及其值
            cleaned_args = []
            skip_count = 0

            for i, item in enumerate(orig_args):
                if skip_count > 0:
                    skip_count -= 1
                    continue

                # 如果当前项是选项标志, 跳过它及其值
                if item in option_flags:
                    # 获取这个选项后面的值的数量
                    values = BaseHandler._extract_args_by_str(orig_args[i:], item)
                    skip_count = len(values)
                    continue

                cleaned_args.append(item)

            # 更新args字段
            if cleaned_args:
                result["args"] = cleaned_args
            else:
                # 如果清理后args为空, 则移除args字段
                result.pop("args", None)

        # kwargs take precedence over everything parsed from *args*
        result.update(kwargs)
        return result

    @staticmethod
    def _parse_positional_args(rule: dict[str, Any], arg_list: list[Any]) -> dict[str, Any]:
        """Parse positional arguments according to rule."""
        result: dict[str, Any] = {}
        idx = 0

        for name in rule.get("positional", []):
            is_variadic = name.endswith("*")
            clean_name = name.rstrip("*")

            if is_variadic:
                # Consume tokens until next recognised option flag (if any)
                stop_idx = len(arg_list)
                for flag in rule.get("options", {}):
                    if flag in arg_list[idx:]:
                        candidate = arg_list.index(flag, idx)
                        stop_idx = min(stop_idx, candidate)

                result[clean_name] = arg_list[idx:stop_idx]
                idx = stop_idx
                continue

            if idx < len(arg_list):
                result[clean_name] = arg_list[idx]
                idx += 1

        # Store unconsumed positional tokens under "args"
        if idx < len(arg_list):
            result.setdefault("args", []).extend(arg_list[idx:])

        return result

    @staticmethod
    def _parse_option_flags(rule: dict[str, Any], arg_list: list[Any]) -> dict[str, Any]:
        """Parse option flags according to rule."""
        result: dict[str, Any] = {}

        for flag, name in rule.get("options", {}).items():
            if flag in arg_list:
                values = BaseHandler._extract_args_by_str(arg_list, flag)
                if name.endswith("*"):
                    result[name.rstrip("*")] = values
                else:
                    if values:
                        result[name] = values[0] if len(values) == 1 else values

        return result

    # ------------------------------------------------------------------
    # Universal command-line like argument parser
    # ------------------------------------------------------------------
    def parse_command(self, func_name: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Parse *args* / *kwargs* of an OpenSeesPy *func_name* call into a
        dictionary according to :pyattr:`_COMMAND_RULES`.

        The method follows *Tcl-style* rules that OpenSeesPy adopts:
        1.  The command name determines a fixed ordered set of *positional*
            arguments followed by an arbitrary remainder.  A name ending in
            ``*`` in :pyattr:`_COMMAND_RULES` absorbs *all remaining* tokens
            into a list.
        2.  *Flag*-style options (e.g. ``'-mass'``) are extracted together with
            their subsequent numeric values until the next string token is met.
        3.  Any *kwargs* supplied by the caller override values parsed from
            *args*.

        If the command does not appear in :pyattr:`_COMMAND_RULES` we still try
        to extract something meaningful by applying a few heuristics that
        reflect common OpenSeesPy conventions.  We *do not* attempt to be
        perfect, just sufficiently useful for most handlers.
        """
        kwargs = dict(kwargs or {})  # copy to avoid mutating caller data
        rule = self._COMMAND_RULES.get(func_name)

        # If we have no dedicated rule, use generic parsing
        if rule is None:
            return self._parse_generic_command(args, kwargs)

        # Otherwise use rule-based parsing
        return self._parse_rule_based_command(rule, args, kwargs)

    # Convenience helper so that concrete handlers can do::
    #     parsed = self._parse(func_name, *args, **kwargs)
    def _parse(self, func_name: str, *args, **kwargs):
        return self.parse_command(func_name, *args, *kwargs)
