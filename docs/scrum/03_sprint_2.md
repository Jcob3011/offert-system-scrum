# Raport ze Sprintu 2: Logika Biznesowa i Kreator Ofert

## 📅 Ramy Czasowe i Cel
*   **Czas trwania**: 9 maja 2026 r. – 22 maja 2026 r. (2 tygodnie)
*   **Cel Sprintu (Sprint Goal)**: Implementacja modułu tworzenia i edycji nagłówka ofert, dynamicznej tabeli kosztorysu pozycji oferty oraz automatycznego przeliczania wartości finansowych.

---

## 🏃‍♂️ 1. Rejestr Zadań Sprintu (Sprint Backlog)
Do realizacji w tym sprincie wybrano następujące historyjki z Rejestru Produktu:
1.  **US4**: Tworzenie nagłówka oferty (5 SP) – *Status: UKOŃCZONE*
2.  **US5**: Dynamiczne pozycje kosztorysu (8 SP) – *Status: UKOŃCZONE*
3.  **US6**: Automatyczne kalkulacje finansowe (Netto, VAT, Brutto) (3 SP) – *Status: UKOŃCZONE*

*   **Suma zadeklarowanych Story Points**: 16 SP
*   **Dostarczonych Story Points**: 16 SP (100% realizacji)

---

## 📉 2. Wykres Spalania (Burndown Chart Data)
Poniższa tabela przedstawia stan pozostałych Story Points dzień po dniu podczas trwania Sprintu 2.

| Dzień Sprintu | Data (2026) | Pozostało Pracy (Idealnie) | Pozostało Pracy (Faktycznie) | Opis / Zdarzenie |
| :---: | :---: | :---: | :---: | :--- |
| Dzień 0 | 09.05 (Sob) | 16.0 SP | 16.0 SP | Planowanie Sprintu 2, start prac |
| Dzień 1 | 10.05 (Nie) | 14.8 SP | 16.0 SP | Weekend |
| Dzień 2 | 11.05 (Pon) | 13.6 SP | 16.0 SP | Implementacja modelu `Offer` i pól nagłówkowych |
| Dzień 3 | 12.05 (Wt) | 12.4 SP | 11.0 SP | **Ukończenie US4** (Nagłówek oferty z auto-numerem) |
| Dzień 4 | 13.05 (Śr) | 11.2 SP | 11.0 SP | Rozpoczęcie prac nad `OfferItem` i Django forms |
| Dzień 5 | 14.05 (Czw) | 10.0 SP | 11.0 SP | Prace nad `inlineformset_factory` dla pozycji |
| Dzień 6 | 15.05 (Pią) | 8.8 SP | 11.0 SP | Tworzenie skryptu JS do dynamicznego klonowania wierszy |
| Dzień 7 | 16.05 (Sob) | 7.6 SP | 11.0 SP | Weekend |
| Dzień 8 | 17.05 (Nie) | 6.4 SP | 11.0 SP | Weekend |
| Dzień 9 | 18.05 (Pon) | 5.2 SP | 11.0 SP | Rozwiązywanie problemów z walidacją `TOTAL_FORMS` |
| Dzień 10 | 19.05 (Wt) | 4.0 SP | 3.0 SP | **Ukończenie US5** (Dynamiczna tabela pozycji) |
| Dzień 11 | 20.05 (Śr) | 2.8 SP | 3.0 SP | Praca nad sygnałami bazodanowymi w Django |
| Dzień 12 | 21.05 (Czw) | 1.6 SP | 0.0 SP | **Ukończenie US6** (Sygnały i automatyczne sumy Netto) |
| Dzień 13 | 22.05 (Pią) | 0.0 SP | 0.0 SP | Przegląd i Retrospektywa Sprintu 2 |

---

## 🔍 3. Przegląd Sprintu (Sprint Review)
Podczas prezentacji pomyślnie zademonstrowano:
*   Formularz tworzenia nowej oferty. System automatycznie generuje unikalny numer oferty w formacie `OF/YYYYMMDD/XXXX` na podstawie daty i losowego identyfikatora.
*   Dynamiczną tabelę na pozycje oferty. Handlowiec może w czasie rzeczywistym dodawać nowe wiersze za pomocą przycisku oraz usuwać je zaznaczając odpowiedni checkbox.
*   Automatyczną logikę sumującą: zapisanie pozycji kosztorysu w bazie danych wyzwala sygnał Django (`recalculate_offer_total`), który natychmiastowo aktualizuje sumaryczną wartość netto całej oferty w tabeli bazodanowej.

---

## 🔄 4. Retrospektywa Sprintu 2 (Sprint Retrospective)

### Co poszło dobrze (Keep doing / Start):
*   Dynamiczny interfejs oparty o vanilla JavaScript działa szybko i sprawnie, nie obciążając serwera.
*   Sygnały Django (`@receiver(post_save)`) okazały się bardzo stabilnym rozwiązaniem do automatycznych obliczeń bazodanowych, odciążając warstwę widoków (`views.py`).

### Co poszło źle (Stop):
*   Pojawił się krytyczny problem z dodawaniem wierszy w JavaScript z powodu niepoprawnego prefixu pól (`offeritem_set` vs `items`). Powodowało to błędy walidacji Django i uniemożliwiało zapisanie formularza.

### Akcje naprawcze (Action Items / Continue):
*   Wprowadzono mechanizm awaryjny (fallback) w kodzie JavaScript, który automatycznie wykrywa właściwy prefix wejściowy formularza (`TOTAL_FORMS`), co zapobiega crashom i poprawia elastyczność systemu.
