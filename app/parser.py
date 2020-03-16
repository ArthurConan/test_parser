import aiohttp_jinja2
import aiohttp
import json

from aiohttp import web
from datetime import datetime

from app.errors import request_errors, redis_errors
from config import settings
from app.addition import status


class Parser(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        """
        This method should get all available result data from source and parse it.
        Result data extracted via aiohttp get request.
        Also catch casual connection error.
        :return: render template with context as dict
        """
        letter = self.request.match_info.get('letter').lower()
        results = {}
        total_result = []

        for i in range(100):
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(settings.BASE_URL.format(i)) as resp:
                        results = json.loads(await resp.text())
                        break
                except request_errors:
                    continue
                except (AttributeError, TypeError):
                    continue
        if results:
            total_result = self.get_parsed_data(results.get('sections'), results.get('events'), letter)
            await self.redis_insert(results, total_result)
        return {
            'result': total_result
        }

    async def redis_insert(self, raw_result, total_result):
        """
        Add parsed and raw (just to be safe) received data to sets in redis database.
        Also catch casual redis error.
        :param raw_result: raw data from source, that includes info about sports, sections, events
        :param total_result: parsed data from source
        :return:
        """
        try:
            redis = await self.request.app['redis']
            tr = redis.multi_exec()
            tr.sadd('sports', *list(map(str, raw_result.get('sports'))))
            tr.sadd('sections', *list(map(str, raw_result.get('sections'))))
            tr.sadd('events', *list(map(str, raw_result.get('events'))))
            tr.sadd('total', *list(map(str, total_result)))
            await tr.execute()
        except redis_errors:
            pass
        return

    @staticmethod
    def get_parsed_data(section_data, events_data, letter):
        """
        Parse raw data from source and convert to appropriate view.
        :param section_data: data from source with info about sport sections
        :param events_data: data from source with info about sport events
        :param letter: for selection and filtration result
        :return: parsed data
        """
        total_result = [
            {
                "section": section.get('name'),
                "event": [{k: (datetime.utcfromtimestamp(v).strftime('%B %d at %H:%M') if k in ['startTime']
                               else status.get(v) if k in ['status'] else v)
                           for k, v in event.items() if k in ['id', 'name', 'score', 'startTime', 'status', 'comment3']}
                          for event in events_data if all([int(event.get('id')) in section.get('events'),
                                                           event.get('name', '').lower().startswith(letter)])]
            }
            for section in section_data
        ]
        total_result.sort(key=lambda dictionary: int(dictionary.get('event')[0].get('id', 0))
                          if dictionary.get('event') else 0)
        return total_result


