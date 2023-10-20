import csv
import matplotlib.pyplot as plt
import ast
from scipy.stats import stats
import math
import numpy as np
plt.rcParams["font.family"] = "Times New Roman"

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

NAMES['wroclaw_2019'] = {
    'poland_wroclaw_2019_.pb': 'a',
    'poland_wroclaw_2019_local.pb': 'b',
}

NAMES['wroclaw_2020'] = {
    'poland_wroclaw_2020_.pb': 'a',
    'poland_wroclaw_2020_local.pb': 'b',
}

NAMES['wroclaw_2021'] = {
    'poland_wroclaw_2021_.pb': 'a',
    'poland_wroclaw_2021_local.pb': 'b',
}

NAMES['krakow_2018'] = {
    # 'poland_krakow_2018_.pb' : '',
    'poland_krakow_2018_bienczyce.pb': '',
    'poland_krakow_2018_biezanow-prokocim.pb': '',
    'poland_krakow_2018_bronowice.pb': '',
    'poland_krakow_2018_czyzyny.pb': '',
    'poland_krakow_2018_debniki.pb': '',
    'poland_krakow_2018_grzegorzki.pb': '',
    'poland_krakow_2018_krowodrza.pb': '',
    'poland_krakow_2018_lagiewniki-borek-falecki.pb': '',
    'poland_krakow_2018_mistrzejowice.pb': '',
    'poland_krakow_2018_nowa-huta.pb': '',
    'poland_krakow_2018_podgorze.pb': '',
    'poland_krakow_2018_podgorze-duchackie.pb': '',
    'poland_krakow_2018_pradnik-bialy.pb': '',
    'poland_krakow_2018_pradnik-czerwony.pb': '',
    'poland_krakow_2018_stare-miasto.pb': '',
    'poland_krakow_2018_swoszowice.pb': '',
    'poland_krakow_2018_wzgorza-krzeslawickie.pb': '',
    'poland_krakow_2018_zwierzyniec.pb': '',
}

NAMES['krakow_2019'] = {
    # 'poland_krakow_2019_.pb' : '',
    'poland_krakow_2019_bienczyce.pb': '',
    'poland_krakow_2019_biezanow-prokocim.pb': '',
    'poland_krakow_2019_bronowice.pb': '',
    'poland_krakow_2019_czyzyny.pb': '',
    'poland_krakow_2019_debniki.pb': '',
    'poland_krakow_2019_grzegorzki.pb': '',
    'poland_krakow_2019_krowodrza.pb': '',
    'poland_krakow_2019_lagiewniki-borek-falecki.pb': '',
    'poland_krakow_2019_mistrzejowice.pb': '',
    'poland_krakow_2019_nowa-huta.pb': '',
    'poland_krakow_2019_podgorze.pb': '',
    'poland_krakow_2019_podgorze-duchackie.pb': '',
    'poland_krakow_2019_pradnik-bialy.pb': '',
    'poland_krakow_2019_pradnik-czerwony.pb': '',
    'poland_krakow_2019_stare-miasto.pb': '',
    'poland_krakow_2019_swoszowice.pb': '',
    'poland_krakow_2019_wzgorza-krzeslawickie.pb': '',
    'poland_krakow_2019_zwierzyniec.pb': '',
}

NAMES['krakow_2020'] = {
    # 'poland_krakow_2020_.pb' : '',
    'poland_krakow_2020_bienczyce.pb': '',
    'poland_krakow_2020_biezanow-prokocim.pb': '',
    'poland_krakow_2020_bronowice.pb': '',
    'poland_krakow_2020_czyzyny.pb': '',
    'poland_krakow_2020_debniki.pb': '',
    'poland_krakow_2020_grzegorzki.pb': '',
    'poland_krakow_2020_krowodrza.pb': '',
    'poland_krakow_2020_lagiewniki-borek-falecki.pb': '',
    'poland_krakow_2020_mistrzejowice.pb': '',
    'poland_krakow_2020_nowa-huta.pb': '',
    'poland_krakow_2020_podgorze.pb': '',
    'poland_krakow_2020_podgorze-duchackie.pb': '',
    'poland_krakow_2020_pradnik-bialy.pb': '',
    'poland_krakow_2020_pradnik-czerwony.pb': '',
    'poland_krakow_2020_stare-miasto.pb': '',
    'poland_krakow_2020_swoszowice.pb': '',
    'poland_krakow_2020_wzgorza-krzeslawickie.pb': '',
    'poland_krakow_2020_zwierzyniec.pb': '',
}

NAMES['krakow_2021'] = {
    # 'poland_krakow_2021_.pb' : '',
    'poland_krakow_2021_bienczyce.pb': '',
    'poland_krakow_2021_biezanow-prokocim.pb': '',
    'poland_krakow_2021_bronowice.pb': '',
    'poland_krakow_2021_czyzyny.pb': '',
    'poland_krakow_2021_debniki.pb': '',
    'poland_krakow_2021_grzegorzki.pb': '',
    'poland_krakow_2021_krowodrza.pb': '',
    'poland_krakow_2021_lagiewniki-borek-falecki.pb': '',
    'poland_krakow_2021_mistrzejowice.pb': '',
    'poland_krakow_2021_nowa-huta.pb': '',
    'poland_krakow_2021_podgorze.pb': '',
    'poland_krakow_2021_podgorze-duchackie.pb': '',
    'poland_krakow_2021_pradnik-bialy.pb': '',
    'poland_krakow_2021_pradnik-czerwony.pb': '',
    'poland_krakow_2021_stare-miasto.pb': '',
    'poland_krakow_2021_swoszowice.pb': '',
    'poland_krakow_2021_wzgorza-krzeslawickie.pb': '',
    'poland_krakow_2021_zwierzyniec.pb': '',
}

NAMES['krakow_2022'] = {
    # 'poland_krakow_2022_.pb' : '',
    'poland_krakow_2022_bienczyce.pb': '',
    'poland_krakow_2022_biezanow-prokocim.pb': '',
    'poland_krakow_2022_bronowice.pb': '',
    'poland_krakow_2022_czyzyny.pb': '',
    'poland_krakow_2022_debniki.pb': '',
    'poland_krakow_2022_grzegorzki.pb': '',
    'poland_krakow_2022_krowodrza.pb': '',
    'poland_krakow_2022_lagiewniki-borek-falecki.pb': '',
    'poland_krakow_2022_mistrzejowice.pb': '',
    'poland_krakow_2022_nowa-huta.pb': '',
    'poland_krakow_2022_podgorze.pb': '',
    'poland_krakow_2022_podgorze-duchackie.pb': '',
    'poland_krakow_2022_pradnik-bialy.pb': '',
    'poland_krakow_2022_pradnik-czerwony.pb': '',
    'poland_krakow_2022_stare-miasto.pb': '',
    'poland_krakow_2022_swoszowice.pb': '',
    'poland_krakow_2022_wzgorza-krzeslawickie.pb': '',
    'poland_krakow_2022_zwierzyniec.pb': '',
}

NAMES['zabrze_2020'] = {
    # 'poland_zabrze_2020_.pb': '',
    'poland_zabrze_2020_biskupice.pb': '',
    'poland_zabrze_2020_centrum-polnoc.pb': '',
    'poland_zabrze_2020_centrum-poludnie.pb': '',
    'poland_zabrze_2020_grzybowice.pb': '',
    'poland_zabrze_2020_guido.pb': '',
    'poland_zabrze_2020_helenka.pb': '',
    'poland_zabrze_2020_konczyce.pb': '',
    'poland_zabrze_2020_maciejow.pb': '',
    'poland_zabrze_2020_makoszowy.pb': '',
    'poland_zabrze_2020_mikulczyce.pb': '',
    'poland_zabrze_2020_osiedle-mikolaja-kopernika.pb': '',
    'poland_zabrze_2020_osiedle-mlodego-gornika.pb': '',
    'poland_zabrze_2020_osiedle-tadeusza-kotarbinskiego.pb': '',
    'poland_zabrze_2020_pawlow.pb': '',
    'poland_zabrze_2020_rokitnica.pb': '',
    'poland_zabrze_2020_zaborze-polnoc.pb': '',
    'poland_zabrze_2020_zaborze-poludnie.pb': '',
    'poland_zabrze_2020_zandka.pb': '',
}

NAMES['zabrze_2021'] = {
    # 'poland_zabrze_2021_.pb': '',
    'poland_zabrze_2021_biskupice.pb': '',
    'poland_zabrze_2021_centrum-polnoc.pb': '',
    'poland_zabrze_2021_centrum-poludnie.pb': '',
    'poland_zabrze_2021_grzybowice.pb': '',
    'poland_zabrze_2021_guido.pb': '',
    'poland_zabrze_2021_helenka.pb': '',
    'poland_zabrze_2021_konczyce.pb': '',
    'poland_zabrze_2021_maciejow.pb': '',
    'poland_zabrze_2021_makoszowy.pb': '',
    'poland_zabrze_2021_mikulczyce.pb': '',
    'poland_zabrze_2021_osiedle-mikolaja-kopernika.pb': '',
    'poland_zabrze_2021_osiedle-mlodego-gornika.pb': '',
    'poland_zabrze_2021_osiedle-tadeusza-kotarbinskiego.pb': '',
    'poland_zabrze_2021_pawlow.pb': '',
    'poland_zabrze_2021_rokitnica.pb': '',
    'poland_zabrze_2021_zaborze-polnoc.pb': '',
    'poland_zabrze_2021_zaborze-poludnie.pb': '',
    'poland_zabrze_2021_zandka.pb': '',
}

NAMES['katowice_2020'] = {
    # 'poland_katowice_2020_.pb': '',
    'poland_katowice_2020_bogucice.pb': '',
    'poland_katowice_2020_brynow-czesc-wschodnia-osiedle-zgrzebnioka.pb': '',
    'poland_katowice_2020_dab.pb': '',
    'poland_katowice_2020_dabrowka-mala.pb': '',
    'poland_katowice_2020_giszowiec.pb': '',
    'poland_katowice_2020_janow-nikiszowiec.pb': '',
    'poland_katowice_2020_kostuchna.pb': '',
    'poland_katowice_2020_koszutka.pb': '',
    'poland_katowice_2020_ligota-panewniki.pb': '',
    'poland_katowice_2020_murcki.pb': '',
    'poland_katowice_2020_osiedle-paderewskiego-muchowiec.pb': '',
    'poland_katowice_2020_osiedle-tysiaclecia.pb': '',
    'poland_katowice_2020_osiedle-witosa.pb': '',
    'poland_katowice_2020_piotrowice-ochojec.pb': '',
    'poland_katowice_2020_podlesie.pb': '',
    'poland_katowice_2020_srodmiescie.pb': '',
    'poland_katowice_2020_szopienice-burowiec.pb': '',
    'poland_katowice_2020_welnowiec-jozefowiec.pb': '',
    'poland_katowice_2020_zaleska-halda-brynow-czesc-zachodnia.pb': '',
    'poland_katowice_2020_zaleze.pb': '',
    'poland_katowice_2020_zarzecze.pb': '',
    'poland_katowice_2020_zawodzie.pb': '',
}

NAMES['katowice_2021'] = {
    # 'poland_katowice_2021_.pb': '',
    'poland_katowice_2021_bogucice.pb': '',
    'poland_katowice_2021_brynow-czesc-wschodnia-osiedle-zgrzebnioka.pb': '',
    'poland_katowice_2021_dab.pb': '',
    'poland_katowice_2021_dabrowka-mala.pb': '',
    'poland_katowice_2021_giszowiec.pb': '',
    'poland_katowice_2021_janow-nikiszowiec.pb': '',
    'poland_katowice_2021_kostuchna.pb': '',
    'poland_katowice_2021_koszutka.pb': '',
    'poland_katowice_2021_ligota-panewniki.pb': '',
    'poland_katowice_2021_murcki.pb': '',
    'poland_katowice_2021_osiedle-paderewskiego-muchowiec.pb': '',
    'poland_katowice_2021_osiedle-tysiaclecia.pb': '',
    'poland_katowice_2021_osiedle-witosa.pb': '',
    'poland_katowice_2021_piotrowice-ochojec.pb': '',
    'poland_katowice_2021_podlesie.pb': '',
    'poland_katowice_2021_srodmiescie.pb': '',
    'poland_katowice_2021_szopienice-burowiec.pb': '',
    'poland_katowice_2021_welnowiec-jozefowiec.pb': '',
    'poland_katowice_2021_zaleska-halda-brynow-czesc-zachodnia.pb': '',
    'poland_katowice_2021_zaleze.pb': '',
    'poland_katowice_2021_zarzecze.pb': '',
    'poland_katowice_2021_zawodzie.pb': '',
}

NAMES['gdansk_2020'] = {
    # 'poland_gdansk_2020_.pb': '',
    'poland_gdansk_2020_aniolki.pb': '',
    'poland_gdansk_2020_bretowo.pb': '',
    'poland_gdansk_2020_brzezno.pb': '',
    'poland_gdansk_2020_chelm.pb': '',
    'poland_gdansk_2020_jasien.pb': '',
    'poland_gdansk_2020_kokoszki.pb': '',
    'poland_gdansk_2020_krakowiec-gorki-zachodnie.pb': '',
    'poland_gdansk_2020_letnica.pb': '',
    'poland_gdansk_2020_matarnia.pb': '',
    'poland_gdansk_2020_mlyniska.pb': '',
    'poland_gdansk_2020_nowy-port.pb': '',
    'poland_gdansk_2020_oliwa.pb': '',
    'poland_gdansk_2020_olszynka.pb': '',
    'poland_gdansk_2020_orunia-gorna-gdansk-poludnie.pb': '',
    'poland_gdansk_2020_orunia-sw-wojciech-lipce.pb': '',
    'poland_gdansk_2020_osowa.pb': '',
    'poland_gdansk_2020_piecki-migowo.pb': '',
    'poland_gdansk_2020_przerobka.pb': '',
    'poland_gdansk_2020_przymorze-male.pb': '',
    'poland_gdansk_2020_przymorze-wielkie.pb': '',
    'poland_gdansk_2020_rudniki.pb': '',
    'poland_gdansk_2020_siedlce.pb': '',
    'poland_gdansk_2020_srodmiescie.pb': '',
    'poland_gdansk_2020_stogi.pb': '',
    'poland_gdansk_2020_strzyza.pb': '',
    'poland_gdansk_2020_suchanino.pb': '',
    'poland_gdansk_2020_ujescisko-lostowice.pb': '',
    'poland_gdansk_2020_vii-dwor.pb': '',
    'poland_gdansk_2020_wrzeszcz-dolny.pb': '',
    'poland_gdansk_2020_wrzeszcz-gorny.pb': '',
    'poland_gdansk_2020_wyspa-sobieszewska.pb': '',
    'poland_gdansk_2020_wzgorze-mickiewicza.pb': '',
    'poland_gdansk_2020_zabianka-wejhera-jelitkowo-tysiaclecia.pb': '',
    'poland_gdansk_2020_zaspa-mlyniec.pb': '',
    'poland_gdansk_2020_zaspa-rozstaje.pb': '',
}

NAMES['czestochowa_2020'] = {
    # 'poland_czestochowa_2020_.pb': '',
    'poland_czestochowa_2020_bleszno.pb': '',
    'poland_czestochowa_2020_czestochowka-parkitka.pb': '',
    'poland_czestochowa_2020_dzbow.pb': '',
    'poland_czestochowa_2020_gnaszyn-kawodrza.pb': '',
    'poland_czestochowa_2020_grabowka.pb': '',
    'poland_czestochowa_2020_kiedrzyn.pb': '',
    'poland_czestochowa_2020_lisiniec.pb': '',
    'poland_czestochowa_2020_mirow.pb': '',
    'poland_czestochowa_2020_ostatni-grosz.pb': '',
    'poland_czestochowa_2020_podjasnogorska.pb': '',
    'poland_czestochowa_2020_polnoc.pb': '',
    'poland_czestochowa_2020_rakow.pb': '',
    'poland_czestochowa_2020_srodmiescie.pb': '',
    'poland_czestochowa_2020_stare-miasto.pb': '',
    'poland_czestochowa_2020_stradom.pb': '',
    'poland_czestochowa_2020_trzech-wieszczow.pb': '',
    'poland_czestochowa_2020_tysiaclecie.pb': '',
    'poland_czestochowa_2020_wrzosowiak.pb': '',
    'poland_czestochowa_2020_wyczerpy-aniolow.pb': '',
    'poland_czestochowa_2020_zawodzie-dabie.pb': '',
}

def import_data(path):
    meta = {}
    projects = {}
    votes = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        section = ""
        header = []
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ["meta", "projects", "votes"]:
                section = str(row[0]).strip().lower()
                header = next(reader)
            elif section == "meta":
                meta[row[0]] = row[1].strip()
            elif section == "projects":
                projects[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    projects[row[0]][key.strip()] = row[it + 1].strip()
            elif section == "votes":
                votes[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    votes[row[0]][key.strip()] = row[it + 1].strip()
    return meta, projects, votes


if __name__ == "__main__":

    REGIONS = [
        # 'warszawa_2023', 'warszawa_2022', 'warszawa_2021', 'warszawa_2020'
        # 'krakow_2020', 'krakow_2021', 'krakow_2022',
        'wroclaw_2019', 'wroclaw_2020', 'wroclaw_2021',
        # 'zabrze_2020', 'zabrze_2021',
        # 'katowice_2021', 'katowice_2020'
        # 'gdansk_2020'
        # 'czestochowa_2020'
    ]

    costs = []

    for region in REGIONS:

        for name in NAMES[region]:
            path = f"data/{region}/{name}"
            print(path)
            meta, projects, votes = import_data(path)

            for project_id in projects:
                if float(projects[project_id]['votes']) != 0:
                    cost = float(projects[project_id]['cost']) / float(meta['budget'])
                    costs.append(cost)

            plt.xticks(size=25, rotation=65)
            plt.yticks(size=25)
            plt.xlabel('Normalized Project Cost', size=32)
            plt.ylabel('Number of Projects', size=32)

    plt.hist(costs, bins=np.linspace(0, max(costs), 51), color='royalblue')

    # plt.savefig('images/costs/warsaw_costs', bbox_inches='tight')
    # plt.savefig('images/costs/krakow_costs', bbox_inches='tight')
    plt.savefig('images/costs/wroclaw_costs', bbox_inches='tight')
    # plt.savefig('images/costs/zabrze_costs', bbox_inches='tight')
    # plt.savefig('images/costs/katowice_costs', bbox_inches='tight')
    # plt.savefig('images/costs/gdansk_costs', bbox_inches='tight')
    # plt.savefig('images/costs/czestochowa_costs', bbox_inches='tight')

    # plt.show()
