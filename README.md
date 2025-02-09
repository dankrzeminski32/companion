# companion

an http 1.0 web server, implemented with python

Note: This is not intended to be used in any form of a production environment. For sake of time, I didn't pay attention to every edge case or security concern. 

## Goals

- Implement a subset of the http 1.0 protocol (rfc 1945)
- Handle GET and HEAD requests from a client
- Manage multiple connections (threading, multiprocessing, etc)
- Use only the python standard lib 