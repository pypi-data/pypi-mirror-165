import abc
from typing import Generic, Iterable, List, Optional, TypeVar, Union

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import count
from starlette import status

from .exception import LOSException
from .schemas import Pageable, Sort, PageResponse

T = TypeVar("T")
ID = TypeVar("ID")


class IRepository(Generic[T, ID]):

    @abc.abstractmethod
    async def count(self, *args, **kwargs) -> int:
        ...

    @abc.abstractmethod
    async def delete(self, entity: T) -> int:
        ...

    @abc.abstractmethod
    async def delete_all(self, entities: Iterable[T]) -> None:
        ...

    @abc.abstractmethod
    async def delete_all_by_id_in_batch(self, integers: Iterable[ID]) -> None:
        ...

    @abc.abstractmethod
    async def delete_all_in_batch(self, entities: Iterable[T]) -> None:
        ...

    @abc.abstractmethod
    async def delete_by_id(self, integer: ID) -> bool:
        ...

    @abc.abstractmethod
    async def exists(self, *args, **kwargs) -> bool:
        ...

    @abc.abstractmethod
    async def exists_by_id(self, integer: ID) -> bool:
        ...

    @abc.abstractmethod
    async def find_all(self, pageable: Optional[Pageable], sort: Optional[Sort]) -> Union[List[T], PageResponse[T]]:
        ...

    @abc.abstractmethod
    async def find_all_by_id(self, integers: Iterable[ID]) -> List[T]:
        ...

    @abc.abstractmethod
    async def find_by_id(self, integer: ID) -> Optional[T]:
        ...

    @abc.abstractmethod
    async def find_one(self, *args, **kwargs) -> Optional[T]:
        ...

    @abc.abstractmethod
    async def get_by_id(self, integer: ID) -> T:
        ...

    @abc.abstractmethod
    async def save(self, entity: T) -> T:
        ...

    @abc.abstractmethod
    async def save_all(self, entities: Iterable[T]) -> List[T]:
        ...

    @abc.abstractmethod
    async def save_and_flush(self, entity: T) -> T:
        ...

    @abc.abstractmethod
    async def save_all_and_flush(self, entities: Iterable[T]) -> List[T]:
        ...


class Repository(IRepository[T, ID]):
    type_ = T
    id_ = ID

    async def delete(self, entity: T) -> int:
        rs = await self.session.delete(entity)
        logger.info(f"sqlalchemy delete: {rs}")
        return rs

    async def delete_all(self, entities: Iterable[T]) -> None:
        await self.session.delete(entities)

    async def delete_all_by_id_in_batch(self, integers: Iterable[ID]) -> None:
        self.session.query(self.type_.id.in_(integers)).delete()

    async def delete_all_in_batch(self, entities: Iterable[T]) -> None:
        self.session.delete(entities)

    async def delete_by_id(self, id: ID) -> bool:
        self.session.query(self.type_.id == id).delete()

    async def exists(self, *args, **kwargs) -> bool:
        ...

    async def exists_by_id(self, integer: ID) -> bool:
        return bool(self.session.query(1).where(self.type_.id == integer).first())

    async def find_all(self, pageable: Pageable = None, sort: Sort = None, *args, **kwargs) -> Union[List[T], PageResponse[T]]:
        if pageable:
            entities = self.session.query(self.type_).offset(pageable.page - 1).size(pageable.size).all()
            total_entities = await self.session.query(count(self.type_.id))
            return PageResponse(data=entities, total_items=total_entities, current_page=pageable.page)
        if sort:
            orders = [f"{sort.order_by}, {order.direction}" for order in sort.direction]
            return await self.session.query(self.type_).order_by(sa.text(str(orders))).all()
        return await self.session.query(self.type_).all()

    async def find_all_by_id(self, integers: Iterable[ID]) -> List[T]:
        return self.session.query(self.type_).where(self.type_.id.in_(integers))

    async def find_by_id(self, integer: ID) -> T:
        return self.session.query(self.type_).filter(self.type_.id == integer).one()

    async def get_by_id(self, integer: ID) -> T:
        return self.session.get(self.type_, integer)

    async def save(self, entity: T) -> T:
        if entity.id is not None:
            ...
        else:
            self.session.add(entity)
        try:
            self.session.flush()
        except IntegrityError as e:
            logger.exception(e)
            raise LOSException.with_error(code="UPDATE_ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg_template="Update error")
        return entity

    async def save_all(self, entities: Iterable[T]) -> List[T]:
        try:
            self.session.bulk_save_objects(entities, return_defaults=True)
        except Exception as ex:
            logger.exception(ex)
        return list(entities)


class MongoRepository(IRepository[T, ID]):

    async def save(self, entity: T, modified_by=None) -> T:
        return await self.collection.insert_one(entity, modified_by)
