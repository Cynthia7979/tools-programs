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
    simplified_save = lambda text: fetch_and_save(text, get_safe_filename(f'{text}.wav', logger), logger)

    with open('script.txt', 'r') as f1:
        lines = f1.readlines()
        logger.info(f'Retrieved script from script.txt. {len(lines)} lines total.')

        for n, line in enumerate(lines):
            line = line.replace('/n', '').replace('/r', '')
            n = n+1

            logger.info(f'Processing line {n} of {len(lines)} ({(n/len(lines)) * 100:.0f}%), '
                        f'{len(lines)-n} left.')

            if len(line) > 257:
                logger.warning('Line is longer than 256 characters. Processing as two parts.')
                simplified_save(line[:257])
                simplified_save(line[257:])
            else:
                simplified_save(line)

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

def fetch_and_save(text, filename, logger):
    if os.path.exists(f'./downloads/{filename}'):
        logger.warning('Skipping due to existing file.')
    else:
        logger.info('Downloading...')
        with open(f'./downloads/{filename}', 'wb') as f2:
            f2.write(fetch(text, logger))
        logger.info('Saved.')


def get_safe_filename(s, logger):
    keep = (' ','.','_')
    safe_fn = "".join(c for c in s if c.isalnum() or c in keep).rstrip()
    logger.debug(f'Safe filename: {safe_fn}')
    return safe_fn


if __name__ == '__main__':
    main()
