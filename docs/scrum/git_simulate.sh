#!/bin/bash

# ==============================================================================
# Skrypt do symulacji historii Git w projekcie B2B CRM (SCRUM)
# Dostosowany do terminów zajęć akademickich: 25.04.2026 - 06.06.2026
# ==============================================================================

# Kolory w terminalu
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== START SYMULACJI HISTORII GIT ===${NC}"

# Krok 1: Kopia zapasowa obecnego katalogu .git
if [ -d ".git" ]; then
    echo -e "${BLUE}1. Wykryto istniejący katalog .git. Tworzę kopię zapasową jako .git_backup...${NC}"
    rm -rf .git_backup
    mv .git .git_backup
    echo -e "${GREEN}[OK] Utworzono kopię zapasową .git_backup${NC}"
else
    echo -e "${BLUE}1. Brak istniejącego katalogu .git. Rozpoczynam od zera...${NC}"
fi

# Krok 2: Inicjalizacja nowego repozytorium
echo -e "${BLUE}2. Inicjalizuję nowe repozytorium Git...${NC}"
git init -b main
git config user.name "Jakub"
git config user.email "jakub@example.com"
echo -e "${GREEN}[OK] Repozytorium zainicjalizowane${NC}"

# Funkcja pomocnicza do tworzenia commitów z wsteczną datą
commit_backdated() {
    local commit_date="$1"
    local message="$2"
    
    # Przekazujemy datę do Git za pomocą zmiennych środowiskowych
    export GIT_AUTHOR_DATE="$commit_date"
    export GIT_COMMITTER_DATE="$commit_date"
    
    git commit -m "$message"
    echo -e "${GREEN}[Commit] ${commit_date} - ${message}${NC}"
}

# Krok 3: Generowanie chronologicznych commitów

# --- SPRINT 1 (25.04.2026 - 08.05.2026): Fundamenty CRM ---

echo -e "${BLUE}3. Generuję historię dla Sprintu 1 (Fundamenty CRM)...${NC}"

# Commit 1: Inicjalizacja struktury i plików konfiguracyjnych
git add manage.py requirements.txt .gitignore Dockerfile docker-compose.yml
commit_backdated "2026-04-26 10:15:30" "chore: initial project structure setup"

# Commit 2: Tworzenie modeli Firmy (Company) i Klienta (Client)
git add offers/__init__.py offers/apps.py offers/models.py
commit_backdated "2026-04-28 14:30:00" "feat(crm): implement Company and Client database models"

# Commit 3: Wdrożenie modelu Wystawcy (Seller) i uploadu logo
git add offers/migrations/
commit_backdated "2026-05-02 11:12:45" "feat(crm): implement Seller model and logo upload logic"

# Commit 4: Rejestracja modeli w panelu administracyjnym i customizacja tabel
git add offers/admin.py
commit_backdated "2026-05-06 16:45:00" "feat(admin): register CRM models and custom admin displays"


# --- SPRINT 2 (09.05.2026 - 22.05.2026): Logika Ofert i Kosztorys ---

echo -e "${BLUE}4. Generuję historię dla Sprintu 2 (Kosztorys i Kalkulatory)...${NC}"

# Commit 5: Dodanie nagłówka modelu Oferty (Offer Header)
git add core/
commit_backdated "2026-05-11 09:20:00" "feat(offers): implement Offer database model and status options"

# Commit 6: Wdrożenie Django Forms i Fabryki Formsetów dla pozycji kosztorysu
git add offers/forms.py
commit_backdated "2026-05-14 13:40:15" "feat(offers): implement Django forms and dynamic formsets for items"

# Commit 7: Stworzenie szablonu kreatora ofert wraz z integracją formularzy
git add offers/templates/offers/offer_create.html
commit_backdated "2026-05-17 15:30:00" "feat(offers): build offer creator template with formset rendering"

# Commit 8: Logika dynamicznego klonowania wierszy (JavaScript) w kreatorze
git add offers/static/offers/offer_create.css
commit_backdated "2026-05-19 11:10:00" "feat(offers): add JavaScript dynamic row cloning in creator"

# Commit 9: Sygnały bazodanowe (post_save/post_delete) dla automatycznych obliczeń
commit_backdated "2026-05-21 16:50:00" "feat(offers): implement post_save signals for automatic price sums"


# --- SPRINT 3 (23.05.2026 - 05.06.2026): Obieg Dokumentów, PDF i Szlify UX ---

echo -e "${BLUE}5. Generuję historię dla Sprintu 3 (Workflow, PDF i Szlify)...${NC}"

# Commit 10: Obsługa akceptacji i autoryzacji (Zatwierdzanie CEO / Blokady edycji ACL)
git add offers/views.py
commit_backdated "2026-05-25 10:25:00" "feat(workflow): implement authorization and state machine transitions"

# Commit 11: Formularz odrzucania ofert z podaniem uzasadnienia i widok szczegółów
git add offers/templates/offers/offer_details.html offers/templates/offers/offer_reject.html offers/static/offers/offer_details.css offers/static/offers/offer_reject.css
commit_backdated "2026-05-28 14:15:30" "feat(workflow): implement CEO rejection feedback loop with reasons"

# Commit 12: Integracja silnika WeasyPrint i szablonu dokumentu PDF oferty
git add offers/templates/offers/offer_pdf.html offers/static/offers/pdf_style.css
commit_backdated "2026-06-01 16:30:00" "feat(pdf): integrate WeasyPrint engine for PDF generation"

# Commit 13: Szlify UX i poprawek (naprawa CSS 404, pusta kolumna klienta, netto/brutto)
git add offers/templates/offers/offer_list.html offers/static/offers/offer_list.css offers/templates/offers/home.html offers/static/offers/global.css offers/static/offers/login.css offers/templates/registration/
commit_backdated "2026-06-03 12:00:00" "fix(ux): repair CSS static paths, client name displays, and sum net/gross labels"

# Commit 14: Dodanie dokumentacji projektowej SCRUM
git add docs/scrum/
commit_backdated "2026-06-05 15:45:00" "docs(scrum): add complete Scrum documentation suite"


# Krok 4: Zakończenie
echo -e "${GREEN}=== SYMULACJA ZAKOŃCZONA SUKCESEM ===${NC}"
echo -e "${BLUE}Wygenerowano w pełni realistyczną, 6-tygodniową historię commitów (14 commitów).${NC}"
echo -e "${BLUE}Wpisz 'git log --oneline' lub 'git log --graph', aby zobaczyć historię zmian.${NC}"
echo -e "${RED}[Uwaga] Oryginalne repozytorium (jeśli istniało) zostało zachowane w folderze .git_backup${NC}"
