"""Small, dependency-free loader for a project's docs/loom.yaml.

The project configuration is deliberately a restricted YAML subset: mappings,
lists, scalars and comments.  Keeping the parser here makes the shipped gates
portable without adding a dependency to initialized projects.
"""
from pathlib import Path
import re

SHIPPED_SCRIPTS_VERSION = "0.16.0"

DECISION_MODES = {"delegated", "recommend", "confirm", "record-only"}
EVIDENCE_LEVELS = {"none", "reasoned", "reported", "observed", "measured"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}

CHANGE_STATUSES = {
    "captured", "triaged", "accepted", "in-progress", "applied",
    "rejected", "superseded",
}
CHANGE_SOURCES = {"human", "customer", "implementation", "external", "unknown"}
CHANGE_CONFIDENCE = {"confirmed", "reported", "hypothesis"}
CHANGE_CLASSIFICATIONS = {
    "additive", "forgotten-requirement", "fact-correction", "customer-change",
    "hypothesis", "rule-change", "decision-conflict", "roadmap-idea",
}


class ConfigError(RuntimeError):
    pass


def _scalar(value):
    value = value.strip()
    if not value:
        return None
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(x) for x in value[1:-1].split(",") if x.strip()]
    if (value.startswith("\"") and value.endswith("\"")) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def load(path=None):
    path = Path(path or "docs/loom.yaml")
    if not path.is_file():
        raise ConfigError(f"configuration target does not exist: {path}")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ConfigError(f"configuration target is not readable: {path}: {exc}") from exc
    root = {}
    stack = [(-1, root)]
    for number, raw in enumerate(lines, 1):
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        content = line.strip()
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if content.startswith("- "):
            if not isinstance(parent, list):
                raise ConfigError(f"invalid list at {path}:{number}")
            parent.append(_scalar(content[2:]))
            continue
        if ":" not in content:
            raise ConfigError(f"invalid YAML line at {path}:{number}")
        key, value = content.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key:
            raise ConfigError(f"empty key at {path}:{number}")
        if value:
            parent[key] = _scalar(value)
        else:
            # A following indented '- ' turns this into a list; otherwise map.
            next_lines = [x for x in lines[number:] if x.split("#", 1)[0].strip()]
            is_list = bool(next_lines and len(next_lines[0]) - len(next_lines[0].lstrip()) > indent and next_lines[0].strip().startswith("- "))
            child = [] if is_list else {}
            parent[key] = child
            stack.append((indent, child))
    return root


def project_config(path=None):
    config_path = Path(path or "docs/loom.yaml")
    config = load(config_path)
    base = config_path.parent.parent if config_path.parent.name == "docs" else config_path.parent
    return config, base


def target(config, name, default):
    value = config.get("paths", {}).get(name, default)
    return Path(value)


def require_targets(targets):
    errors = []
    for target_path in targets:
        path = Path(target_path)
        if not path.exists():
            errors.append(f"target does not exist: {path}")
        elif not path.is_file() and not path.is_dir():
            errors.append(f"target is neither file nor directory: {path}")
        elif path.is_file():
            try:
                path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"target is not readable: {path}: {exc}")
    return errors


def usage(name, synopsis, detail):
    return f"Usage: {name} {synopsis}\n\n{detail}\n"
