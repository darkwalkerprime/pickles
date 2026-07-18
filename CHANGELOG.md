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

## [0.1.8] - 2026-07-16

### Opraveno
- **Nefungující lékárničky (Zrušené léčení)** – Opraven kritický bug, kdy sebrání lékárničky okurku občas vůbec nevyléčilo. 
  - **Příčina:** Šlo o síťovou *race condition* způsobenou nedávno přidanou striktní validací HP na serveru (která měla zabránit zmrtvýchvstání). Opožděné pakety z klienta o pohybu či fyzice nesly starou (nižší) hodnotu HP. Server tuto zpožděnou starou hodnotu mylně vyhodnotil jako nově obdržené poškození a čerstvě přičtené zdraví z lékárničky okamžitě smazal.
  - **Řešení (`app.py`):** Do eventu `collect_crate` byl přidán ochranný časový zámek (`heal_lock_until`). Server nyní u dané okurky po dobu 1 sekundy od vyléčení ignoruje klientské updaty zdraví (`sync_worm`, `client_explosion`), které by HP snižovaly. Klient tak dostane bezpečný prostor pro synchronizaci nového stavu zdraví.

## [0.1.9] - 2026-07-17

### Opraveno
- **Chybějící zámek pro `explosion_mine.mp3` na začátku nové hry** – Doplnění opravy z 0.1.6, na kterou se tehdy zapomnělo u tohoto konkrétního zvuku.
  - Příčina: stejná jako u `win_fanfare`/`explosion_grave` v 0.1.6 (opožděný `state_update` staré hry dorazí klientovi až po `init_state` nové hry), ale zámek `newGameSoundLockUntil` v `executeExplosion()` tehdy pokrýval jen `type === 'grave'`, nikoli `type === 'mine'`.
  - Řešení: podmínka v `executeExplosion()` nyní blokuje přehrání i pro `type === 'mine'`, po stejnou dobu `NEW_GAME_SOUND_LOCK_MS` jako u `grave`. Aktualizován i vysvětlující komentář nad `NEW_GAME_SOUND_LOCK_MS`.
  - Soubor: `index.html` (žádné nové proměnné, jen rozšíření stávající podmínky a komentáře).
  - `app.py` beze změny.

- **Herní zvuky a hudba pronikající do menu / mezi hrami** – Po ukončení hry (návrat do menu) nebo po jejím restartu mohly dozvučující efekty jako `airdrop.mp3` nebo `molotov_fire.mp3` (smyčka hoření) pokračovat v přehrávání i mimo hru; při ukončení hry během držení tlačítka "PAL!" se stejně choval i zvuk nabíjení zbraně.
  - Příčina: jednorázové efekty se přehrávají přes `soundCache[type].cloneNode()` uvnitř `playSound()`, takže po zavolání k nim nezůstávala žádná trvalá reference a nešlo je hromadně zastavit. Zvuk nabíjení (`chargeOsc`, Web Audio oscilátor vázaný na tlačítko "PAL!") a smyčka `molotov_fire` neměly při odchodu z hry ani při restartu žádný úklid.
  - Řešení: přidáno sledované pole `activeClonedSounds` (naplňuje/vyprazdňuje `playSound()` přes `ended`/`error` listenery) a nová funkce `stopAllGameSounds()`, která zastaví všechny sledované klony, smyčku `molotov_fire`, `chargeOsc`/`powerInterval` a skryje ukazatel síly výstřelu. Zavolána při ukončení hry (`btnConfirmExit`), návratu z obrazovky konce hry (`btnBackToMenu`) a na začátku každé nové hry/restartu (`init_state` handler) — takže konec hry i restart nyní vždy umlčí všechny herní zvuky i hudbu dané mapy, a nová hra je znovu spustí od čista.
  - Soubor: `index.html` (nová proměnná `activeClonedSounds`, nová funkce `stopAllGameSounds()`, 3 nová volací místa; drobná úprava `playSound()` pro sledování klonů).
  - `app.py` beze změny (oba bugy jsou čistě klientská záležitost přehrávání zvuku).
 
## [0.2.0] - 2026-07-18

**Opraveno**
- Vykreslování vody u pravého okraje mapy (index.html) — vlna se přestávala kreslit 5 px před okrajem plátna a vytvářela dojem neviditelné bariéry držící vodu ve vzduchu. Opraveno u zadní i přední vrstvy vody (výplň i obrysová linka).
- Granát/frag prolétal skrz okurky (index.html) — chyběla kolizní kontrola s hitboxem okurky, projektil testoval jen terén. Granát/frag se nyní od zasažené okurky odrazí (stejně jako od terénu) a nemůže se v ní zaseknout.
- Granát/frag hozený přímo pod sebe se teleportoval nad hlavu okurky místo dopadu na zem (index.html) — nový bug způsobený předchozí opravou. Výpočet bodu odrazu couval proti vektoru rychlosti, což při téměř svislém pádu vytáhlo granát vysoko nad hitbox. Nyní se počítá nejbližší hrana hitboxu, takže granát skončí těsně u strany, ze které přiletěl.

**Beze změny**
- app.py — s žádnou z oprav nesouvisel, ponechán v původním stavu.
