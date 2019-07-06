#!/usr/bin/env python3

from app import app


if __name__ == "__main__":
    app.run(debug=app.config.get('FLASK_DEBUG'),
            host=app.config.get('FLASK_HOST'),
            port=app.config.get('FLASK_PORT'))
