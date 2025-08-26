import requests
import os
import time


# Osnovne nastavitve
OSNOVNI_URL = "https://www.goodreads.com/list/show/143500.Best_Books_of_the_Decade_2020_s?ref=ls_fl_0_seeall"
IMENIK_HTML = "goodreads_html" # mapa, v katero bomo shranili podatke
CSV_DATOTEKA = "goodreads_knjige.csv" # ime CSV datoteke, v katero bomo shranili podatke

ZACETNA_STRAN = 1
KONCNA_STRAN = 20

# ZBIRANJE PODATKOV

HEADERS = {"User-agent": "Chrome/136.0.7103.114"}

def shrani_osnovne_htmlje(ZACETNA_STRAN, KONCNA_STRAN):
    """Funkcija shrani HTML strani."""
    os.makedirs(IMENIK_HTML, exist_ok=True) # ustvari mapo, če je še ni

    for stran in range(ZACETNA_STRAN, KONCNA_STRAN + 1):
        url = f"{OSNOVNI_URL}?page={stran}"
        print(f"Pobiram stran {stran}: {url}")
        html = requests.get(url, headers=HEADERS)

        if html.status_code == 200:
            ime_datoteke = os.path.join(IMENIK_HTML, f"stran_{stran}.html")
            with open(ime_datoteke, "w", encoding="utf-8") as f:
                f.write(html.text)
            # print(f"Stran {stran} shranjena v {ime_datoteke}") # za preverjanje
        else:
            print(f"Napaka pri strani {stran}.")

        time.sleep(1) # počakamo 1 sekundo, da ne obremenimo strežnika

shrani_osnovne_htmlje(ZACETNA_STRAN, KONCNA_STRAN)
