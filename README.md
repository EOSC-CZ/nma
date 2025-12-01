# NMA

URLcka pro integraci NMA s RIVem

GET /riv/register  - vraci stranku s formularem, jedno policko "pid"
POST /riv/register - prijima formular s "pid"
GET /datasets/<pid>/edit - stranka s formularem pro editaci udaju o datasetu
GET /datasets/<pid> - landing page datasetu

pid:
    doi:10.5072/FK2/XXXXX
    handle:12345/XXXXX

/riv/register - flask view funkce, zadny resource/resource config

Metadata resolving:

- riv/resolvers/base.py - zakladni trida a funkce pro resolvovani metadat
- riv/resolvers/<resolver>.py - jednotlive resolvery

Resolve probiha tak, ze se jeden po druhem zkousi vsechny resolvery, dokud nektery nenajde metadata.

PID se bere tak, ze se vezme z metadat persistent_url, matchne oproti PERSISTENT_IDENTIFIER_PREFIXES v konfiguraci a podle toho se urci typ identifikatoru (doi, handle) a vyextrahuje se samotny identifikator. Vysledek bude vypadat jako:
  doi:10.5072/FK2/XXXXX nebo handle:12345/XXXXX