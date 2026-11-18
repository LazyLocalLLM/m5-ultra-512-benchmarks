"""Recompute a finding's Markdown summary from rows.csv and runs.csv."""

import argparse
import csv
import itertools
import json
from pathlib import Path
import statistics
import sys


COLUMNS = ["run id", "started", "engine", "engine version", "settings", "test",
           "content", "prompt tokens", "users", "n", "writing tok/s", "total tok/s",
           "first token seconds"]


def read_csv(folder, name):
    with (Path(folder) / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def measure(rows, field, decimals):
    values = [float(row[field]) for row in rows if row[field] != ""]
    if not values:
        return ""
    return "{:.{p}f} ({:.{p}f} to {:.{p}f})".format(
        statistics.median(values), min(values), max(values), p=decimals)


def markdown(value):
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "<br>").replace("\r", "<br>").replace("\n", "<br>")


def table_line(values):
    return "| " + " | ".join(markdown(value) for value in values) + " |"


def group_order(key):
    test, content, prompt, users = key
    return test, content, float(prompt) if prompt else 0, float(users) if users else 0


def summarize(folder):
    """Return Markdown lines; missing identity items count as different answers."""
    rows = read_csv(folder, "rows.csv")
    runs = {run["run_id"]: run for run in read_csv(folder, "runs.csv")}
    groups = {}
    identities = {}
    for row in rows:
        if row["ok"] != "1" or row["warmup"] == "1" or row["test"] == "server_start":
            continue
        run_id = row["run_id"]
        if run_id not in runs:
            raise ValueError("A row refers to an unknown run: " + run_id)
        if row["test"] == "identity":
            items = identities.setdefault(run_id, {})
            extra = json.loads(row["extra"] or "{}")
            if "item" in extra:
                items.setdefault(extra["item"], set()).add(extra["sha256"])
        else:
            key = tuple(row[field] for field in ("test", "content", "prompt_target", "users"))
            groups.setdefault(run_id, {}).setdefault(key, []).append(row)
    run_order = sorted(runs, key=lambda run_id: (runs[run_id]["started"], run_id))
    lines = [table_line(COLUMNS), table_line(["---"] * len(COLUMNS))]
    for run_id in run_order:
        run = runs[run_id]
        for key in sorted(groups.get(run_id, {}), key=group_order):
            samples = groups[run_id][key]
            cells = [run_id, run["started"], run["engine"], run["engine_version"], run["settings"]]
            cells.extend(key)
            cells.extend([len(samples), measure(samples, "write_tps", 1),
                          measure(samples, "total_tps", 1), measure(samples, "first_s", 2)])
            lines.append(table_line(cells))
    if identities:
        lines.extend(["", "## Identity", ""])
        for left, right in itertools.combinations([run_id for run_id in run_order if run_id in identities], 2):
            left_items, right_items = identities[left], identities[right]
            items = set(left_items) | set(right_items)
            same = sum(left_items.get(item) == right_items.get(item) for item in items)
            lines.append("{} ({}) against {} ({}). {} of {} prompts gave the same answers.".format(
                left, runs[left]["engine"], right, runs[right]["engine"], same, len(items)))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    args = parser.parse_args(argv)
    try:
        lines = summarize(args.folder)
    except FileNotFoundError as error:
        print("Missing file: " + Path(error.filename).name)
        return 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Refused. " + " ".join(str(error).splitlines()))
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
