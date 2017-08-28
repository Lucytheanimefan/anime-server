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
            entries.append(entry.to_string())

        return entries


if __name__ == '__main__':
    coordinator = MalCoordinator()
    for entry in coordinator.fetch_animelist("Silent_Muse"):
        print entry
        print "\n"
