import csv
import sys
import requests
import graphviz
import os

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

    cfg.setdefault("repo", "https://crates.io/api/v1/crates")
    cfg.setdefault("mode", "url")
    cfg.setdefault("output", "deps")
    cfg.setdefault("deep", "3")
    cfg.setdefault("filter", "")

    for key in ("package_name", "version"):
        if not cfg.get(key):
            print(f"Ошибка: параметр '{key}' обязателен")
            sys.exit(1)

    try:
        cfg["deep"] = int(cfg["deep"])
        if cfg["deep"] <= 0:
            raise ValueError
    except ValueError:
        print("Ошибка: deep должен быть положительным целым числом")
        sys.exit(1)

    return cfg


def fetch_dependencies(cfg: dict) -> list[str]:
    base = cfg["repo"].rstrip("/")
    name = cfg["package_name"]
    version = cfg["version"]
    url = f"{base}/{name}/{version}/dependencies"

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса к репозиторию: {e}")
        print(f"URL: {url}")
        sys.exit(1)

    try:
        data = resp.json()
    except ValueError:
        print("Ошибка: сервер вернул невалидный JSON")
        sys.exit(1)

    deps = []
    for item in data.get("dependencies", []):
        crate = item.get("crate_id")
        if crate:
            deps.append(crate)

    return deps


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

    deps = fetch_dependencies(cfg)

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
