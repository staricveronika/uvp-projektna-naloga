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


## Hipoteze
### Razmerje med ocenami in popularnostjo
* Knjige z več ocenami imajo bolj stabilno povprečno oceno (morda bližje 4 ali 4,5).
    - Potrebni podatki: 'st_ocen', 'povprecna_ocena'.
    - Analiza: Scatter plot ratings_count vs average_rating.

* Manj ocenjene knjige imajo ekstremnejše ocene.
    - Potrebni podatki: 'st_ocen', 'povprecna_ocena'.
    - Analiza: Histogram average_rating za manj ocenjene knjige.

* Top 10 knjig po oceni vs. top 10 knjig po številu ocen - kako se razlikujeta?

### Analiza ocen
* Povprečna ocena knjig je običajno med 4 in 4,5.
* Standardni odklon pokaže, katere knjige so "kontroverzne".


### Analiza avtorjev
* Avtorji, ki imajo na seznamu več knjig, imajo povprečno višje ocene.
    - Potrebni podatki: 'avtor', 'povprecna_ocena'
    - Analiza: Group by 'avtor', povprečje ocen, bar chart top avtorjev.

* Avtorji, ki pišejo v določenih žanrih, imajo boljše povprečne ocene.

### Analiza žanrov
* Nekateri žanri so na seznamu bolj zastopani.
    - Potrebni podatki: 'zanr'.
    - Aanliza: Bar chart števila knjig po žanru.

* Kateri žanr je najbolj zastopan?

* Fantazijske knjige imajo višje povprečne ocene.
    - Potrebni podatki: 'zanr', 'povprecna_ocena'.
    - Analiza: Box plot 'povprecna_ocena' po žanru.

### Analiza leta izdaje
* Najbolje ocenjene knjige so pogosto izdane pred več leti (več časa za zbiranje ocen).
    - Potrebni podatki: 'leto_izdaje', 'povprecna_ocena'.
    - Analiza: scatter plot 'leto_izdaje' vs 'povprecna_ocena'.

* Ali določeno leto izida izstopa z več (/bolje ocenjenimi knjigami)?
    - Potrebni podatki: leto_izdaje.
    - Analiza: Histogram po letu izdaje.


* Novejše knjige imajo manj ocen (a morda višje povprečne ocene, ker se jih aktivno promovira).
    - Potrebni podatki: 'leto_izdaje', 'st_ocen'.
    - Analiza: scatter plot: 'leto_izdaje' vs 'st_ocen'.

### Analiza dolžine knjig
* Daljše knjige so bolje ocenjene (ker ti more bit knjiga všeč da jo sploh do konca prebereš).
    - Potrebni podatki: 'st_strani', 'povprecna_ocena'.
    - Analiza: Scatter plot.

### Analiza recenzij
* Knjige z zelo velikim številom ocen imajo tudi več recenij.
    - Analiza: Scatter plot 'st_ocen' vs. 'st_recenzij'.

 
