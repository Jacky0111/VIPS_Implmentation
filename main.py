from VIPS.Vips import Vips
from urllib.parse import unquote


def main():
    vips = Vips('https://www.thestar.com.my/news/nation/2021/06/18/high-spikes-in-registration-as-vaccinations-revved-up')
    vips.setRound(10)
    vips.service()


if __name__ == '__main__':
    main()
