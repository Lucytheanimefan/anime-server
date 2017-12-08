import logging

import requests

import mal

log = logging.getLogger(__name__)


class MalCoordinator(object):
    """
    Coordinator that interfaces with MyAnimeList.net
    """
    def fetch_animelist(self, username):
        """
        Fetches the animelist for a given user.

        :param common.User user: Given user

        :return: Raw JSON.
        :rtype: list[mal.MalEntry]
        """
        entries = []

        url = 'https://myanimelist.net/animelist/{}/load.json'.format(username)
        r = requests.get(url)
        json_entries = r.json()

        if isinstance(json_entries, dict):
            log.error(u"Error while fetching top anime for {}".format(username))
            return entries

        for json_entry in json_entries:
            entry = mal.MalEntry(username)
            entry.anime_id = json_entry['anime_id']
            entry.title = json_entry['anime_title']
            entry.user_status = json_entry['status']
            entry.airing_status = json_entry['anime_airing_status']
            entry.watched_episodes = json_entry['num_watched_episodes']
            entry.total_episodes = json_entry['anime_num_episodes']
            entry.user_score = json_entry['score']
            entry.image_url = json_entry['anime_image_path']
            entry.url = "https://myanimelist.net" + json_entry['anime_url']
            entries.append(entry.to_string())

        return entries


    def authenticate(username, password):
        """
        Authenticates username and password with MAL (PS MAL authentication security is fucking terrible wow)
        
        :returns 'user:password' encoded as base64 string (because this is the only way to save authentication without throwing the poor user's password around thanks to MAL auth scheme lol. Not that this is any safer, but it makes my conscience feel better

        """
        #TODO: Figure out how not to get banned by MAL for too many incorrect logins??
        from base64 import b64encode
        url = 'https://myanimelist.net/api/account/verify_credentials.xml'
        encoded_credentials = base64.b64encode(('%s:%s' % (username, password)).encode('utf-8'))
        r = requests.get(url, headers = {'Authorization': 'Basic %s' % encoded_credentials.decode('utf-8')})
        return r.status_code, encoded_credentials

if __name__ == '__main__':
    coordinator = MalCoordinator()
    for entry in coordinator.fetch_animelist("Silent_Muse"):
        print entry
        print "\n"
