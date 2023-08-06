from pathlib import Path
import tracemalloc
import os, sys

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))
from DZDutils.files import (
    create_tar_stream_of_file,
    generate_big_random_bin_file,
    create_tmp_tar_archive_of_file,
)


file = Path("/tmp/big_file")
target_file = Path("/tmp/big_file.tar")
size_bytes = 500000000
if not file.exists() or not file.stat().st_size >= size_bytes:
    generate_big_random_bin_file(file, size_bytes)
target_file.unlink(missing_ok=True)


def stream_as_tar():
    with open(file, "rb") as src:
        with create_tar_stream_of_file(file_obj=src) as src_tar:
            # with open(file, "rb") as src:
            with open(target_file, "wb") as trg:
                while chunk := src_tar.read(1024):
                    trg.write(chunk)


def stream_from_tmp_tar():
    with open(file, "rb") as src:
        with create_tmp_tar_archive_of_file(file_obj=src) as src_tar:
            # with open(file, "rb") as src:
            with open(target_file, "wb") as trg:
                while chunk := src_tar.read(1024):
                    trg.write(chunk)


# starting the monitoring
tracemalloc.start()
stream_from_tmp_tar()
# displaying the memory
print("Wanted size:", size_bytes / (1024 * 1024), "MB")
print("Mem used:", tracemalloc.get_traced_memory()[1] / (1024 * 1024), "MB")
assert (
    file.stat().st_size == target_file.stat().st_size
), f"Size from src and trg differs: {file.stat().st_size} =! {target_file.stat().st_size}"
print(
    f"File sizes: {file.stat().st_size/ (1024 * 1024)} == {target_file.stat().st_size/ (1024 * 1024)}"
)
# stopping the library
tracemalloc.stop()
