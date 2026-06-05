# Raport ze Sprintu 3: Workflow, PDF i Szlify Wyglądu (UX)

## 📅 Ramy Czasowe i Cel
*   **Czas trwania**: 23 maja 2026 r. – 5 czerwca 2026 r. (2 tygodnie)
*   **Cel Sprintu (Sprint Goal)**: Implementacja obiegu dokumentu (Zatwierdzanie/Odrzucanie przez CEO, Konsultacja IT), generatora ofert PDF z logotypem firmy oraz ostateczne poprawienie wyglądu (UX), ścieżek CSS i logiki finansowej.

---

## 🏃‍♂️ 1. Rejestr Zadań Sprintu (Sprint Backlog)
Do realizacji w tym sprincie wybrano następujące historyjki z Rejestru Produktu:
1.  **US7**: Zwinny obieg dokumentów i blokada edycji (5 SP) – *Status: UKOŃCZONE*
2.  **US8**: System odrzucania ofert z feedbackiem (3 SP) – *Status: UKOŃCZONE*
3.  **US9**: Moduł konsultacji technicznych (2 SP) – *Status: UKOŃCZONE*
4.  **US10**: Generator PDF z logotypem firmy (8 SP) – *Status: UKOŃCZONE*
5.  **US11**: Polerowanie UX i poprawki błędów wyglądu (3 SP) – *Status: UKOŃCZONE*

*   **Suma zadeklarowanych Story Points**: 21 SP
*   **Dostarczonych Story Points**: 21 SP (100% realizacji)

---

## 📉 2. Wykres Spalania (Burndown Chart Data)
Poniższa tabela przedstawia stan pozostałych Story Points dzień po dniu podczas trwania Sprintu 3.

| Dzień Sprintu | Data (2026) | Pozostało Pracy (Idealnie) | Pozostało Pracy (Faktycznie) | Opis / Zdarzenie |
| :---: | :---: | :---: | :---: | :--- |
| Dzień 0 | 23.05 (Sob) | 21.0 SP | 21.0 SP | Planowanie Sprintu 3, start prac |
| Dzień 1 | 24.05 (Nie) | 19.4 SP | 21.0 SP | Weekend |
| Dzień 2 | 25.05 (Pon) | 17.8 SP | 21.0 SP | Implementacja maszyny stanów w widokach i adminie |
| Dzień 3 | 26.05 (Wt) | 16.2 SP | 16.0 SP | **Ukończenie US7** (Obieg i blokada edycji ACL) |
| Dzień 4 | 27.05 (Śr) | 14.6 SP | 11.0 SP | **Ukończenie US8 i US9** (Odrzucenia CEO i Konsultacje) |
| Dzień 5 | 28.05 (Czw) | 13.0 SP | 11.0 SP | Konfiguracja silnika PDF `WeasyPrint` |
| Dzień 6 | 29.05 (Pią) | 11.4 SP | 11.0 SP | Prace nad szablonem PDF i integracją CSS |
| Dzień 7 | 30.05 (Sob) | 9.8 SP | 11.0 SP | Weekend |
| Dzień 8 | 31.05 (Nie) | 8.2 SP | 11.0 SP | Weekend |
| Dzień 9 | 01.06 (Pon) | 6.6 SP | 3.0 SP | **Ukończenie US10** (Generowanie PDF z bazy) |
| Dzień 10 | 02.06 (Wt) | 5.0 SP | 3.0 SP | Identyfikacja i analiza błędów w szablonach (szlify UX) |
| Dzień 11 | 03.06 (Śr) | 3.4 SP | 0.0 SP | **Ukończenie US11** (Szlify wyglądu, naprawa CSS 404, sumy brutto) |
| Dzień 12 | 04.06 (Czw) | 1.8 SP | 0.0 SP | Testy integracyjne systemu i weryfikacja poprawności |
| Dzień 13 | 05.06 (Pią) | 0.0 SP | 0.0 SP | Przegląd i Retrospektywa Końcowa |

---

## 🔍 3. Przegląd Sprintu (Sprint Review)
Podczas prezentacji pomyślnie zademonstrowano:
*   Kompletny cykl życia oferty handlowej: Handlowiec wysyła ofertę, CEO otrzymuje powiadomienie, może ją zatwierdzić lub odrzucić. Przy odrzuceniu CEO wpisuje powód, który Handlowiec widzi na pulpicie i może na jego podstawie poprawić ofertę.
*   Moduł "Konsultacja z Seniorem IT" pozwalający skierować ofertę do działu technicznego.
*   Zabezpieczenia edycji (Readonly) uniemożliwiające modyfikację wysłanej oferty.
*   Funkcję generowania profesjonalnego PDF za pomocą silnika `WeasyPrint`, który dynamicznie wylicza sumę Netto, VAT (23%) oraz Brutto, a także ładuje logotyp spółki.
*   Polerowanie interfejsu (UX): poprawiono ścieżki do plików CSS (brak błędów 404 w konsoli), naprawiono błędy składniowe HTML w kreatorze i PDF oraz poprawiono wyświetlanie klienta (pokazuje imię, nazwisko i firmę, a nie NIP) i logikę prezentacji finansowej.

---

## 🔄 4. Retrospektywa Sprintu 3 (Sprint Retrospective)

### Co poszło dobrze (Keep doing / Start):
*   Silnik `WeasyPrint` pozwolił na zachowanie 100% spójności graficznej dokumentu drukowanego z szablonami HTML i CSS.
*   Uproszczono kod szablonów poprzez zaimplementowanie właściwości `css_class` w modelu `Offer` – zamiast wielokrotnych warunków `{% if %}` w HTML, klasy kolorów badży są teraz pobierane bezpośrednio z kodu backendu.

### Co poszło źle (Stop):
*   W połowie sprintu zidentyfikowano serię błędów w szablonach: pusta kolumna "Klient" na liście, brakujące style CSS (błędy 404) oraz poważną pomyłkę w oznaczeniach finansowych (suma netto była podpisana jako brutto). Gdyby nie rygorystyczne testy manualne pod koniec prac, błędy te trafiłyby do użytkowników końcowych.

### Akcje naprawcze (Action Items / Continue):
*   Wdrożono procedurę natychmiastowego usuwania błędów (Hotfix), poprawiono ścieżki ładowania zasobów statycznych, zaktualizowano szablony szczegółów i listy oraz zintegrowano dynamiczne wyliczenia finansowe oparte o metody modelu `get_total_vat` i `get_total_gross`. Na przyszłość należy planować testy cząstkowe wcześniej w trakcie sprintu.
