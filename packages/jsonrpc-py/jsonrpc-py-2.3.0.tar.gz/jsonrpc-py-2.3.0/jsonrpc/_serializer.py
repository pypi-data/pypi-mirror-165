# Pure zero-dependency JSON-RPC 2.0 implementation.
# Copyright © 2022 Andrew Malchuk. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABCMeta, abstractmethod
from functools import cached_property
from io import BytesIO
from json import JSONDecoder, JSONEncoder
from pickle import HIGHEST_PROTOCOL, Pickler, Unpickler
from typing import Any, ClassVar, Final

from ._errors import Error, ErrorEnum

__all__: Final[list[str]] = ["JSONSerializer", "PickleSerializer"]

# Eliminate a whitespaces to get the most compact JSON representation:
_JSON_COMPACT_SEPARATORS: Final[tuple[str, str]] = "\u002c", "\u003a"

# Ensure to output JSON as a strict JavaScript subset:
_JSON_ESCAPE_TABLE: Final[dict[int, str]] = {
    0x2028: "\\u2028",
    0x2029: "\\u2029"
}


class BaseSerializer(metaclass=ABCMeta):
    __slots__: tuple[str, ...] = ()

    @abstractmethod
    def serialize(self, obj: Any, /) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, obj: bytes, /) -> Any:
        raise NotImplementedError


class JSONSerializer(BaseSerializer):
    """
    Simple class for JSON serialization and deserialization.
    """
    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__}()>"

    @cached_property
    def _encoder(self) -> JSONEncoder:
        """
        Returns the :py:class:`json.JSONEncoder` object for the serialization.
        """
        return JSONEncoder(ensure_ascii=False, separators=_JSON_COMPACT_SEPARATORS)

    @cached_property
    def _decoder(self) -> JSONDecoder:
        """
        Returns the :py:class:`json.JSONDecoder` object for the deserialization.
        """
        return JSONDecoder(object_hook=None, object_pairs_hook=None)

    def serialize(self, obj: Any, /) -> bytes:
        """
        Returns the JSON representation of a value.

        :param obj: An any type of object that must be JSON serializable.
        :raises jsonrpc.Error: If any exception has occurred due the serialization or/and encoding to :py:class:`bytes`.
        :returns: The :py:class:`bytes` object containing the serialized Python data structure.
        """
        try:
            return self._encoder.encode(obj).translate(_JSON_ESCAPE_TABLE).encode("utf-8", "surrogatepass")
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to serialize object to JSON") from exc

    def deserialize(self, obj: bytes, /) -> Any:
        """
        Returns the value encoded in JSON in appropriate Python type.

        :param obj: The :py:class:`bytes` object containing the serialized JSON document.
        :raises jsonrpc.Error: If any exception has occurred due the deserialization or/and decoding from :py:class:`bytes`.
        :returns: An any type of object containing the deserialized Python data structure.
        """
        try:
            return self._decoder.decode(obj.decode("utf-8", "surrogatepass"))
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to deserialize object from JSON") from exc


class PickleSerializer(BaseSerializer):
    """
    Simple class for the "Pickling" and "Unpickling" Python objects.
    """
    __slots__: tuple[str, ...] = ()

    #: Pickle protocol version used for the serialization.
    #: Defaults to :py:data:`pickle.HIGHEST_PROTOCOL`.
    PROTOCOL_VERSION: ClassVar[int] = HIGHEST_PROTOCOL

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__}()>"

    def serialize(self, obj: Any, /) -> bytes:
        """
        Returns the pickled representation of a value.

        :param obj: An any type of object that must be serializable.
        :raises jsonrpc.Error: If exception has occurred due the pickling.
        :returns: The :py:class:`bytes` object containing the pickled object.
        """
        try:
            with BytesIO() as raw_buffer:
                Pickler(raw_buffer, self.PROTOCOL_VERSION).dump(obj)
                return raw_buffer.getvalue()
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to serialize object") from exc

    def deserialize(self, obj: bytes, /) -> Any:
        """
        Returns the unpickled representation of a value.

        :param obj: The :py:class:`bytes` object containing the pickled object.
        :raises jsonrpc.Error: If exception has occurred due the unpickling.
        :returns: An any type of object containing the deserialized Python data structure.
        """
        try:
            with BytesIO(obj) as raw_buffer:
                return Unpickler(raw_buffer).load()
        except Exception as exc:
            raise Error(code=ErrorEnum.PARSE_ERROR, message="Failed to deserialize object") from exc
