from abc import ABC, abstractmethod
from typing import Any, AsyncIterable, Dict, Generic, Tuple, Type, TypeVar

from kilroy_server_py_utils import Categorizable, Observable, classproperty

DataType = TypeVar("DataType")
MetricType = TypeVar("MetricType", bound="Metric")


class Metric(Categorizable, Generic[DataType], ABC):
    _observable: Observable[Tuple[int, DataType]]

    def __init__(self, observable: Observable[Tuple[int, DataType]]) -> None:
        super().__init__()
        self._observable = observable

    @classmethod
    async def build(cls: Type[MetricType], *args, **kwargs) -> MetricType:
        return cls(*args, observable=await Observable.build(), **kwargs)

    @classproperty
    def category(cls) -> str:
        return cls.name

    @classproperty
    @abstractmethod
    def name(cls) -> str:
        pass

    @classproperty
    @abstractmethod
    def label(cls) -> str:
        pass

    @classproperty
    @abstractmethod
    def config(cls) -> Dict[str, Any]:
        pass

    async def report(self, data: DataType, dataset: int = 0) -> None:
        await self._observable.set((dataset, data))

    async def watch(self) -> AsyncIterable[Tuple[int, DataType]]:
        async for dataset_id, data in self._observable.subscribe():
            yield dataset_id, data
