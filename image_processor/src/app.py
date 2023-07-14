from injectors.init_app import app, host
import routers.api


if __name__ == "__main__":
    app.run(host=host)
