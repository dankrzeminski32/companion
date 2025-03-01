# companion

an http 1.0 web server, implemented with python

Note: This is not intended to be used in any form of a production environment. For sake of time, I didn't pay attention to every edge case or security concern. 

## Installation

First, install the companion server to your computer, 

```bash
pip install companion-server
```

Now, we can run the server... The only required argument is a path to your content directory, this is how the server knows where to look for content (e.g. HTML, PNG, etc)

You can optionally specify a port otherwise it will default to 8180

```bash
companion-server /home/dan/webserver/content/ --port 1000
```

## Development

First install the dev dependancies,

```bash
poetry install --with dev
```

Then you can run the test suite,

```bash
poetry run pytest .
```

## Goals

[x] Implement a subset of the http 1.0 protocol (rfc 1945)

[x] Handle GET and HEAD requests from a client

[x] Manage multiple connections (threading, multiprocessing, etc)

[x] Use only the python standard lib 