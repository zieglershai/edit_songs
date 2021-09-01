# This file is the Python type hints stub file for the sip extension module.
#
# Copyright (c) 2016 Riverbank Computing Limited <info@riverbankcomputing.com>
#
# This file is part of SIP.
#
# This copy of SIP is licensed for use under the terms of the SIP License
# Agreement.  See the file LICENSE for more details.
#
# This copy of SIP may also used under the terms of the GNU General Public
# License v2 or v3 as published by the Free Software Foundation which can be
# found in the files LICENSE-GPL2 and LICENSE-GPL3 included in this package.
#
# SIP is supplied WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


from typing import overload, Sequence, Union


# Constants.
SIP_VERSION = ...       # type: int
SIP_VERSION_STR = ...   # type: str


# The bases for SIP generated types.
class wrappertype: ...
class simplewrapper: ...
class wrapper(simplewrapper): ...


# PEP 484 has no explicit support for the buffer protocol so we just name types
# we know that implement it.
Buffer = Union['array', 'voidptr', str, bytes, bytearray]


# The array type.
array = Sequence


# The voidptr type.
class voidptr:

    def __init__(addr: Union[int, Buffer], size: int = -1, writeable: bool = True) -> None: ...

    def __int__(self) -> int: ...

    @overload
    def __getitem__(self, i: int) -> bytes: ...

    @overload
    def __getitem__(self, s: slice) -> 'voidptr': ...

    def __hex__(self) -> str: ...

    def __len__(self) -> int: ...

    def __setitem__(self, i: Union[int, slice], v: Buffer) -> None: ...

    def asarray(self, size: int = -1) -> array: ...

    # Python doesn't expose the capsule type.
    #def ascapsule(self) -> capsule: ...

    def asstring(self, size: int = -1) -> bytes: ...

    def getsize(self) -> int: ...

    def getwriteable(self) -> bool: ...

    def setsize(self, size: int) -> None: ...

    def setwriteable(self, bool: bool) -> None: ...


# Remaining functions.
def cast(obj: simplewrapper, type: wrappertype) -> simplewrapper: ...
def delete(obj: simplewrapper) -> None: ...
def dump(obj: simplewrapper) -> None: ...
def enableautoconversion(type: wrappertype, enable: bool) -> bool: ...
def getapi(name: str) -> int: ...
def isdeleted(obj: simplewrapper) -> bool: ...
def ispycreated(obj: simplewrapper) -> bool: ...
def ispyowned(obj: simplewrapper) -> bool: ...
def setapi(name: str, version: int) -> None: ...
def setdeleted(obj: simplewrapper) -> None: ...
def setdestroyonexit(destroy: bool) -> None: ...
def settracemask(mask: int) -> None: ...
def transferback(obj: wrapper) -> None: ...
def transferto(obj: wrapper, owner: wrapper) -> None: ...
def unwrapinstance(obj: simplewrapper) -> None: ...
def wrapinstance(addr: int, type: wrappertype) -> simplewrapper: ...
