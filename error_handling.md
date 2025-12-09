# Error handling

1. Spatny format urlcka - nepodarilo se rozpoznat jako podporovany persistentni identifikator.

   * Zobrazit jako: "Identifikator neni podporovan.", uz tam je seznam persistentnich identifikatoru
   * Pridat odkaz na support a odkazat na nej uzivatele v chybove hlascce.
   * (mozna) logovat do glitchtipu.

2. PID existuje (nekdo ho naimportoval)

   * Redirekt na landing page stranku daneho zaznamu. 

3. Chyba resolveru - neocekavana vyjimka v resolveru.

   * Zobrazit jako: "Nastala neocekavana chyba v resolveru 'X'.", kde X je nazev resolveru. 
   * Pridat zopakujte za chvili, pokud problem pretrva, kontaktujte podporu.
   * Pridat odkaz na support a odkazat na nej uzivatele v chybove hlascce.
   * Logovat puvodni vyjimku do glitchtipu.

4. Resolver vratil metadata s problemem (warning nebo error)

   * Zobrazit uzivateli flash, ale pustit ho do editoru

5. Pri vytvareni draftu (pres service) doslo k chybe a draft nebyl vytvoren.

   * Zobrazit jako: "Nastala chyba pri vytvareni zaznamu. Zkuste to prosim znovu, pokud problem pretrva, kontaktujte podporu."
   * Pridat odkaz na support a odkazat na nej uzivatele v chybove hlascce.
   * Logovat puvodni vyjimku do glitchtipu.

6. Pri vytvareni draftu byly zaznamenane chyby (marshmallow), ale draft se vytvoril.

   * Zobrazit uzivateli flash, ale pustit ho do editoru

a. odbocka - Publikovani draftu - zmeny

   * 1. zavolat znovu save, abychom zjistili problemy a vymazaly se nevalidni pole
   * 2. nahodit default values pro required fields
   * pak temprve publikovat

7. Pri publikovani doslo k chybe a zaznam nebyl publikovan.

   * Zobrazit jako: "Nastala neznama chyba pri publikovani zaznamu. Kontaktujte podporu."
   * Pridat odkaz na support a odkazat na nej uzivatele v chybove hlascce.
   * dulezite: Logovat puvodni vyjimku do glitchtipu.

8. Detail zaznamu jeste neexistuje (je v draftu) (spojeno s bodem 7), a jdu z bodu 2.

   * uzivateli zobrazit separatni error stranku, ze zaznam prochazi publikacnim procesem a at to zkusi pristi den.
   * pokud dalsi den tam nic nebude, at kontaktuje podporu.

9. Editacni formular - jede oproti ostremu zaznamu, ne draftu.

   * kdyz uzivatel klikne na save a ma chyby:
      * nic se neulozi
      * react zobrazi chyby a formular zustane na editacni strance

   * pokud chyby nejsou, save znamena "automaticky publish" (protoze jsme na ostrem zaznamu)

10. Secret link - neplatny nebo vyprsely

    * otestovat (invenio zobrazi asi svou stranku, ale chce to testnout) !!!
    * uzivateli se musi zobrazit error stranku s informaci, ze odkaz je neplatny nebo vyprsely a at kontaktuje podporu, pokud jeste potrebuje pristup. Pridat odkaz na support.