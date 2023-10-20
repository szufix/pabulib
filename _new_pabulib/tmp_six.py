
from PIL import Image



NAMES = {}

NAMES['warszawa_2023'] = {
    'poland_warszawa_2023_bemowo.pb': 'Bemowo',
    'poland_warszawa_2023_bialoleka.pb': 'Białołęka',
    'poland_warszawa_2023_bielany.pb': 'Bielany',
    'poland_warszawa_2023_mokotow.pb': 'Mokotów',
    'poland_warszawa_2023_ochota.pb': 'Ochota',
    'poland_warszawa_2023_praga-polnoc.pb': 'Praga-Północ',
    'poland_warszawa_2023_praga-poludnie.pb': 'Praga-Południe',
    'poland_warszawa_2023_rembertow.pb': 'Rembertów',
    'poland_warszawa_2023_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2023_targowek.pb': 'Targówek',
    'poland_warszawa_2023_ursus.pb': 'Ursus',
    'poland_warszawa_2023_ursynow.pb': 'Ursynów',
    'poland_warszawa_2023_wawer.pb': 'Wawer',
    'poland_warszawa_2023_wesola.pb': 'Wesoła',
    'poland_warszawa_2023_wilanow.pb': 'Wilanów',
    'poland_warszawa_2023_wlochy.pb': 'Włochy',
    'poland_warszawa_2023_wola.pb': 'Wola',
    'poland_warszawa_2023_zoliborz.pb': 'Żoliborz'
}

NAMES['warszawa_2022'] = {
    'poland_warszawa_2022_bemowo.pb': 'Bemowo',
    'poland_warszawa_2022_bialoleka.pb': 'Białołęka',
    'poland_warszawa_2022_bielany.pb': 'Bielany',
    'poland_warszawa_2022_mokotow.pb': 'Mokotów',
    'poland_warszawa_2022_ochota.pb': 'Ochota',
    'poland_warszawa_2022_praga-polnoc.pb': 'Praga-Północ',
    'poland_warszawa_2022_praga-poludnie.pb': 'Praga-Południe',
    'poland_warszawa_2022_rembertow.pb': 'Rembertów',
    'poland_warszawa_2022_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2022_targowek.pb': 'Targówek',
    'poland_warszawa_2022_ursus.pb': 'Ursus',
    'poland_warszawa_2022_ursynow.pb': 'Ursynów',
    'poland_warszawa_2022_wawer.pb': 'Wawer',
    'poland_warszawa_2022_wesola.pb': 'Wesoła',
    'poland_warszawa_2022_wilanow.pb': 'Wilanów',
    'poland_warszawa_2022_wlochy.pb': 'Włochy',
    'poland_warszawa_2022_wola.pb': 'Wola',
    'poland_warszawa_2022_zoliborz.pb': 'Żoliborz'
}

NAMES['warszawa_2021'] = {
    'poland_warszawa_2021_bemowo.pb': 'Bemowo',
    'poland_warszawa_2021_bialoleka.pb': 'Białołęka',
    'poland_warszawa_2021_bielany.pb': 'Bielany',
    'poland_warszawa_2021_mokotow.pb': 'Mokotów',
    'poland_warszawa_2021_ochota.pb': 'Ochota',
    'poland_warszawa_2021_praga-polnoc.pb': 'Praga-Północ',
    'poland_warszawa_2021_praga-poludnie.pb': 'Praga-Południe',
    'poland_warszawa_2021_rembertow.pb': 'Rembertów',
    'poland_warszawa_2021_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2021_targowek.pb': 'Targówek',
    'poland_warszawa_2021_ursus.pb': 'Ursus',
    'poland_warszawa_2021_ursynow.pb': 'Ursynów',
    'poland_warszawa_2021_wawer.pb': 'Wawer',
    'poland_warszawa_2021_wesola.pb': 'Wesoła',
    'poland_warszawa_2021_wilanow.pb': 'Wilanów',
    'poland_warszawa_2021_wlochy.pb': 'Włochy',
    'poland_warszawa_2021_wola.pb': 'Wola',
    'poland_warszawa_2021_zoliborz.pb': 'Żoliborz'
}

NAMES['warszawa_2020'] = {
    'poland_warszawa_2020_bemowo.pb': 'Bemowo',
    'poland_warszawa_2020_bialoleka.pb': 'Białołęka',
    'poland_warszawa_2020_bielany.pb': 'Bielany',
    'poland_warszawa_2020_mokotow.pb': 'Mokotów',
    'poland_warszawa_2020_ochota.pb': 'Ochota',
    'poland_warszawa_2020_praga-polnoc.pb': 'Praga-Północ',
    'poland_warszawa_2020_praga-poludnie.pb': 'Praga-Południe',
    'poland_warszawa_2020_rembertow.pb': 'Rembertów',
    'poland_warszawa_2020_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2020_targowek.pb': 'Targówek',
    'poland_warszawa_2020_ursus.pb': 'Ursus',
    'poland_warszawa_2020_ursynow.pb': 'Ursynów',
    'poland_warszawa_2020_wawer.pb': 'Wawer',
    'poland_warszawa_2020_wesola.pb': 'Wesoła',
    'poland_warszawa_2020_wilanow.pb': 'Wilanów',
    'poland_warszawa_2020_wlochy.pb': 'Włochy',
    'poland_warszawa_2020_wola.pb': 'Wola',
    'poland_warszawa_2020_zoliborz.pb': 'Żoliborz'
}

REGION = {
    'warszawa_2023_geo': 'warszawa_2023',
    'warszawa_2022_geo': 'warszawa_2022',
    'warszawa_2021_geo': 'warszawa_2021',
    'warszawa_2020_geo': 'warszawa_2020',
    'warszawa_2023': 'warszawa_2023',
    'warszawa_2022': 'warszawa_2022',
    'warszawa_2021': 'warszawa_2021',
    'warszawa_2020': 'warszawa_2020',
}




def merge_images(list_of_names=None, size=250, show=False, ncol=1, nrow=1,
                 region=None):

    region = 'six'

    images = []
    images.append(Image.open(f'images/warszawa_2020/poland_warszawa_2020_mokotow.pb.png'))
    images.append(Image.open(f'images/warszawa_2021/poland_warszawa_2021_ochota.pb.png'))
    images.append(Image.open(f'images/warszawa_2022/poland_warszawa_2022_wawer.pb.png'))

    images.append(Image.open(f'images/warszawa_2020_geo/poland_warszawa_2020_mokotow.pb.png'))
    images.append(Image.open(f'images/warszawa_2021_geo/poland_warszawa_2021_ochota.pb.png'))
    images.append(Image.open(f'images/warszawa_2022_geo/poland_warszawa_2022_wawer.pb.png'))
    # for i, name in enumerate(list_of_names):
    #     images.append(Image.open(f'images/{region}/{name}.png'))
    image1_size = images[0].size

    new_image = Image.new('RGB', (ncol * image1_size[0], nrow * image1_size[1]),
                          (size, size, size))

    for i in range(ncol):
        for j in range(nrow):
            try:
                new_image.paste(images[i + j * ncol], (image1_size[0] * i, image1_size[1] * j))
            except:
                pass


    new_image.save(f'images/{region}.png', "PNG", quality=85)
    if show:
        new_image.show()


if __name__ == "__main__":

    merge_images(ncol=3, nrow=2, show=True)
