from typing import Optional

from api.schemas import db, devices
from pydantic import BaseModel, constr
from sqlalchemy import select


class Device(BaseModel):
    id: Optional[int]
    groupId: Optional[int]
    name: constr(max_length=64)
    modele: constr(max_length=64)
    type: int
    ip: constr(max_length=15)
    toggle: bool

    @classmethod
    async def add(cls, device: 'Device') -> 'Device':
        """
        Add a device to the database.
        The device's id is auto generated by the database.
        The id is suppressed without warning.
        """
        values = device.dict()
        values.pop('id')

        query = devices.insert().values(**values)
        device.id = await db.execute(query)

        return device

    @classmethod
    async def get(cls, id: int) -> Optional['Device']:
        """Get a device from the database from its id."""
        query = devices.select().where(devices.c.id == id)
        device = await db.fetch_one(query)
        if device:
            return Device(**device)

    @classmethod
    async def get_devices_ip(cls, ip: str) -> list['Device']:
        """Get a device from the database from its ip address."""
        query = devices.select().where(devices.c.ip == ip)
        response = await db.fetch_all(query)
        r = [Device(**device) for device in response]
        print(r)
        return r

    @classmethod
    async def get_toggle(cls, id: int) -> Optional['Device']:
        """Get the status of a device from the database from its id."""
        query = select(devices.c.toggle).select_from(devices).where(devices.c.id == id)
        toggle = await db.fetch_one(query)
        if toggle:
            return toggle

    @classmethod
    async def get_all(cls) -> list['Device']:
        """Return a list of all devices from the database."""
        return [Device(**device) for device in await db.fetch_all(devices.select())]

    @classmethod
    async def update(cls, id: int, **kwargs) -> Optional['Device']:
        """Update fields of a device."""
        query = devices.update().where(devices.c.id == id).values(**kwargs).returning(devices)
        if device := await db.fetch_one(query):
            return Device(**device)

    @classmethod
    async def edit_toggle(cls, id: int, toggle: bool, device: 'Device') -> Optional['dict']:
        """Edit toggle of a device using another device object."""
        device = device.dict()
        device.pop('id')
        device['toggle'] = toggle
        return await cls.update(id, **device)

    @classmethod
    async def edit(cls, id: int, device: 'Device') -> Optional['Device']:
        """Edit a device using another device object."""
        device = device.dict()
        device.pop('id')
        return await cls.update(id, **device)

    @classmethod
    async def delete(cls, id: int) -> Optional['Device']:
        """Delete a device and return it. Return None if the device does not exists."""
        query = devices.delete().where(devices.c.id == id).returning(devices)
        device = await db.fetch_one(query)

        return device
