import urllib2
import json
import logging

from google.appengine.api import urlfetch

from apps.data_hunter.models.hunters.base_hunter import HunterAbstract
from apps.data_hunter.models.player_records import Player


class PlayerHunterCBS(HunterAbstract):

    def __init__(self):
        self.site = 'http://api.cbssports.com'
        self.params = 'version=3.0&SPORT=football&response_format=json'
        self.api_key = 'mWgOPLFox6hDE5Ab1BsHqSGYakdnCfyI'
        self.type = 'player'

        self.endpoints = dict(
            players='/fantasy/players/list'
        )

    def request_content(self):
        urlfetch.set_default_fetch_deadline(15)

        req_string = '{0}{1}'.format(self.site, self.endpoints.get('players', ''))
        req_string += "?"+self.params
        logging.info(req_string)

        req = urllib2.Request(req_string)
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req)

        if response.code != 200:
            raise ValueError('Request Error: Status Code: %s' % response.code)

        return response.read()

    def parse_content(self, content):
        record_list = list()
        exception_list = ['tqb', 'dst', 'st']
        json_result = json.loads(content)
        try:
            body = json_result.get('body')
            player_list = body.get('players')
        except:
            raise ValueError("Invalid CPS Player Data Format: Missing 'body->player'")

        for player in player_list:
            if player.get('position').lower() in exception_list:
                continue
            if player.get('position').lower() == 'd':
                player['position'] = 'def'
            if 'unknown-player' in player.get('photo', ''):
                player['photo'] = ''
            try:
                record_list.append(dict(
                    first_name=player.get('firstname', "").lower(),
                    last_name=player.get('lastname', "").lower(),
                    name=player.get('fullname', "").lower(),
                    position=player.get('position', "").lower(),
                    jersey=int(player.get('jersey', "0")),
                    team=player.get('pro_team', "").lower(),
                    bye_week=int(player.get('bye_week', "")),
                    image=player.get('photo', "").lower(),
                ))
            except Exception as e:
                logging.exception(e)
                logging.warning("Invalid Player: %s" % player)

        return record_list


class PlayerHunterPro(HunterAbstract):

    def __init__(self):
        self.site = 'https://profootballapi.com'
        self.api_key = 'mWgOPLFox6hDE5Ab1BsHqSGYakdnCfyI'
        self.type = 'player'

        self.endpoints = dict(
            players='/players'
        )

    def request_content(self):
        urlfetch.set_default_fetch_deadline(15)

        data = dict(
            api_key=self.api_key,
            stats_type='offense',
            year='2015'
        )

        req_string = '{0}{1}'.format(self.site, self.endpoints.get('players', ''))

        req = urllib2.Request(req_string)
        response = urllib2.urlopen(req, json.dumps(data))
        if response.code != 200:
            raise ValueError('Request Error: Status Code: %s' % response.code)

        return response.read()

    def parse_content(self, content):
        record_list = list()

        json_result = json.loads(content)

        return record_list

