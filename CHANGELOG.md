# Changelog

## [0.1.0] - 2026-06-13
První verze Pickles

## [0.1.1] - 2026-06-14

### Opraveno
- **AI zámek zbraně po prvním výstřelu z brokovnice/lupary** – AI již nemůže po prvním výstřelu z brokovnice nebo lupary přepnout na jinou zbraň. Dříve mohl tento bug způsobit, že AI v jednom tahu vystřelila například z brokovnice a poté z bazuky. Nyní AI musí buď vystřelit znovu stejnou zbraní, nebo počkat na timeout tahu.

### Přidáno
- **Možnost přeskočit tah po prvním výstřelu z brokovnice/lupary** – Hráč nyní může po prvním výstřelu z brokovnice nebo lupary tah přeskočit tlačítkem ⏭ a ušetřit tak druhý náboj. Dříve hra po prvním výstřelu vždy vyžadovala i druhý výstřel.
  
## [0.1.2] - 2026-06-15

### Opraveno
- Zaseknutí zvuku nabíjení zbraně při utopení aktivní okurky před výstřelem
- Zamrznutí hry při současném výbuchu více min (řetězové exploze nyní probíhají sekvenčně)
- AI nesprávně nabíjela direct-fire zbraně (M79, shotgun, lupara, uzi, plasma, railgun)
- Náhodné přehrávání zvuků při načtení nové hry způsobené předčasným preloadem audio souborů

### Změněno
- Munice snížena: frag, M79, uzi, plazma, molotov, railgun `10 → 2`; shotgun, lupara `20 → 4`; bazuka a granát zůstávají neomezené
- Damage všech zbraní snížen na polovinu (bazooka `50 → 25`, granát `65 → 32`, railgun `85 → 42`, mina `50 → 25` atd.)
- Burn damage molotovu snížen `3 → 1` HP za tick

## [0.1.3] - 2026-06-17

###  Opravy chyb

* **Zobrazení zbraní:** Opravena vizuální chyba, kdy se UI předčasně přepínalo na bazuku při střelbě posledního zásobníku z Uzi nebo Plasmy. Zbraň se nyní přepne zpět na výchozí až po úplném dokončení animace střelby.

* **Stabilita enginu (Zamrzání):** Opraven kritický bug způsobující zamrznutí nebo pád herní smyčky při hromadných explozích. Přidány bezpečnostní pojistky (kontroly na `undefined` objekty) do `executeExplosion` a hlavní smyčky pro korektní zpracování současně zničených entit (miny, bedny, hroby).

###  Vylepšení

* **UI Munice:** Zvýšen práh pro zobrazení varování o nízkém stavu munice (červené zbarvení odznaku) u vícestranných zbraní (Brokovnice, Lupara) z původních 2 na 4 zbývající náboje.
