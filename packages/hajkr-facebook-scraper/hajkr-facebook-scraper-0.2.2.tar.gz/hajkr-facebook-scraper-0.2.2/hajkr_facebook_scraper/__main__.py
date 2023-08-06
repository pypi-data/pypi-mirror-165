from facebook_scraper import *
from facebook_scraper.exceptions import LoginRequired
import argparse
import logging


def enable_logging():
    logger = logging.getLogger('facebook_scraper')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

    # file_handler = logging.FileHandler('logs/debug.log')
    # file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    # logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def write_post_to_disk(post):
    filename = f'{post["post_id"]}.json'
    with open(f'output/{filename}', mode='wt') as file:
        json.dump(post, file, indent=4, default=str)


def write_posts_to_disk(posts, filename):
    keys = list(posts[0].keys())
    for post in posts:
        for key in post.keys():
            if key not in keys:
                keys.append(key)

    with open(filename, 'w', encoding=locale.getpreferredencoding()) as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(posts)


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument('group_id', type=str, help="Facebook group id")
    parser.add_argument('--proxy', type=str, help="Proxy server address", default=None)
    parser.add_argument('--c_user', type=str, help="Facebook cookie c_user", default=None)
    parser.add_argument('--xs', type=str, help="Facebook cookie xs", default=None)
    parser.add_argument('--pages', type=int, help="Number of pages to download", default=5)
    parser.add_argument('--debug', type=bool, help="Enable debug", default=False)
    parser.add_argument('--logging', type=bool, help="Enable logging", default=False)
    parser.add_argument('--filename', type=str, help="Output file", default='posts.csv')

    args = parser.parse_args()
    print(args)

    if args.logging:
        enable_logging()

    count = 0
    list_of_posts = []
    options = {
        "page_limit": args.pages,
    }

    scraper = FacebookScraper()
    if args.proxy:
        logger.info(f'Proxy: {args.proxy}')
        scraper.requests_kwargs.update({
            'proxies': {
                'http': args.proxy,
                'https': args.proxy,
            }
        })

    if args.c_user:
        logger.info(f'Cookie c_user: {args.c_user}')
        scraper.session.cookies.set("c_user", args.c_user)
    if args.xs:
        logger.info(f'Cookie xs: {args.xs}')
        scraper.session.cookies.set("xs", args.xs)

    try:
        for post in scraper.get_group_posts(args.group_id, **options):
            logger.info(f'{count + 1} => {post["post_id"]}, {post["time"]}')

            if args.debug:
                write_post_to_disk(post)

            list_of_posts.append(post)

            count += 1
    except LoginRequired:
        logger.error("Login is required.")

        if count == 0:
            logger.warning("Login required. No posts found. Is your IP banend?")
            exit(1)

    if count == 0:
        logger.warning("No posts found. Is your IP banend?")
        exit(1)

    write_posts_to_disk(list_of_posts, args.filename)


if __name__ == '__main__':
    run()
