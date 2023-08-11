from TVRemoteProjectPyFile import *
from functions import *


def main() -> None:
    try:
        application = QApplication([])
        window = TVremote()
        window.show()
        application.exec()
    except RuntimeError:
        print("Runtime Error.")


if __name__ == "__main__":
    main()
