cd $(dirname $0)

# datarepo
./harvest_datarepo_eosc_cz.sh

# zenodo communities
./harvest_cvut.sh
./harvest_czu.sh
./harvest_upol.sh
./harvest_utb.sh
./harvest_vscht.sh

# lindat
./harvest_lindat.sh
