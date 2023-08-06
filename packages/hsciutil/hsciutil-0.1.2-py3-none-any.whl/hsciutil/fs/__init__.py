import glob
import itertools
from pathlib import Path
from typing import Iterator


def recurse_directories(input_paths: Iterator[Path]) -> Iterator[Path]:
    """Expand a list of paths, recursively returning all entries in directories found

    Parameters
    ----------
    input_paths: Iterator[Path]
        The paths to recurse

    Returns
    -------
    Iterator[str]:
        A flattened iterator of files under the input paths

    """
    return itertools.chain.from_iterable(
        map(lambda path: path.rglob("*") if path.is_dir() else [path], input_paths)
    )


def expand_globs(input_globs: Iterator[str], recurse=False) -> Iterator[Path]:
    """Recursively expand input globs

    Parameters
    ----------
    input_globs: Iterator[str]
        The globs to expand
    recurse: bool, default=False
        Whether to recursively expand all directories matched by the glob

    Returns
    -------
    Iterator[str]:
        A flattened iterator of the expanded globs

    """
    ret: Iterator[Path] = map(Path,itertools.chain.from_iterable(
        map(lambda glob_pattern: glob.iglob(str(Path(glob_pattern).expanduser()), recursive=True), input_globs)
    ))
    if recurse:
        seen: set[Path] = set()

        def filter_seen(path: Path):
            if path in seen:
                return False
            seen.add(path)
            return True
        ret = filter(filter_seen, recurse_directories(ret))
    return ret


__all__ = ["expand_globs", "recurse_directories"]
