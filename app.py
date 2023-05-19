import asyncio
import time

import requests

from telegram_poster import Poster
from tweet_scan import Scanner, ConfigError


def download_image(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print(f"Image saved as {file_path}")


async def process_tweet(scan, poster, previous_tweet: list):
    if scan.tweet_link not in previous_tweet:
        if scan.tweet_text:
            await poster.post_message(scan.tweet_text)
            print('message was sent')
        if scan.tweet_img:
            for i, url in enumerate(scan.tweet_img):
                count = i + 1
                path = f'img_{count}.jpg'
                download_image(url, path)
                await poster.post_picture(path)
            print('all pictures were sent')
        previous_tweet.append(scan.tweet_link)


async def main():
    scan = Scanner(user='your screen name')
    poster = Poster()
    try:
        scan.config_check()
        scan.authenticate()

        previous_tweet = [scan.tweet_link]

        while True:
            scan.get_tweet()
            await process_tweet(scan, poster, previous_tweet)
            time.sleep(30)

    except ValueError as e:
        print(f'Error: {e}')
    except ConfigError:
        scan.set_config()
        scan.get_tweet()


if __name__ == "__main__":
    asyncio.run(main())
