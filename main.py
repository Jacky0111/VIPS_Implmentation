from VIPS.Vips import Vips
from urllib.parse import unquote


def main():
    vips = Vips(unquote('https://www.thestar.com.my/', encoding="utf-8"))
    vips.setRound(10)
    vips.service()


if __name__ == '__main__':
    main()
