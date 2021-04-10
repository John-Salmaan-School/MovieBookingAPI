# Main file that runs the app
from moviebookingapi import init_app
import config

app = init_app()

if __name__ == "__main__":
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )

