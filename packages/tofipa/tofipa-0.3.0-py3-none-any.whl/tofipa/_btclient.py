from functools import cached_property

import aiobtclientapi


class Client:
    def __init__(self, config):
        self._config = config.copy()

    @property
    def config(self):
        return self._config.copy()

    @cached_property
    def api(self):
        """:class:`aiobtclientapi.APIBase` subclass instance"""
        return aiobtclientapi.api(
            name=self._config['client'],
            url=self._config['url'],
            username=self._config['username'],
            password=self._config['password'],
        )

    async def add_torrent(self, torrent, location):
        """Add `torrent` at download directory `location`"""
        async with self.api:
            return await self.api.add(
                torrent,
                location=location,
                verify=self._config['verify'],
                stopped=self._config['stopped'],
            )
