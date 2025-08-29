# Projektna naloga pri UVP

## Opis naloge
Projektna naloga obsega pridobivanje in analizo podatkov s seznama [Best Books of the 21st Century](https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century) na spletni strani [Goodreads](https://www.goodreads.com/).
Sestavljena je iz funkcij v Pythonu in predstavitve rezultatov v Jupyter Notebooku. Pobrala sem prvih 22 strani seznama, na katerih je skupno 2201 recept.
Zajeti podatki vključujejo:
* ID knjige, ki ga ustvari Goodreads,
* naslov,
* avtor,
* povprečna ocena,
* število ocen,
* število recenzij,
* leto izdaje,
* število strani,
* jezik,
* število trenutnih bralcev,
* žanri.

## Navodila za uporabo
Ta program samodejno zbere podatke o knjigah s seznama, tako da prenese HTML strani seznama in posameznih knjig, iz njih izlušči osnovne podatke in jih shrani v CSV datoteko.  

Preden poženete program morate imeti nameščene naslednje pakete: 
* `requests`,
* `pandas`,
* `matplotlib`,
* `seaborn`.  
Zadnji trije so potrebni za ogled datoteke `analiza_podatkov.ipynb`, kjer so pridobljeni podatki obdelani in vizualizirani.  

Ko imate te pakete nameščene, lahko poženete datoteko programa `zajem_podatkov.py`. Program ustvari naslednji mapi in datoteko:
* `goodreads_html/` – sem shrani HTML strani seznama,
* `goodreads_podsamezne_knjige_html/` – sem shrani HTML strani posameznih knjig,
* `goodreads_knjige.csv` – končna datoteka z izluščenimi podatki.

Med izvajanjem se bodo v terminalu izpisovala sporočila, ki bodo opisovala, na kateri točki je trenutno program. Po končanem zagonu se bo izpisalo: "Vsi koraki so uspešno zaključeni."

