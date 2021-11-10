from typing import Optional

from api import models
from api.schemas import db, devices, groups
from pydantic import BaseModel, constr


class Group(BaseModel):
    id: Optional[int]
    name: constr(max_length=64)

    @classmethod
    async def add(cls, group: 'Group') -> 'Group':
        """
        Add a group to the database.
        The group's id is auto generated by the database.
        The id is suppressed without warning.
        """
        values = group.dict()
        values.pop('id')

        query = groups.insert().values(**values)
        group.id = await db.execute(query)

        return group

    @classmethod
    async def get(cls, id: int) -> Optional['Group']:
        """Get a group from the database from its id."""
        query = groups.select().where(groups.c.id == id)
        group = await db.fetch_one(query)
        if group:
            return Group(**group)

    @classmethod
    async def get_all(cls) -> list['Group']:
        """Return a list of all groups from the database."""
        return [Group(**group) for group in await db.fetch_all(groups.select())]

    @classmethod
    async def update(cls, id: int, **kwargs) -> Optional['Group']:
        """Update fields of a group."""
        query = groups.update().where(groups.c.id == id).values(**kwargs).returning(groups)
        if group := await db.fetch_one(query):
            return Group(**group)

    @classmethod
    async def edit(cls, id: int, group: 'Group') -> Optional['Group']:
        """Edit a group using another group object."""
        group = group.dict()
        group.pop('id')
        return await cls.update(id, **group)

    @classmethod
    async def delete(cls, id: int) -> Optional['Group']:
        """Delete a group and return it. Return None if the group does not exists."""
        # Move the devices from this group to the default one
        await db.execute(devices.update().where(devices.c.groupId == id).values(id=None))

        query = groups.delete().where(groups.c.id == id).returning(groups)
        group = await db.fetch_one(query)

        return group

    @classmethod
    async def get_devices(cls, id: int) -> list['models.devices.Device']:
        """Get the list of all devices belonging to the group."""
        query = devices.select().where(devices.c.groupId == id)

        return await db.fetch_all(query)
