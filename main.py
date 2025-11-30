import csv
import os
import sys
import requests
import graphviz


def read_config(path: str) -> dict:
    try:
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        print(f"Ошибка: не найден файл конфигурации {path}")
        sys.exit(1)

    cfg: dict[str, str] = {}
    for row in rows:
        if len(row) < 2:
            continue
        key, value = row[0].strip(), row[1].strip()
        if not key or key.lower() == "key":
            continue
        cfg[key] = value

    cfg.setdefault("output", "deps")
    cfg.setdefault("deep", "3")
    cfg.setdefault("filter", "")
    cfg.setdefault("mode", "file")

    for key in ("package_name", "repo", "mode", "version"):
        if not cfg.get(key):
            print(f"Ошибка: параметр '{key}' обязателен")
            sys.exit(1)

    if cfg["mode"] not in ("file", "url"):
        print("Ошибка: mode должен быть 'file' или 'url'")
        sys.exit(1)

    try:
        cfg["deep"] = int(cfg["deep"])
        if cfg["deep"] <= 0:
            raise ValueError
    except ValueError:
        print("Ошибка: deep должен быть положительным целым числом")
        sys.exit(1)

    return cfg


def load_lock(cfg: dict) -> str:
    if cfg["mode"] == "file":
        path = cfg["repo"]
        if os.path.isdir(path):
            path = os.path.join(path, "Cargo.lock")
        if not os.path.exists(path):
            print(f"Ошибка: не найден файл {path}")
            sys.exit(1)
        with open(path, encoding="utf-8") as f:
            return f.read()
    else:
        try:
            resp = requests.get(cfg["repo"], timeout=15)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            print(f"Ошибка загрузки по URL: {e}")
            sys.exit(1)


def parse_lock(text: str) -> dict[tuple[str, str], list[str]]:
    result: dict[tuple[str, str], list[str]] = {}

    name = None
    version = None
    deps: list[str] = []
    in_deps = False

    for raw in text.splitlines():
        line = raw.strip()

        if line == "[[package]]":
            if name and version:
                result[(name, version)] = deps
            name, version, deps, in_deps = None, None, [], False
            continue

        if line.startswith("name ="):
            value = line.split("=", 1)[1].strip()
            name = value.strip('"')
            continue

        if line.startswith("version ="):
            value = line.split("=", 1)[1].strip()
            version = value.strip('"')
            continue

        if line.startswith("dependencies = ["):
            in_deps = True
            if line.rstrip().endswith("]"):
                in_deps = False
            continue

        if in_deps:
            if line.startswith("]"):
                in_deps = False
            elif '"' in line:
                dep_full = line.split('"')[1]
                dep_name = dep_full.split()[0]
                deps.append(dep_name)

    if name and version:
        result[(name, version)] = deps

    return result


def build_graph(root: str, deps: list[str], flt: str) -> str:
    flt = flt or ""
    lines = ["digraph G {"]
    for dep in deps:
        if flt and flt not in root and flt not in dep:
            continue
        lines.append(f'"{root}"->"{dep}"')
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    cfg_path = sys.argv[1] if len(sys.argv) > 1 else "config.csv"
    cfg = read_config(cfg_path)

    print("Параметры конфигурации:")
    for k, v in cfg.items():
        print(f"{k} = {v}")

    lock_text = load_lock(cfg)
    all_deps = parse_lock(lock_text)

    key = (cfg["package_name"], cfg["version"])
    if key not in all_deps:
        print("Ошибка: указанная комбинация name+version не найдена в Cargo.lock")
        sys.exit(1)

    deps = all_deps[key]
    print("\nПрямые зависимости пакета:")
    if deps:
        for d in deps:
            print(" -", d)
    else:
        print(" (нет зависимостей)")

    dot_source = build_graph(cfg["package_name"], deps, cfg["filter"])
    graph = graphviz.Source(dot_source, format="png")
    graph.render(filename=cfg["output"], view=True, overwrite_source=True)
    os.remove(cfg["output"])


if __name__ == "__main__":
    main()
