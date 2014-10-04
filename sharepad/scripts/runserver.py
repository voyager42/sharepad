import random

from sharepad import app


if __name__ == '__main__':
    random.seed()
    app.debug = True
    app.run()
else:
    random.seed()
