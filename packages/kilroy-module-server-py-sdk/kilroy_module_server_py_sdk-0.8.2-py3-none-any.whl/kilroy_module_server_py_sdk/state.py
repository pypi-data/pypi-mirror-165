from abc import ABC

from kilroy_module_py_shared import SerializableModel


class SerializableState(SerializableModel, ABC):
    class Config:
        allow_mutation = True
