# Run under glados_voice_fetcher/
import os
import requests
import log

api_link = "https://glados.c-net.org/generate?text={text}"


def main():
    if not os.path.exists('./downloads'):
        os.mkdir('./downloads/')
    logger = log.log_init(os.path.basename(__file__))
    logger.info('Starting...')

    with open('script.txt', 'r') as f1:
        lines = f1.readlines()
        logger.info(f'Retrieved script from script.txt. {len(lines)} lines total.')
        for n, line in enumerate(lines):
            line = line.strip('/n')
            logger.info(f'Processing line {n+1} of {len(lines)}, '
                        f'{len(lines)-n+1} ({((len(lines)-n+1)/len(lines)) * 100:.0f}%) left.')
            safe_filename = get_safe_filename(f'{line}.wav', logger)
            if os.path.exists(f'./downloads/{safe_filename}'):
                logger.warning(f'Skipping due to existing file.')
            else:
                logger.info('Downloading line...')
                with open(f'./downloads/{safe_filename}', 'wb') as f2:
                    f2.write(fetch(line, logger))
                logger.info('Saved.')
    logger.info('Work complete.')


def fetch(text, logger):
    logger.debug(f'Fetching text "{text}"...')
    response = requests.get(api_link.format(text=text)).content
    if response == b'Your sample is queued for processing.\n':
        logger.debug('Waiting for response.')
        # Wait for response
        response = requests.get(api_link.format(text=text)).content
    logger.debug('Text fetched.')
    return response


def get_safe_filename(s, logger):
    keep = (' ','.','_')
    safe_fn = "".join(c for c in s if c.isalnum() or c in keep).rstrip()
    logger.debug(f'Safe filename: {safe_fn}')
    return safe_fn


if __name__ == '__main__':
    main()
