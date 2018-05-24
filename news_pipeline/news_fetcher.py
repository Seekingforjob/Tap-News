import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://qaxmxozt:k7_R-cmOcZbdORt5LUWktg2F1vTsRS9u@otter.rmq.cloudamqp.com/qaxmxozt"
DEDUPE_NEWS_TASK_QUEUE_NAME = "dedupe-news"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://hilhtjts:H48lD7TxF_1DQdcZhBOsOvFpmgJOmwQW@otter.rmq.cloudamqp.com/hilhtjts"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass
scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)