# anime-server
Miscellaneous place for all of my anime stuff

## Visualize your MyAnimeList anime at https://lucys-anime-server.herokuapp.com/mal?username=YOUR MAL USERNAME HERE

* Visualizes your MAL anime using `three.js`. 
* Creates a text sprite that appears as 3d block text of the anime's title and attaches that to a corresponding spherical mesh. The sphere's size and number of segments depend on the user's score for that anime. The larger the score, the larger the sphere will be. Furthermore, the x and y coordinate of the sphere is also dependent on the score. The higher the score, the closer the sphere will be to the center. The y coordinate is simply the order in which the anime appears on the list. 

## Get seasonal anime recommendations for any year and season
### How it works
1. Given a year and a season, `anime_rec.py` scrapes all of the seasonal anime (title, studio, description) from [https://www.livechart.me/]. 
2. Given the user's MyAnimeList, I use the MAL api to get all of the user's watched anime ids, and then beautifulsoup to scrape the genre and studio information for the individual anime's page (which can be created using the anime id) and respective information such as anime score. Using this data, I can create dictionaries of weighted genres and animation studios, with the most favored genres and studios having the highest values. These 2 dictionaries are used to rank new seasonal anime.  
This is also done in parallel using python's `multiprocessing` as some people can have extremely long MyAnimeLists, which makes scraping a bit faster. However, when too many processes are spawned, the MyAnimeList server stops responding, so a timeout of ~30 seconds is provided before trying to hit the site again.
3. The above operation in #2 can take a long time–so long that it timesout heroku's maximum http request time. As a result, I use a Redis queue to schedule a background worker to do the scraping and have an ajax call periodically calling a backend endpoint to see whether or not the method has returned. When it returns, the results are presented in a UI.

## View data on anime character biometrics (such as height and weight)
