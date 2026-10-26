# Nasazeni NMA

## Pred shozenim predchoziho

Pustit lokalne:

```

invenio rdm-records add-to-fixture affiliations
(a pockat az workery naindexuji)

export BEARER=...

python scripts/download_nma_data.py non_harvested_nma_records.jsonl

python scripts/fix_downloaded_record.py non_harvested_nma_records.jsonl fixed_nma_records.jsonl

python scripts/validate_records.py fixed_nma_records.jsonl
```

Na serveru pak:

zkopirovat vocabularies.yaml a vocabularies adresar do app-data
dat invenio rdm-records add-to-fixture affiliations

zkopirovat fixed_nma_records.jsonl do app_data/datasets.jsonl

invenio rdmr-records add-to-fixture datasets
