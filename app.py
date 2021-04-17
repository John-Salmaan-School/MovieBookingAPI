# Main file that runs the app
from moviebookingapi import init_app
import logging
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = init_app()

if __name__ == "__main__":
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )