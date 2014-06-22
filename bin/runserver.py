#!/usr/bin/env python

from mockernaut.app import create_app


if __name__ == '__main__':
    app = create_app()
    app.run('localhost', 4000, debug=True)
