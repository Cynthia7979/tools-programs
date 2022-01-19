# GLaDOS Voice Fetcher
This tool uses the API provided by [GLaDOS Voice Generator](https://glados.c-net.org)
and aims to provide convenience in bulk-generation.

The API:
```shell script
curl -L --retry 30 --get --fail \
    --data-urlencode "text=Hello World!" \
    -o "hello_world.wav" \
    "https://glados.c-net.org/generate"
```
