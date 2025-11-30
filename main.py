#!/usr/bin/env python3

import argparse
import sys
import os
from utils import (
    read_config_csv,
    validate_config,
    fetch_repo,
    find_package_cargo,
    parse_cargo_toml_for_deps,
    build_dot,
    save_dot_and_png,
)

def main():
    parser = argparse.ArgumentParser(description="Rust dependency visualizer (Cargo)")
    parser.add_argument("-c", "--config", required=True, help="Path to config.csv")
    args = parser.parse_args()

    # === ЭТАП 1: Чтение и вывод параметров ===
    try:
        cfg = read_config_csv(args.config)
    except Exception as e:
        print(f"[ERROR] reading config: {e}", file=sys.stderr)
        sys.exit(2)

    print("\n=== CONFIG PARAMETERS ===")
    for k, v in cfg.items():
        print(f"{k} = {v}")
    print("==========================\n")

    try:
        validate_config(cfg)
    except Exception as e:
        print(f"[ERROR] Config: {e}")
        sys.exit(3)

    # === ЭТАП 2: Работа с репозиторием ===
    try:
        repo_path, cleanup_cb = fetch_repo(cfg["repo"], cfg["mode"], cfg.get("version"))
    except Exception as e:
        print(f"[ERROR] fetch_repo: {e}")
        sys.exit(4)

    try:
        cargo_path = find_package_cargo(repo_path, cfg.get("name"), cfg.get("version"))
    except Exception as e:
        cleanup_cb()
        print(f"[ERROR] find_package_cargo: {e}")
        sys.exit(5)

    try:
        deps = parse_cargo_toml_for_deps(cargo_path)
    except Exception as e:
        cleanup_cb()
        print(f"[ERROR] parse cargo: {e}")
        sys.exit(6)

    print("=== DIRECT DEPENDENCIES ===")
    if deps:
        for d, v in deps.items():
            print(f"- {d}: {v}")
    else:
        print("(no direct dependencies)")
    print("===========================\n")

    # === ЭТАП 3: Граф зависимостей ===
    dot = build_dot(cfg.get("name") or "root", deps)

    out_file = cfg.get("out_file", "outputs/graph.png")
    try:
        save_dot_and_png(dot, out_file)
        print(f"[OK] PNG graph saved: {out_file}")
    except Exception as e:
        print(f"[WARN] PNG generation failed: {e}")
        print("Saving DOT instead.")
        with open(out_file + ".dot", "w", encoding="utf-8") as f:
            f.write(dot)
        print(f"[OK] DOT saved: {out_file}.dot")

    cleanup_cb()


if __name__ == "__main__":
    main()
