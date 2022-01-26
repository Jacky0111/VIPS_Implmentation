from urllib.parse import unquote

from Prequel import Prequel
from VIPS.Vips import Vips


def main():
    pre = Prequel(unquote('https://www.thestar.com.my/business', 'encoding="utf-8'))
    # pre = Prequel(unquote('https://www.malaymail.com/news/sports', 'encoding="utf-8'))
    # pre = Prequel(unquote('https://www.nst.com.my/business/home', 'encoding="utf-8'))
    # pre = Prequel(unquote('https://sea.mashable.com/science/', 'encoding="utf-8'))
    # pre = Prequel(unquote('https://www.bernama.com/bm/sukan/index.php', 'encoding="utf-8'))

    for index, link in enumerate(pre.url_list):
        vips = Vips(unquote(link, 'encoding="utf-8'))
        vips.runner()

    # vips = Vips(unquote('https://www.thestar.com.my/news/nation/2021/09/26/phase-3-bpr-payments-to-start-from-tuesday'
    #                     '-sept-28-says-pm', 'encoding="utf-8'))

    # vips = Vips(unquote('https://www.thestar.com.my/lifestyle/culture/2021/08/06/festivals-for-britain-as-events-get'
    #                     '-us1bil-covid-reinsurance-cover', 'encoding="utf-8'))
    #
    # vips = Vips(unquote('https://www.thestar.com.my/business/business-news/2021/08/06/tiong-nam-to-acquire-land-from'
    #                     '-senai-airport', 'encoding="utf-8'))
    #
    # vips = Vips(unquote('https://www.nst.com.my/news/nation/2021/09/730991/wise-wait-90-cent-adult-vaccination-rate'
    #                     '-allowing-interstate-travel', 'encoding="utf-8'))
    #
    # vips = Vips(unquote('https://www.malaymail.com/news/malaysia/2021/09/26/deputy-tourism-minister-theme-parks-in'
    #                     '-malaysia-may-reopen-to-public-in-nov/2008582', 'encoding="utf-8'))

    # vips.runner()


if __name__ == '__main__':
    main()
