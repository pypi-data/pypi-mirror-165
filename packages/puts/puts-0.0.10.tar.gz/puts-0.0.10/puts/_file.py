import os
import shlex
import shutil
import subprocess
from multiprocessing import Pool
from pathlib import Path
from typing import List, Tuple, Union


def alternative_file_path(file_path: Union[str, Path]) -> Union[str, Path]:
    """
    To return an alternative path if a file already exists at the supplied path.

    Accepts file_path in the argument as a string or a Path.
    Returns the same type accordingly.
    """
    isPath = True if isinstance(file_path, Path) else False
    file_path: Path = Path(file_path)
    _parent: Path = file_path.parent
    _stem: str = file_path.stem
    _suffix: str = file_path.suffix
    counter = 0
    while file_path.is_file():
        counter += 1
        file_path = _parent / f"{_stem}-{str(counter)}{_suffix}"

    if isPath:
        return file_path
    else:
        return str(file_path)


class MassCopier:
    """
    Multi-processing parallel safe copy operations
    """

    CopyJob = Tuple[str, str]
    verbose = True
    overwrite = False
    large_files = False

    def __init__(self, logger=None):
        self.copy_jobs: List[MassCopier.CopyJob] = []
        self.logger = logger

    def add(self, src: str, dst: str) -> None:
        """Verify and add copy jobs into MassCopier"""
        src = Path(src)
        if not src.exists():
            self.logger.error(f"Source file '{src}' not found.")
            return

        dst = Path(dst).resolve()
        if dst.is_file():
            self.logger.warning(f"Destination path has existing file '{dst}'.")
        elif dst.is_dir():
            dst = dst / src.name
            if dst.is_file():
                dst = str(dst)
                self.logger.warning(f"Destination path has existing file '{dst}'.")

        src = str(src)
        dst = str(dst)
        self.copy_jobs.append((src, dst))

    @staticmethod
    def make_copy(copy_job: CopyJob, logger=None) -> Union[str, CopyJob]:
        """A copy job definition"""
        src, dst = copy_job

        if MassCopier.large_files:
            tmp_dst = str(dst) + ".tmp"
        else:
            tmp_dst = str(dst)

        flags = "-"
        if MassCopier.verbose:
            flags += "v"
        if MassCopier.overwrite:
            flags += "f"
        else:
            flags += "n"

        completed = subprocess.run(
            args=shlex.split(f'cp {flags} "{src}" "{tmp_dst}"'),
            # stdout=subprocess.PIPE,
        )
        failed = True if completed.returncode != 0 else False

        if failed:
            if logger:
                logger.error(f"Failed job: ({src}) -> ({dst})")
            return copy_job
        else:
            # logger.debug(f"Succeeded job: ({src}) -> ({dst})")
            if MassCopier.large_files:
                completed = subprocess.run(
                    args=shlex.split(f'mv {flags} "{tmp_dst}" "{dst}"'),
                    # stdout=subprocess.PIPE,
                )
            return "OK"

    def start(
        self,
        interactive: bool = False,
        verbose: bool = True,
        overwrite: bool = False,
        large_files: bool = False,
    ) -> None:
        """
        Submit copy jobs to multiprocessing pool and start actual copy operations.
        """
        MassCopier.verbose = verbose
        MassCopier.overwrite = overwrite
        MassCopier.large_files = large_files

        if verbose:
            print(f"Number of files to be copied: {len(self.copy_jobs)}")
            if overwrite:
                print("Overwrite Mode")
            else:
                print("Safe Mode (Strictly do not overwrite)")

            if large_files:
                print("Large Files Mode (Prevent incomplete transfer)")
            else:
                print("Regular Files Mode (Do not prevent incomplete transfer)")

            if verbose:
                print("Verbose Mode")

        if interactive:
            _start = str(input("Start to copy (y/n)? ")).strip()
            if _start != "y":
                self.logger.warning("Operation aborted by instruction.")
                return

        pool = Pool()
        result = pool.map(MassCopier.make_copy, self.copy_jobs)
        if verbose:
            print(list(result))


if __name__ == "__main__":
    cp = MassCopier()
    cp.add("...", "...")
    cp.start(1, 1, 0, 1)
