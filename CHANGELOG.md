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

## [0.1.4] - 2026-06-18

## Změny: Přidána podpora ovládání pro PC (Myš & Klávesnice)

Hra nyní plně podporuje hraní na počítači. Dosud bylo možné hru ovládat pouze na dotykových zařízeních, ovládací prvky a logika rozhraní ale byly aktualizovány tak, aby plynule reagovaly i na standardní PC periferie.

### Nové
* **Podpora myši:** Všechna herní a UI tlačítka na obrazovce nyní reagují na události myši (`mousedown`, `mouseup`, `mouseleave`).
* **Podpora klávesnice:** Přidáni globální posluchači událostí (`keydown`, `keyup`) pro pohodlné hraní bez nutnosti klikat na UI prvky.
* **Mapování kláves:**
    * `Šipky` nebo `W A S D` – Pohyb okurky a míření
    * `Mezerník (Space)` – Zahájení a ukončení střelby (nabíjení síly)
    * `Enter` nebo `Shift` – Skok
    * `Tab` – Přepínání aktivní okurky
    * `Escape` – Otevření menu / Pauza

### Změněno
* **Klientská logika (`index.html`):** Upravena pomocná funkce `setupBtn` a individuální posluchače událostí u tlačítek střelby, skoku a zbraní. Nyní paralelně obsluhují dotykové (`touchstart`, `touchend`) i myší události tak, aby se na různých zařízeních navzájem neblokovaly a nezpůsobovaly nechtěné dvojité kliky (např. prevence u `Space` a `Enter`).

## [0.1.5] - 2026-07-14

### Bugfix: Paměť předchozích tahů (`app.py`)

**Problém:** Po přepnutí tahu hra vždy zvolila prvního živého červa v pořadí týmu místo toho, se kterým hráč hrál naposledy.

- `find_next_alive_worm()` — nyní nejprve zkusí vrátit naposledy hraného červa daného týmu (pokud je stále naživu); na prvního v pořadí spadne jen když mezitím zemřel.
- Přidán `last_active_worm` do herního stavu — pro každý tým si pamatuje ID naposledy aktivního červa.
- `last_active_worm` se aktualizuje na obou místech, kde dochází ke změně `active_worm_id`: `handle_next_turn` (konec tahu) a `handle_switch_worm` (ruční přepnutí).

**Vedlejší oprava:** Celý `app.py` byl uložen v kódování Windows-1250 místo UTF-8, což způsobovalo `SyntaxError` při každém spuštění. Převedeno na čisté UTF-8 (pouze přeznačení kódování, žádná změna logiky).

### Bugfix: Zaseknutý zvuk nabíjení (`index.html`)

**Problém:** Zvuk nabíjení zbraně se občas zasekl v permanentní smyčce, řešitelné jen obnovením stránky.

- `startChargeSound()` — nyní před vytvořením nového oscilátoru vždy nejprve tvrdě zastaví a odpojí případný předchozí běžící (dřív se při dvojím volání reference přepsala a starý oscilátor osaměl bez možnosti ho vypnout).
- `handleShootStart` — přidána ochrana proti duplicitnímu spuštění (řeší typický spouštěč: `touchstart` + syntetický `mousedown` na jeden dotyk na mobilu).
- `state_update` handler — při přepnutí tahu se nyní vždy uklidí běžící nabíjecí zvuk i interval (řeší případ, kdy tah skončí, např. vypršením časového limitu, zatímco hráč držel tlačítko a nabíjel výstřel).

## [0.1.6] - 2026-07-15

### Opraveno
- **Zvukový bug na začátku nové hry**: efekty `win_fanfare.mp3` a `explosion_grave.mp3` se občas přehrály hned po startu nové hry, ještě než okurky dopadly na zem.
  - Příčina: `state_update` patřící ještě staré hře (poslední exploze před restartem) mohl kvůli threading race na serveru (`async_mode='threading'`, žádný zámek na `game_state`) dorazit klientovi *po* `init_state` nové hry, takže se zpracoval, jako by patřil té nové.
  - Řešení: po přijetí `init_state` se na 1000 ms zablokuje přehrávání `win_fanfare` a `explosion_grave` (hudba není dotčena — jede mimo `playSound()`).
  - Soubor: `index.html` (přidána konstanta `NEW_GAME_SOUND_LOCK_MS` a proměnná `newGameSoundLockUntil`; 3 podmíněná místa: `init_state`, `updateUI()`, `executeExplosion()`).
  - `app.py` beze změny.
 
## [0.1.7] - 2026-07-16
    
### Oprava síťové synchronizace a oživování (Server-side)
**Opravené chyby (Bug Fixes):**
 * **Zmrtvýchvstání okurek:** Opravena kritická chyba, která způsobovala, že se mrtvé nebo těžce zraněné okurky po chvíli zhmotnily s původním počtem HP.
 * **Race condition u brokovnicových zbraní:** Vyřešen problém se synchronizací poškození u zbraní, které střílejí více projektilů najednou (Lupara, S686). Opožděné pakety (kvůli síťové latenci/pingu) už nebudou přepisovat reálný stav serveru staršími údaji.
**Technické změny v kódu (app.py):**
 * **Event sync_worm:** Přidána striktní validace příchozího zdraví. Server nyní přijme novou hodnotu HP od klienta pouze za předpokladu, že je *nižší* než hodnota, kterou má server aktuálně uloženou v paměti.
 * **Event client_explosion:** Změněna logika zpracování hromadného updatu stavu po výbuchu. Server již bezhlavě nepřepisuje celý slovník worms daty ze zpožděného klienta. Místo toho iteruje přes jednotlivé okurky, bezpečně aktualizuje jejich souřadnice (x, y, úhel) a u HP opět kontroluje, zda dochází pouze k jeho poklesu.
**Poznámka k mechanikám:**
 * **Léčení (Lékárničky):** Tato oprava nijak nerozbíjí mechaniku sbírání lékárniček (které HP naopak zvyšují). Přičítání HP z beden je totiž řešeno samostatným, plně serverovým eventem (collect_crate), který není závislý na klientských zpožděních.

**Oprava: předčasné přepnutí tahu na padající okurku**

- `next_turn` handler teď před přepnutím aktivního hráče čeká 1000 ms (`time.sleep(1.0)`), místo aby přepínal okamžitě.
- Původní logika přepnutí (výběr týmu, reset `weapon_used_this_turn`, nový `wind`, `find_next_alive_worm`) přesunuta beze změny do nové funkce `_perform_next_turn()`, volané až po prodlevě.
- Díky prodlevě stihnou doběhnout eventy z fyziky pádu (`sync_worm`, `client_explosion`) a zapsat aktuální `hp` do `game_state` dřív, než se vybírá další aktivní hráč — pokud okurka pádem zemře, `find_next_alive_worm` ji už nevybere a sáhne po jiné živé okurce z týmu.
- Broadcast po prodlevě přepsán z `emit(..., broadcast=True)` na `socketio.emit(...)` — funkčně shodné (odešle všem připojeným), ale nezávisí na zachování Flask request kontextu přes `time.sleep`.

Žádné jiné chování, endpointy ani datové struktury nedotčeny.
