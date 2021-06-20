from VIPS.Vips import Vips
from urllib.parse import unquote


def main():
    vips = Vips(unquote('https://www.thestar.com.my/news/nation/2021/06/18/high-spikes-in-registration-as-vaccinations-revved-up', encoding="utf-8"))
    vips.setRound(10)
    vips.service()


if __name__ == '__main__':
    main()
