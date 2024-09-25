from datetime import datetime
from typing import Iterable
from urllib.error import HTTPError

import requests
from oarepo_runtime.datastreams import BaseReader, StreamEntry

class ZenodoLoader(BaseReader):
    def __init__(self, *, source, all_records, identifiers, oai_config, oai_run, start_from, oai_harvester_id, manual,
                 **kwargs):

        super().__init__(source=source, **kwargs)
        self.all_records = all_records
        self.identifiers = identifiers
        self.oai_config = oai_config
        self.oai_run = oai_run
        self.start_from = start_from
        self.oai_harvester_id = oai_harvester_id
        self.manual = manual

    @property
    def base_query(self):
        return self.oai_config['setspecs']

    def __iter__(self) -> Iterable[StreamEntry]:
        """
        Return iterable or none if there is error
        """
        res = self.get_all_results_zenodo(self.base_query)

        # todo: filtering and double checking if affiliation is correct

        for seq, record in enumerate(res):
            if record is None:
                yield None
            else:
                record = requests.get(url=record['links']['self'], headers={'Accept':'application/vnd.inveniordm.v1+json'}).json()
                yield StreamEntry(entry=record,
                                  seq=seq,
                                  context={
                                    "oai": {
                                    "metadata": (
                                        record['metadata']
                                        if "metadata" in record
                                        else {}
                                    ),
                                    "datestamp": record['updated'],
                                    "deleted": False,
                                    "identifier": f"oai:zenodo.org:{record['id']}",
                                    "setSpecs": self.base_query,
                                    },
                                    "oai_run": self.oai_run,
                                    "oai_harvester_id": self.oai_harvester_id,
                                    "manual": self.manual
                                  })


    def search_zenodo(self, params=None, url=None):
        """
        Sends api request to zenodo either with specific params or to specific url
        Handles http error and returns json response
        """
        try:
            if url is None:
                response = requests.get(self.source, params=params)
            else:
                response = requests.get(url)  # specific url to send api request
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"Other error occurred: {err}")
            return None


    def get_all_results_zenodo(self, query) -> list[dict]:
        """
        Retrieves all results from zenodo using query
        """
        if self.start_from is not None:
            try:
                datetime.strptime(self.start_from, '%Y-%m-%d')
                query = f'({query}) AND updated:[{self.start_from} TO *]'
            except ValueError:
                print("Start from date is not in correct format")
                yield None

        search_results = self.search_zenodo(params={
            'q': query,
            'sort' : "oldest"
        })

        while True:
            if search_results is None:
                yield None
                return

            for search_result in search_results.get('hits', {}).get('hits', []):
               yield search_result
            if search_results.get('links',{}).get('next') is not None:
                search_results = self.search_zenodo(url=search_results.get('links').get('next'))
            else:
                break
