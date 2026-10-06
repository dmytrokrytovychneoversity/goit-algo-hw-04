"""Recursively copy files into folders named after their extensions."""

import argparse
import shutil
import sys
from pathlib import Path


def unique_path(path: Path) -> Path:
    """Add a numbered suffix when a destination name already exists."""
    candidate = path
    number = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(f"{path.stem}_{number}{path.suffix}")
        number += 1
    return candidate


def copy_files(source: Path, destination: Path) -> tuple[int, int]:
    """Walk directories recursively and return copied and failed counts."""
    copied = failed = 0
    try:
        entries = sorted(source.iterdir())
    except OSError as error:
        print(f"Cannot read {source}: {error}", file=sys.stderr)
        return 0, 1

    for entry in entries:
        try:
            if entry.is_symlink():
                print(f"Skipping symbolic link: {entry}")
                continue
            if entry.resolve() == destination:
                continue
            if entry.is_dir():
                nested_copied, nested_failed = copy_files(entry, destination)
                copied += nested_copied
                failed += nested_failed
            elif entry.is_file():
                extension = entry.suffix.lstrip(".").lower() or "no_extension"
                folder = destination / extension
                folder.mkdir(parents=True, exist_ok=True)
                target = unique_path(folder / entry.name)
                shutil.copy2(entry, target)
                copied += 1
        except OSError as error:
            print(f"Cannot process {entry}: {error}", file=sys.stderr)
            failed += 1

    return copied, failed


def main() -> int:
    """Parse paths and organize the source files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source directory")
    parser.add_argument("destination", nargs="?", type=Path, default=Path("dist"))
    args = parser.parse_args()
    try:
        source = args.source.resolve()
        destination = args.destination.resolve()
        if not source.is_dir():
            parser.error("source must be an existing directory")
        if source == destination:
            parser.error("source and destination must be different directories")
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Cannot prepare directories: {error}", file=sys.stderr)
        return 1

    copied, failed = copy_files(source, destination)
    print(f"Copied: {copied}. Errors: {failed}. Destination: {destination}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
