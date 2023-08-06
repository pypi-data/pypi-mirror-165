from typing import Any, Union, Type, Callable
import hashlib
from pathlib import Path
import io
from io import FileIO, BytesIO
import tarfile

def is_file_like(obj:Any):
    return (
        isinstance(obj, io.TextIOBase)
        or isinstance(obj, io.BufferedIOBase)
        or isinstance(obj, io.RawIOBase)
        or isinstance(obj, io.IOBase)
        or issubclass(type(obj), io.TextIOBase)
        or issubclass(type(obj), io.BufferedIOBase)
        or issubclass(type(obj), io.RawIOBase)
        or issubclass(type(obj), io.IOBase)
    )


def hashfile(file: Union[str, Path, FileIO], alg: Type[Callable] = None) -> str:
    """Provide a path or file and get a hash hex string back

    Args:
        file (Union[str, Path, FileIO]): A path or file like object
        alg (Type[hashlib._Hash], optional): The hashing alg to create the hash of the file. Must be a hashlib func compatibel callable. \
            Defaults to hashlib.sha256.

    Returns:
        str: A hex str representing the hash of the file
    """
    # source: https://www.geeksforgeeks.org/compare-two-files-using-hashing-in-python/
    if alg == None:
        alg = hashlib.sha256

    # A arbitrary (but fixed) buffer
    # size (change accordingly)
    # 65536 = 65536 bytes = 64 kilobytes
    BUF_SIZE = 65536

    # Initializing the hash method
    hash_: hashlib._Hash = alg()
    seek_pos: int = None
    if is_file_like(file):
        seek_pos = file.tell()
        file.seek(0)
        f = file
    else:
        f = open(file, "rb")
    while True:

        # reading data = BUF_SIZE from
        # the file and saving it in a
        # variable
        data = f.read(BUF_SIZE)

        # True if eof = 1
        if not data:
            break

        # Passing that data to that sh256 hash
        # function (updating the function with
        # that data)
        hash_.update(data)

    if seek_pos:
        # we had an opened file obj. lets restore it to the old state
        file.seek(seek_pos)
    else:
        # we created a local file obj based on a path. lets close it
        f.close()

    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return hash_.hexdigest()


def create_tar_stream(file_path:Union[str,Path]=None,file_obj:FileIO=None,file_obj_name:str="file") -> BytesIO:
    if not file_path and not file_obj:
        raise ValueError("No source file provided.")
    if file_path and file_obj:
        raise ValueError("Expected `file_path` or `file_obj`. Got both.")
    pw_tarstream = BytesIO()
    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
    if file_path:
        if isinstance(file_path,str):
            file_path = Path(file_path)
        file_obj = open(file_path, 'r').read()
    old_state = file_obj.tell()
    file_obj.seek(0)
    tarinfo = tarfile.TarInfo(name=file_path.name if file_path else file_obj_name)
    # tarinfo.mode = 0600
    pw_tar.gettarinfo(fileobj=file_obj)
    pw_tar.addfile(tarinfo, file_obj.read())
    pw_tar.close()
    pw_tarstream.seek(0)
    # revert cursor to inital state
    file_obj.seek(old_state)
    return pw_tarstream