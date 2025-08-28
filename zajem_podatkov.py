import requests
import os
import time
import re
import csv
import html

# OSNOVNE NASTAVITVE

OSNOVNI_URL = "https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century"
IMENIK_HTML = "goodreads_html" # mapa, v katero bomo shranili podatke
CSV_DATOTEKA = "goodreads_knjige.csv" # ime CSV datoteke, v katero bomo shranili podatke
IMENIK_KNJIG_HTML = "goodreads_posamezne_knjige_html" # ime mape, v katero bomo shranili HTML-je posameznih knjig

ZACETNA_STRAN = 1
KONCNA_STRAN = 30

HEADERS = {"User-agent": "Chrome/136.0.7103.114"}

# ZBIRANJE PODATKOV

def shrani_osnovne_htmlje(ZACETNA_STRAN, KONCNA_STRAN):
    """Funkcija shrani HTML strani v mapo."""
    os.makedirs(IMENIK_HTML, exist_ok=True) # ustvari mapo goodreads_html, če še ne obstaja, ne bo napake, če mapa že obstaja

    for stran in range(ZACETNA_STRAN, KONCNA_STRAN + 1):
        url = f"{OSNOVNI_URL}?page={stran}" # sestavi url spletne strani, ki jo želimo pobrati
        print(f"Pobiram stran {stran}: {url}")
        html = requests.get(url, headers=HEADERS)

        if html.status_code == 200: # če je zahteva uspešna
            ime_datoteke = os.path.join(IMENIK_HTML, f"stran_{stran}.html")
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
            with open(pot, encoding="utf-8") as f:
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

# shrani_strani_posameznih_knjig(povezave)

# IZLUŠČIMO PODATKE
def pocisti_besedilo(besedilo):
    """Odstrani odvečne presledke in HTML entitete, ki se pojavijo v HTML."""
    if besedilo:
        besedilo = html.unescape(besedilo)    # &amp; spremeni v &
        besedilo = " ".join(besedilo.split()) # odstrani večkratne presledke
        return besedilo
    return None

def izlusci_osnovne_podatke(od, do):
    """Funkcija izlušči osnovne podatke o knjigah iz HTML strani seznama."""
    # ne odpira posameznih strani knjig, npr. https://www.goodreads.com/book/show/12345
    # namesto tega odpira HTML-je, ki smo jih shranili s seznama knjig, npr. goodreads_html/stran_1.html, stran_2.html
    osnovni_podatki = []
    vzorec = re.compile(
    r'<tr itemscope itemtype="http://schema.org/Book">.*?'
    r'data-resource-id="(?P<id_knjige>\d+)".*?'
    r'<a\s+class="bookTitle"[^>]*>.*?<span[^>]*>(?P<naslov>.*?)</span>.*?</a>'
    r'.*?<a\s+class="authorName"[^>]*>.*?<span[^>]*>(?P<avtor>.*?)</span>.*?</a>'
    r'.*?(?P<povp_ocena>\d+\.\d+)\s+avg rating.*?(?P<st_ocen>[\d,]+)\s+ratings',
    re.DOTALL
    )

    for stran in range(od, do + 1):
        pot = os.path.join(IMENIK_HTML, f"stran_{stran}.html") # sestavi pot do ustrezne datoteke, npr. goodreads_html/stran_1.html
        with open(pot, encoding="utf-8") as f:
            vsebina = f.read()
            for najdba in vzorec.finditer(vsebina):
                id_knjige = int(najdba["id_knjige"])
                naslov = pocisti_besedilo(najdba["naslov"]) # najdba["ime_knjige"] vzame zajeti naslov knjige
                avtor = pocisti_besedilo(najdba["avtor"])
                povp_ocena = float(najdba["povp_ocena"]) # oceno pretvori v decimalno število
                st_ocen = int(najdba["st_ocen"].replace(",", ""))
                osnovni_podatki.append((id_knjige, naslov, avtor, povp_ocena, st_ocen))
    return osnovni_podatki

def izlusci_podrobne_podatke_iz_knjige(osnovni_podatki):
    podrobni_podatki = []

    for knjiga in osnovni_podatki: # osnovni podatki je seznam tuplov
        id_knjige = knjiga[0]
        naslov = knjiga[1]
        avtor = knjiga[2]
        povp_ocena = knjiga[3]
        st_ocen = knjiga[4]

        ime_datoteke = f"{id_knjige}.html"
        pot = os.path.join(IMENIK_KNJIG_HTML, ime_datoteke)
        with open(pot, encoding="utf-8") as f:
            vsebina = f.read()

        # Privzete vrednosti
        st_strani = None
        jezik = None
        leto_izdaje = None
        st_trenutnih_bralcev = 0
        zanri_niz = None
        st_recenzij = 0
        
        # Število strani
        st_strani_re = re.search(r'(\d+)\s+pages', vsebina)
        st_strani = int(st_strani_re.group(1)) if st_strani_re else None

        # Jezik
        jezik_re = re.search(r'"inLanguage"\s*:\s*"([^"]+)"', vsebina)
        jezik = jezik_re.group(1) if jezik_re else None

        # Leto izdaje
        # podatek o tem je zapisan v JSON skripti na HTML strani
        import datetime
        vzorec = re.search(r'"publicationTime":\s*(\d+)', vsebina)  # poišče v HTML vrstico kot je "publicationTime":1234567800000
        # publicationTime je zapisan v UTC (Coordinated Universal Time)
        if vzorec:
            timestamp_v_sekundah = int(vzorec.group(1)) / 1000 # pretvorimo timestamp iz milisekund v sekunde (delimo s 1000)
            datum_v_utc = datetime.datetime.utcfromtimestamp(timestamp_v_sekundah) # iz timestampa naredimo datum (v UTC času)
            # funkcija utcfromtimestamp pretvori timestamp pretvori v normalen datum
            # rezultat je recimo 2004-09-14 00:00:00
            leto_izdaje = datum_v_utc.year # iz objekta datetime vrnemo samo leto --> 2004
        else:
            leto_izdaje = None # če timestamp ni najden, vrnemo None
    

        # Trenutni bralci
        trenutni_bralci_re = re.search(r'([\d,]+)\s+people\s+are\s+currently\s+reading', vsebina)
        st_trenutnih_bralcev = int(trenutni_bralci_re.group(1).replace(",", "")) if trenutni_bralci_re else 0

        # Žanri
        zanri_re = re.findall(r'"bookGenres":\s*\[.*?\]', vsebina, re.DOTALL)
        if zanri_re:
            # poiščemo vse "name":"..." znotraj tega bloka
            imena_zanrov = re.findall(r'"name":"(.*?)"', zanri_re[0])
            zanri_niz = ", ".join(imena_zanrov)
        else:
            zanri_niz = None

        # Število recenzij
        st_recenzij_re = re.search(r'([\d,]+)\s+reviews', vsebina)
        st_recenzij = int(st_recenzij_re.group(1).replace(",", "")) if st_recenzij_re else 0

        # Združi osnovne in podrobne podatke
        podrobni_podatki.append({
            "id_knjige": id_knjige,
            "naslov": naslov,
            "avtor": avtor,
            "povp_ocena": povp_ocena,
            "st_ocen": st_ocen,
            "st_recenzij": st_recenzij,
            "leto_izdaje": leto_izdaje,
            "st_strani": st_strani,
            "jezik": jezik,
            "st_trenutnih_bralcev": st_trenutnih_bralcev,
            "zanri": zanri_niz
        })

    return podrobni_podatki

# SHRANIMO V CSV

def shrani_v_csv(podrobni_podatki):
    with open(CSV_DATOTEKA, "w", newline="", encoding="utf-8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow([
            "id_knjige",
            "naslov",
            "avtor",
            "povp_ocena",
            "st_ocen",
            "st_recenzij",
            "leto_izdaje",
            "st_strani",
            "jezik",
            "st_trenutnih_bralcev",
            "zanri"
        ])
        for knjiga in podrobni_podatki:
            pisatelj.writerow([
                knjiga["id_knjige"],
                knjiga["naslov"],
                knjiga["avtor"],
                knjiga["povp_ocena"],
                knjiga["st_ocen"],
                knjiga["st_recenzij"],
                knjiga["leto_izdaje"],
                knjiga["st_strani"],
                knjiga["jezik"],
                knjiga["st_trenutnih_bralcev"],
                knjiga["zanri"]
            ])

    print(f"Podatki shranjeni v {CSV_DATOTEKA}.")

def main(zacetna_stran=ZACETNA_STRAN, koncna_stran=KONCNA_STRAN):
    # 1. Prenos HTML strani seznama
    shrani_osnovne_htmlje(zacetna_stran, koncna_stran)

    # 2. Pridobitev povezav do posameznih knjig
    povezave = pridobi_povezave_do_knjig()

    # 3. Prenos HTML strani posameznih knjig
    shrani_strani_posameznih_knjig(povezave)

    # 4. Izluščevanje osnovnih podatkov
    osnovni_podatki = izlusci_osnovne_podatke(zacetna_stran, koncna_stran)

    # 5. Izluščenje podrobnih podatkov
    podrobni_podatki = izlusci_podrobne_podatke_iz_knjige(osnovni_podatki)

    # 6. Shrani v CSV
    shrani_v_csv(podrobni_podatki)

    print("Vsi koraki so uspešno zaključeni.")


# Ta del poskrbi, da se program izvrši samo, če datoteko poganjamo direktno, ne pa če jo uvozimo kot modul:
if __name__ == "__main__":
    main()