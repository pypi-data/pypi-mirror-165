from typing import Dict

from constellate.database.sqlalchemy.sqlalchemydbconfig import SQLAlchemyDBConfig, DBConfigType


class UnitToShardMixin(object):
    def __init__(self, data: Dict = None, *args, **kwargs):
        """
        Can be used to set a static table to map between an application defined unit and a shard
        """
        self._data = data

    def get_config_for_unit(self, **kwargs) -> SQLAlchemyDBConfig:
        """
        Get SQLAlchemyDBConfig for an application defined unit
        """
        shard_id = self._get_shard_id_for_unit(**kwargs)
        return self.get_instance_config(identifier=shard_id)

    def get_instance_config(
        self, type: DBConfigType = DBConfigType.INSTANCE, identifier: str = None, **kwargs
    ) -> SQLAlchemyDBConfig:
        """
        Get the SQLALchemyConfig with identifier specified
        @param kwargs Application defined settings to restrict the search for a suitable config
        """
        return self.config_manager.find(type=type, identifier=identifier, **kwargs)

    def _get_shard_id_for_unit(self, **kwargs) -> str:
        """
        Get shard id for an application defined unit
        @param kwargs Application defined settings to restrict the search for a suitable config
        @raises: NotImplementedError if no shard can be found
        """
        # Sample implementation:
        # shard_id = self._data.get(kwargs['something])
        raise NotImplementedError()
