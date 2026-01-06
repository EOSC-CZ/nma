#!/usr/bin/env bash

set -euo pipefail

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_step() {
    echo
    echo -e "${GREEN}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    echo
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    echo
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    echo
}

cd "$(dirname "$0")/.."

print_header "Local Installation Reset Script"

print_header "Manual Step Required"
echo -e "${YELLOW}Please make sure that server is not running and then press Enter to continue...${NC}"
read -r
print_success "Continuing with setup"

# Step 1: Reset invenio private config
print_step "Resetting InvenioRDM configuration..."
if [ -f .invenio.private ] ; then
    # replace services_setup = True with services_setup = False
    sed 's/services_setup = True/services_setup = False/' .invenio.private > .invenio.private.tmp
    mv .invenio.private.tmp .invenio.private
    print_success "Configuration reset complete"
else
    print_warning "No .invenio.private file found, skipping"
fi

# Step 2: Remove docker containers
print_step "Removing Docker containers..."
if [ -f docker/.env ] ; then
    (
        cd docker
        docker compose down
        docker compose rm
    )
    print_success "Docker containers removed"
else
    print_warning "No docker/.env file found, skipping container removal"
fi

# Step 3: Setup services
print_step "Setting up services..."
./run.sh services setup -N
print_success "Services setup complete"

# Step 4: Wait for user to start application
print_header "Manual Step Required"
echo -e "${YELLOW}Please run the following command in another terminal:${NC}"
echo -e "${CYAN}    ./run.sh run${NC}"
echo -e "${YELLOW}Wait for the output to settle, then press Enter to continue...${NC}"
read -r
print_success "Continuing with setup"

source .venv/bin/activate

# Step 5: Create roles
print_step "Creating users and roles..."
# 123456 to keep invenio-cli compatibility if not entered
invenio users create -a -c user@demo.org --password ${DEMO_USER_PASSWORD:-123456}
invenio roles create riv_curators
invenio roles create administration-moderation
invenio access allow administration-access user user@demo.org
invenio access allow administration-moderation user user@demo.org
invenio roles add user@demo.org riv_curators
print_success "Role 'riv_curators' created and user@demo.org assigned"

# Step 6: Create harvesters
print_step "Creating OAI harvesters..."
$(dirname "$0")/create_oai_harvesters.sh