#!/usr/bin/env bash


# harvesters
invenio oai harvesters create --id catchall --name "Catch-all repository harvester" \
    --base-url "https://data.narodni-repozitar.cz" --metadata-prefix "catchall" --model datasets \
    --loader catch-all --transformer "catch-all"

invenio oai harvesters create --id zenodo-czu --name "Zenodo CZU harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "czu" --model datasets \
    --loader zenodo --transformer "zenodo"             \
    --setspec 'creators.affiliation:("Česká zemědělská univerzita v Praze" OR "ČZU" OR "CESKA ZEMEDELSKA UNIVERZITA V PRAZE" OR "CZU Praha" OR "The Czech University of Life Sciences Prague" OR "Czech University of Agriculture Prague")  AND resource_type.type:dataset'

invenio oai harvesters create --id zenodo-cvut --name "Zenodo CVUT harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "cvut" --model datasets \
    --loader zenodo --transformer "zenodo"             \
    --setspec 'creators.affiliation:("České vysoké učení technické v Praze" OR "ČVUT" OR "CESKE VYSOKE UCENI TECHNICKE V PRAZE" OR "CVUT" OR "Czech Technical University In Prague" OR "CTU in Prague" OR "CTU Prague")  AND resource_type.type:dataset'

invenio oai harvesters create --id zenodo-upol --name "Zenodo UPOL harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "upol" --model datasets \
    --loader zenodo --transformer "zenodo"             \
    --setspec 'creators.affiliation:("upol" OR "Univerzita Palackého v Olomouci" OR "Palacký University Olomouc" OR "Palacky University Olomouc") AND resource_type.type:dataset'

invenio oai harvesters create --id zenodo-utb --name "Zenodo UTB harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "utb" --model datasets \
    --loader zenodo --transformer "zenodo"             \
    --setspec 'creators.affiliation:("utb" OR "Univerzita Tomáše Bati ve Zlíně" OR "Tomas Bata University in Zlin") AND resource_type.type:dataset'

invenio oai harvesters create --id zenodo-vscht --name "Zenodo VSCHT harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "vscht" --model datasets \
    --loader zenodo --transformer "zenodo"             \
    --setspec 'creators.affiliation:("vscht" OR "Vysoká škola chemicko-technologická v Praze" OR "UCT Prague" OR "University of Chemistry and Technology, Prague") AND resource_type.type:dataset'


invenio oai harvesters create --id lindat --name "LINDAT/CLARIN repository harvester" \
    --base-url "https://lindat.mff.cuni.cz/repository/server/oai/request" \
    --metadata-prefix "cmdi" --model datasets \
    --loader oai-pmh --transformer "lindat"

invenio oai harvesters create --id av --name "Academy of sciences repository harvester " \
    --base-url "https://asep.lib.cas.cz/arl-cav/cs/oai/" \
    --metadata-prefix "dataciteoai" --setspec "OAIDATACITE" --model datasets \
    --loader oai-pmh --transformer 'oai-import{"model":"datasets"}'