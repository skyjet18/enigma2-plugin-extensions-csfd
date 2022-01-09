# enigma2-plugin-extensions-csfd
Plugin pre enigma2 pre zobrazenie informácií o filmoch z csfd.cz. Vyžaduje python 2.7 - pod python 3.x zatiaľ nefunguje.

## Čo funguje
- Zobrazenie popisu filmu ako jeho hodnotenie, obsah, herci, réžia, ...
- Zobrazenie posteru k filmu
- Zobrazenie galérie obrázkov a videii
- Zobrazenie recenzií a hodnotenie
- Vyhľadávanie podobných a súvisiacich filmov
- Zaujímavosti z filmu

## Nepodporované/neimplementované
- Prihásenie do csfd a veci s tým súvisiace ako vlastné hodnotenie, možnosť hodnotenia, ...
- Načítavanie zoznamu filmov do cache podľa aktuálnej stanice a s tým súvisiace presné vyhľadávanie filmov

## Inštalácia ipk
Stiahnuť z release súbor `enigma2-plugin-extensions-csfd_XX-XX-XXXXXXXX_all.ipk` a v prípade prvotnej inštalácie aj `python-oauthlib_3.1.0_all.ipk` a `python-requests_oauthlib_1.3.0_all.ipk` ktoré sú pribalené k release 15.00 do prijímača

### Pri prvej inštalácii je potrebné najprv nainštalovať plugin + závislosti
```
opkg install python-oauthlib_3.1.0_all.ipk python-requests_oauthlib_1.3.0_all.ipk enigma2-plugin-extensions-csfd_XX-XX-XXXXXXXX_all.ipk
```
### Pri každej ďalšej aktualizácii stačí
```
opkg install enigma2-plugin-extensions-csfd_XX-XX-XXXXXXXX_all.ipk
```
## Inštalácia deb
Stiahnuť z release súbor `enigma2-plugin-extensions-csfd_XX-XX-XXXXXXXX_all.deb` a v prípade prvotnej inštalácie aj `python-oauthlib_3.1.0_all.deb` a `python-requests_oauthlib_1.3.0_all.deb` ktoré sú pribalené k release 15.00 do prijímača

### Pri prvej inštalácii je potrebné najprv nainštalovať plugin + závislosti
```
dpkg -i python-oauthlib_3.1.0_all.deb python-requests_oauthlib_1.3.0_all.deb enigma2-plugin-extensions-csfd_XX-XX-XXXXXXXX_all.deb
```
### Pri každej ďalšej aktualizácii stačí
```
dpkg -i install enigma2-plugin-extensions-csfd_XX-XX-XXXXXXXX_all.deb
```
