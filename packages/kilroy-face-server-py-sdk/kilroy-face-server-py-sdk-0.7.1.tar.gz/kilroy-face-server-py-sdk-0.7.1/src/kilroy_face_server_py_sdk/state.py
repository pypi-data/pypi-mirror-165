from abc import ABC

from kilroy_face_py_shared import SerializableModel


class SerializableState(SerializableModel, ABC):
    class Config:
        allow_mutation = True
