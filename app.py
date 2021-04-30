# Main file that runs the app
from moviebookingapi import init_app, init_db
import logging
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR, filename="app.log")

app = init_app()
init_db()


if __name__ == "__main__":
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )
