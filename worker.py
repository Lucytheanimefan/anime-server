import os

import redis
from rq import Worker, Queue, Connection
from anime_rec import findSeasonRecs, batch_anime_scrape


listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)
q = Queue(connection=conn)

result = q.enqueue(findSeasonRecs, 'Silent_Muse', 'Spring', '2018')


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()