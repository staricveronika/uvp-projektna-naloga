import requests
import os
import time
import re
import csv

# OSNOVNE NASTAVITVE

OSNOVNI_URL = "https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century"
IMENIK_HTML = "goodreads_html" # mapa, v katero bomo shranili podatke
CSV_DATOTEKA = "goodreads_knjige.csv" # ime CSV datoteke, v katero bomo shranili podatke
IMENIK_KNJIG_HTML = "goodreads_posamezne_knjige_html" # ime mape, v katero bomo shranili HTML-je posameznih knjig

ZACETNA_STRAN = 20
KONCNA_STRAN = 22

HEADERS = {"User-agent": "Chrome/136.0.7103.114"}

# ZBIRANJE PODATKOV

def shrani_osnovne_htmlje(ZACETNA_STRAN, KONCNA_STRAN):
    """Funkcija shrani HTML strani v mapo."""
    os.makedirs(IMENIK_HTML, exist_ok=True) # ustvari mapo goodreads_html, če še ne obstaja, ne bo napake, če mapa že obstaja

    for stran in range(ZACETNA_STRAN, KONCNA_STRAN + 1):
        url = f"{OSNOVNI_URL}?page={stran}" # sestavi url spletne strani, ki jo želimo pobrati
        print(f"Pobiram stran {stran}: {url}")
        html = requests.get(url, headers=HEADERS) # ta html je objekt, ki vsebuje status kode in vsebino strani

        if html.status_code == 200: # če je zahteva uspešna
            ime_datoteke = os.path.join(IMENIK_HTML, f"stran_{stran}.html") # sestavi pot do datoteke tako, da upošteva operacijski sistem
            with open(ime_datoteke, "w", encoding="utf-8") as f:
                f.write(html.text) # html.text je vsebina HTML strani kot besedilo
            print(f"Stran {stran} shranjena v {ime_datoteke}") # za preverjanje
        else:
            print(f"Napaka pri strani {stran}.")

        time.sleep(1) # počaka 1 sekundo, preden pošlje naslednjo zahtevo, da ne obremeni strežnika

# shrani_osnovne_htmlje(ZACETNA_STRAN, KONCNA_STRAN)

def pridobi_povezave_do_knjig():
    """Funkcija pridobi vse povezave do posameznih knjig znotraj HTML datotek in jih vrne v seznamu."""
    povezave = set() # da preprečimo podvojene url-je
    for ime_datoteke in os.listdir(IMENIK_HTML): # prebere vse html datoteke v mapi goodreads_html
        if ime_datoteke.endswith(".html"):
            pot = os.path.join(IMENIK_HTML, ime_datoteke)
            with open(pot, encoding="utf-8") as f: # odpre posamezno datoteko za branje
                vsebina = f.read()
                najdeno = re.finditer(r'href="/book/show/(\d+)[^"]*"', vsebina) # poišče vse linke, ki kažejo na posamezne knjige
                # \d+ pomeni vsaj eno števko
                # [^"] pomeni vsi znaki, ki niso narekovaj - tako dobimo vse do konca atributa
                for link in najdeno:
                    # sestavimo celoten url
                    povezave.add("https://www.goodreads.com/book/show/" + link.group(1)) # dodamo celoten url v množico, group(1) predstavlja id knjige
                    # https://www.goodreads.com/book/show/ID  
    return list(povezave) # vrne seznam urljev do knjig

povezave = pridobi_povezave_do_knjig()

def shrani_strani_posameznih_knjig(povezave):
    """Funkcija za vsako povezavo do knjige prenese HTML in ga shrani v mapo."""
    os.makedirs(IMENIK_KNJIG_HTML, exist_ok=True) # ustvari mapo, če še ne obstaja
    for povezava in povezave:
        ime_datoteke = povezava.split("/")[-1] + ".html" # ime datoteke naj bo zadnji del url-ja
        # razdelimo url po poševnicah in vzamemo zadnji del, ki je ID knjige
        # dodamo .html, da bo datoteka shranjena kot HTML
        pot = os.path.join(IMENIK_KNJIG_HTML, ime_datoteke) # sestavimo pot do datoteke skupaj z imenom datoteke
        if not os.path.exists(pot): # če pot do datoteke še ne obstaja
            odgovor = requests.get(povezava, headers=HEADERS) # pošljemo zahtevek na url, rezultat shranimo v spremenljivko odgovor
            if odgovor.status_code == 200: # če je zahtevek uspešen
                with open(pot, "w", encoding="utf-8") as f: # odpre datoteko za pisanje
                    f.write(odgovor.text) # vsebino html strani zapišemo v datoteko
                print(f"{ime_datoteke} je shranjena.")
            else:
                print(f"Napaka pri {povezava}.") # če status kode ni 200, izpišemo opozorilo, katera stran ni bila prenesena
            time.sleep(1)
        else:
            print(f"{ime_datoteke} že obstaja.") # če pot do datoteke že obstaja, jo preskočimo - ne prenašamo znova

shrani_strani_posameznih_knjig(povezave)


# # IZLUŠČEVANJE PODATKOV

# def izlusci_osnovne_podatke(od, do): # od in do določata, katere HTML-je obdelamo
#     """Funkcija izlušči osnovne podatke o knjigah iz HTML strani seznama."""
#     # ne odpira posameznih strani knjig, npr. https://www.goodreads.com/book/show/12345
#     # namesto tega odpira HTML-je, ki smo jih shranili s seznama knjig, npr. goodreads_html/stran_1.html, stran_2.html
#     osnovni_podatki = [] # prazen seznam, kamor bomo shranjevali rezultate
#     # vzorec za iskanje osnovnih podatkov o knjigi
#     vzorec = re.compile(
#         r'<a class="bookTitle" href="[^"]+">(?P<naslov>[^<]+)</a>.*?'
#         r'<a class="authorName" href="[^"]+">(?P<avtor>[^<]+)</a>.*?'
#         r'<span class="minirating">(?P<povp_ocena>[\d\.]+) avg rating.*?(?:\n.*?)*?(?P<leto_izdaje>\d{4})?</span>'
#         r'<span class="minirating">\s*(?P<povp_ocena>[\d\.]+) avg rating — (?P<st_ocen>[\d,]+) ratings — (?P<st_recenzij>[\d,]+) reviews',
#         re.DOTALL
#     )
#     # re.compile(vzorec) ustvari objekt regularnega izraza, ki ga lahko večkrat uporabimo za iskanje, ujemanje, zamenjave
#     # poišče <a class="bookTitle" href="[^"]+"> ... </a>.*?
#     # (?P<ime_knjige>[^<]+) pomeni: shrani vse znake do < v skupino ime_knjige
#     # (?P<leto_izdaje>\d{4})? --> če obstaja, zajame 4-mestno število (leto izdaje)

#     for stran in range(od, do + 1):
#         pot = os.path.join(IMENIK_HTML, f"stran_{stran}.html") # sestavi pot do ustrezne datoteke, npr. goodreads_html/stran_1.html
#         with open(pot, encoding="utf-8") as f:
#             vsebina = f.read() # preberemo HTML vsebino
#             for najdba in vzorec.finditer(vsebina): # poiščemo vsa ujemanja regexa v datoteki
#                 naslov = najdba["naslov"].strip() # najdba["ime_knjige"] vzame zajeti naslov knjige
#                 avtor = najdba["avtor"].strip()
#                 povp_ocena = float(najdba["ocena"]) # oceno pretvori v decimalno število
#                 st_ocen = int(najdba["st_ocen"].replace(",", ""))
#                 st_recenzij = int(najdba["st_recenzij"].replace(",", ""))
#                 leto_izdaje = najdba["leto_izdaje"].strip() if najdba["leto_izdaje"] else None # če regex ne ujame leta, vrne None
#                 osnovni_podatki.append((naslov, avtor, povp_ocena, st_ocen, st_recenzij, leto_izdaje))
#     return osnovni_podatki

# def izlusci_podrobne_podatke_iz_knjige(osnovni_podatki):
#     podrobni_podatki = []

#     for knjiga in osnovni_podatki:
#         naslov = knjiga[0]
#         avtor = knjiga[1]
#         ocena = knjiga[2]
#         st_ocen = knjiga[3]
#         st_recenzij = knjiga[4]
#         leto_izdaje = knjiga[5]

#         ime_datoteke = naslov.replace(" ", "_") + ".html"
#         pot = os.path.join(IMENIK_KNJIG_HTML, ime_datoteke)

#         # Privzete vrednosti
#         st_strani = None
#         jezik = None
#         st_trenutnih_bralcev = 0
#         zanri_niz = 
    

#     for ime_datoteke in os.listdir(IMENIK_KNJIG_HTML):
#         if ime_datoteke.endswith(".html"):
#             pot = os.path.join(IMENIK_KNJIG_HTML, ime_datoteke)
#             with open(pot, encoding="utf-8") as f:
#                 vsebina = f.read()

#             # Število strani
#             st_strani = re.search(r'(\d+) pages', vsebina)
#             st_strani = int(st_strani.group(1)) if st_strani else None

#             # Jezik
#             jezik = re.search(r'Language\s*</div>\s*<div[^>]*>\s*([^<]+)', vsebina)
#             jezik = jezik.group(1).strip() if jezik else None

#             # Število ljudi, ki trenutno berejo knjigo
#             st_trenutnih_bralcev = re.search(r'(\d[\d,]*) people are currently reading', vsebina)
#             st_trenutnih_bralcev = int(st_trenutnih_bralcev.group(1).replace(",", "")) if st_trenutnih_bralcev else 0

#             # Žanri
#             zanri = re.findall(r'<a class="actionLinkLite bookPageGenreLink"[^>]*>([^<]+)</a>', vsebina)
#             zanri = [z.strip() for z in zanri] # odstrani morebitne presledke
#             zanri_niz = ", ".join(zanri) if zanri else None # združi v en niz, ločen z vejicami

#             podrobni_podatki.append({
#                 "st_strani": st_strani,
#                 "jezik": jezik,
#                 "st_trenutnih_bralcev": st_trenutnih_bralcev,
#                 "zanri": zanri_niz
#             })

#     return podrobni_podatki