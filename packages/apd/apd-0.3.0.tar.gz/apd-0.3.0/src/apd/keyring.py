###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Experimental connector the the Linux kernel's keyring API.

Ideally a similar module should be added for macOS/Windows.

See https://man7.org/linux/man-pages/man7/keyutils.7.html
"""
from __future__ import annotations

import ctypes.util
import errno
import os
import re
from collections.abc import MutableMapping
from enum import IntEnum
from pathlib import Path
from typing import Union


class KeyringSpec(IntEnum):
    THREAD = -1
    """This specifies the caller's thread-specific keyring"""
    PROCESS = -2
    """This specifies the caller's process-specific keyring"""
    SESSION = -3
    """This specifies the caller's session-specific keyring"""
    USER = -4
    """This specifies the caller's UID-specific keyring"""
    USER_SESSION = -5
    """This specifies the caller's UID-session keyring"""


defines = {
    "KEYCTL_SEARCH": 10,
    "KEYCTL_READ": 11,
    "KEYCTL_DESCRIBE": 6,
    "KEYCTL_SET_TIMEOUT": 15,
    "KEYCTL_GET_PERSISTENT": 22,
    "KEYCTL_INVALIDATE": 21,
}
KEY_ERROR_NUMBERS = [errno.ENOKEY, errno.EKEYREVOKED, errno.EKEYEXPIRED]


def _load_keyutils():
    # pylint: disable=protected-access
    if hasattr(_load_keyutils, "_keyutils"):
        return _load_keyutils._keyutils
    lib_path = Path(ctypes.util.find_library("keyutils"))
    header_path = lib_path.parent.parent / "include" / "keyutils.h"
    extra_defines = {
        k: int(v, base=0)
        for k, v in re.findall(
            r"#define\s+(\w+)\s+([\-0-9x]+)", header_path.read_text()
        )
    }
    defines.update(extra_defines)
    _load_keyutils._keyutils = ctypes.CDLL(lib_path, use_errno=True)
    return _load_keyutils._keyutils


class KeyutilsError(Exception):
    def __init__(self):
        self.errno = ctypes.get_errno()

    def __str__(self):
        return f"{errno.errorcode[self.errno]}: {os.strerror(self.errno)}"


def keyctl(operation, arg2=None, arg3=None, arg4=None, arg5=None, *, validate=True):
    result = _load_keyutils().keyctl(defines[operation], arg2, arg3, arg4, arg5)
    if validate and result < 0:
        raise KeyutilsError()
    return result


class KeyringItem:
    @classmethod
    def from_name(cls, keyring_id: int, name, *, key_type="user"):
        if isinstance(key_type, str):
            key_type = key_type.encode("utf-8")
        key_id = keyctl("KEYCTL_SEARCH", keyring_id, key_type, name.encode())
        return cls(key_id)

    def __init__(self, key_id):
        self.key_id = key_id

    def __repr__(self):
        return f"{self.__class__.__name__}({self.key_id})"

    @property
    def type(self) -> bytes:
        return self.get_description()["type"]

    @property
    def uid(self) -> int:
        return self.get_description()["uid"]

    @property
    def gid(self) -> int:
        return self.get_description()["gid"]

    @property
    def permissions_mask(self) -> int:
        return self.get_description()["permissions_mask"]

    @property
    def name(self) -> bytes:
        return self.get_description()["name"]

    def get_description(self):
        result = keyctl("KEYCTL_DESCRIBE", self.key_id, None, 0)
        while True:
            buffer = ctypes.create_string_buffer(result)
            result = keyctl(
                "KEYCTL_DESCRIBE", self.key_id, buffer, ctypes.sizeof(buffer)
            )
            if ctypes.sizeof(buffer) >= result:
                break
        type_name, uid, gid, permissions_mask, *_, name = buffer.value.split(b";")
        return dict(
            type=type_name.decode(),
            uid=int(uid),
            gid=int(gid),
            permissions_mask=int(permissions_mask, base=16),
            name=name.decode(),
        )

    def get_value(self):
        result = keyctl("KEYCTL_READ", self.key_id, None, 0)
        while True:
            buffer = ctypes.create_string_buffer(result)
            result = keyctl("KEYCTL_READ", self.key_id, buffer, ctypes.sizeof(buffer))
            if ctypes.sizeof(buffer) >= result:
                return buffer.value.decode()

    def set_timeout(self, timeout: int):
        """Tell the kernel to destroy the key after timeout seconds."""
        keyctl("KEYCTL_SET_TIMEOUT", self.key_id, timeout)

    def clear_timeout(self):
        """Tell the kernel to keep the key permanently."""
        keyctl("KEYCTL_SET_TIMEOUT", self.key_id, 0)


class LinuxKeyring(MutableMapping):
    @classmethod
    def persistent_keyring(cls, keyring_id: int = KeyringSpec.PROCESS, **kwargs):
        keyring_id = keyctl("KEYCTL_GET_PERSISTENT", -1, keyring_id)
        return cls(keyring_id, **kwargs)

    def __init__(self, keyring_id: int, *, default_key_type="user"):
        self.keyring_id = keyring_id
        self.default_key_type = default_key_type

    def __get_keyring_item(self, key: Union[int, str, KeyringItem, tuple[str, type]]):
        if isinstance(key, KeyringItem):
            item = key
        elif isinstance(key, int):
            item = KeyringItem(key)
        else:
            key, key_type = (
                (key, self.default_key_type) if isinstance(key, str) else key
            )
            item = KeyringItem.from_name(self.keyring_id, key, key_type=key_type)
        return item

    def __getitem__(self, key: Union[int, str, KeyringItem, tuple[str, type]]):
        try:
            return self.__get_keyring_item(key).get_value()
        except KeyutilsError as e:
            if e.errno in KEY_ERROR_NUMBERS:
                raise KeyError(key) from None
            raise

    def __setitem__(self, key: Union[str, tuple[str, type]], value: str):
        key, key_type = (key, self.default_key_type) if isinstance(key, str) else key
        key = key.encode("utf-8")
        value = value.encode("utf-8")
        key_type = key_type.encode("utf-8")
        result = _load_keyutils().add_key(
            key_type, key, value, len(value), self.keyring_id
        )
        if result <= 0:
            raise KeyutilsError()
        return result

    def __delitem__(self, key: Union[int, str, KeyringItem, tuple[str, type]]):
        item = self.__get_keyring_item(key)
        keyctl("KEYCTL_INVALIDATE", item.key_id)
        try:
            item.get_description()
        except KeyutilsError as e:
            if e.errno in KEY_ERROR_NUMBERS:
                return
            raise
        raise RuntimeError()

    def __iter__(self):
        for key_metadata in self.keys_with_metadata():
            yield key_metadata

    def __len__(self):
        return sum(1 for _ in self.keys_with_metadata())

    def keys_with_metadata(self):
        try:
            result = keyctl("KEYCTL_READ", self.keyring_id, None, 0)
        except KeyutilsError as e:
            if e.errno in KEY_ERROR_NUMBERS:
                raise
            n_entries = 0
        else:
            n_entries = result // ctypes.sizeof(ctypes.c_int32)

        while True:
            buffer = (ctypes.c_int32 * n_entries)()
            if n_entries == 0:
                break
            result = keyctl(
                "KEYCTL_READ", self.keyring_id, buffer, ctypes.sizeof(buffer)
            )
            if ctypes.sizeof(buffer) >= result:
                break
            n_entries = result // ctypes.sizeof(ctypes.c_int32)
        for item in map(KeyringItem, buffer):
            try:
                if item.key_id == 0 or item.type == "keyring":
                    continue
            except KeyutilsError as e:
                if e.errno in KEY_ERROR_NUMBERS:
                    continue
                raise
            yield item
