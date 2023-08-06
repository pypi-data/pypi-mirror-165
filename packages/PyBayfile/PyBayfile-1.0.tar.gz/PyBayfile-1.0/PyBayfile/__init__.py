r"""
|:| # PyBayfile
|:| ===========
|:| PyBayfile is a Python module for handling bayfiles
|:| bayfiles is a website that allows users to upload and share files
|:|
|:| exmaple of usage:
|:|     from PyBayfile import Archive
|:|
|:|     # make the archive
|:|     path = './etc/file_to_upload.exe'
|:|     archive: Archive = Archive.make_from_path(path)
|:|
|:|     # print the link of the archive: link is str(archive) or archive.link
|:|     print(f'your file is uploaded to: {archive} and the size is {archive.size} bytes')
"""[1:-1]

# an upgraded version of https://github.com/Vodkarm/pybay

from aiohttp import ClientSession as _ClientSession
from asyncio import run as _run, new_event_loop as _n_event_loop, set_event_loop as _s_event_loop, set_event_loop_policy as _s_event_loop_policy, WindowsSelectorEventLoopPolicy as _WindowsSelectorEventLoopPolicy
from typing import AnyStr as _AnyStr, Any as _Any
from os import name as _name
import tempfile as _tempfile


__title__: str = 'PyBayfile'
__author__: str = 'BlueRed'
__version__: str = '1.0'
__license__: str = 'MIT'
__link__: str = 'https://github.com/CSM-BlueRed/PyBayfile'
__doc__: str = '\n'.join(line[4:] for line in open(__file__).read().splitlines() if line.startswith('|:|'))


# asyncio event loop management
loop = _n_event_loop()
_s_event_loop(loop)
if _name == 'nt':
    _s_event_loop_policy(_WindowsSelectorEventLoopPolicy())



class API:
    r"""
    The Bayfile api to store endpoints
    """

    BASE = 'api.bayfiles.com'
    UPLOAD = '/upload'
    INFOS = '/v2/file/{id}/info'



class Bayfile:
    r"""
    represent a Bayfile with his infos
    """

    __slots__ = (
        'url', 'long_url', 'id',
        'name', 'size', 'api_data'
    )

    def __init__(self, data: dict) -> None:
        r"""
        The constructor to store archive infos by the api returned data
        """
        self.url: str = data['file']['url']['short']
        self.long_url: str = data['file']['url']['full']

        self.id: str = data['file']['metadata']['id']
        self.name: str = data['file']['metadata']['name']

        self.size: int = data['file']['metadata']['size']['bytes']
        self.api_data = data


    @classmethod
    def make_from_path(cls, path: str) -> 'Bayfile':
        r"""
        make a Bayfile with the file path
        """
        files = {'file': open(path, 'rb')}

        async def _upload() -> dict:
            async with _ClientSession() as session:
                async with session.post(f'https://{API.BASE}{API.UPLOAD}', data = files) as resp:
                    return await resp.json()

        coro = _upload()
        result = _run(coro)
        coro.close()
        return cls(data = result['data'])


    @classmethod
    def make_from_text(cls, text: _AnyStr, name: str) -> 'Bayfile':
        r"""
        make a Bayfile with just text
        """
        if not isinstance(text, (str, bytes)):
            raise TypeError('text must be string or bytes')

        path = _tempfile.mkdtemp('py-bayfile')

        if isinstance(text, str):
            text = text.encode('utf-8')

        with open(f'{path}/{name}', 'wb') as file:
            file.write(text)

        return cls.make_from_path(f'{path}/{name}')


    @classmethod
    def from_id(cls, id: str) -> 'Bayfile':
        r"""
        get a Bayfile from his ID
        """
        async def _info() -> dict:
            async with _ClientSession() as session:
                async with session.get(f'https://{API.BASE}{API.INFOS}'.format(id = id)) as resp:
                    return await resp.json()

        coro = _info()
        result = _run(coro)
        coro.close()
        return cls(data = result['data'])


    @classmethod
    def from_url(cls, url: str) -> 'Bayfile':
        r"""
        get a Bayfile from his URL
        """
        id = url.split('https://')[1].split('/')[1].split('?')[0]
        return cls.from_id(id)


    def keys(self):
        yield from (slot for slot in self.__class__.__slots__ if slot != 'api_data')


    def __getitem__(self, name: str) -> _Any:
        return getattr(self, name)


    def __str__(self) -> str:
        return self.url


    def __repr__(self) -> str:
        return f'<Bayfile {self.id!r} {self.size}b>'


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bayfile):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Bayfile):
            return self.id != other.id
        return False


    def __hash__(self) -> int:
        return hash(self.id)


    def __lt__(self, other: object) -> bool:
        if isinstance(other, Bayfile):
            return self.size < other.size
        return False


    def __le__(self, other: object) -> bool:
        if isinstance(other, Bayfile):
            return self.size <= other.size
        return False


    def __gt__(self, other: object) -> bool:
        if isinstance(other, Bayfile):
            return self.size > other.size
        return False


    def __ge__(self, other: object) -> bool:
        if isinstance(other, Bayfile):
            return self.size >= other.size
        return False


    def __bool__(self) -> bool:
        return bool(self.size)


    def __getitem__(self, key: str) -> str:
        return getattr(self, key)



Archive = Bayfile
__all__: tuple = tuple(obj for obj in globals() if obj[0] != '_')


def test(*args):
    r"""
    the test function that create a bayfile for debugging
    """
    import os
    file_path: str = args[0]
    bayfile = Archive.make_from_path(os.path.abspath(file_path))

    os.system('')
    print('Bayfile infos:')
    reset = '\u001b[0m'
    red = '\u001b[38;2;255;0;0m'
    blue = '\u001b[38;2;75;75;255m'
    for name, value in dict(bayfile).items():
        key = name + ':'
        print(
            f'{red}{key[:-1]}{reset}:' + (' ' * (13 - len(key))),
            f'{blue}{value}{reset}'
        )


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        test(*sys.argv[1:])