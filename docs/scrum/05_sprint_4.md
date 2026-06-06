# Raport ze Sprintu 4: Automatyzacja, Profilowanie i Optymalizacja PDF

## 📅 Ramy Czasowe i Cel
*   **Czas trwania**: 6 czerwca 2026 r. – 19 czerwca 2026 r. (2 tygodnie)
*   **Cel Sprintu (Sprint Goal)**: Wprowadzenie automatycznej sekwencyjnej numeracji ofert, umożliwienie profilowania handlowców (imię, nazwisko, telefon) i ich integracji ze stopką PDF, a także usunięcie błędów ładowania logotypu firmy w PDF oraz ujednolicenie stylistyki podsumowania finansowego.

---

## 🏃‍♂️ 1. Rejestr Zadań Sprintu (Sprint Backlog)
Do realizacji w tym sprincie wybrano następujące historyjki z Rejestru Produktu:
1.  **US12**: Automatyczna sekwencyjna numeracja ofert (5 SP) – *Status: UKOŃCZONE*
2.  **US13**: Profilowanie użytkowników (dane kontaktowe Handlowca) (5 SP) – *Status: UKOŃCZONE*
3.  **US14**: Integracja danych handlowca z PDF (2 SP) – *Status: UKOŃCZONE*
4.  **US15**: Weryfikacja i poprawka ładowania logotypu w silniku PDF (3 SP) – *Status: UKOŃCZONE*

*   **Suma zadeklarowanych Story Points**: 15 SP
*   **Dostarczonych Story Points**: 15 SP (100% realizacji)

---

## 📉 2. Wykres Spalania (Burndown Chart Data)
Poniższa tabela przedstawia stan pozostałych Story Points dzień po dniu podczas trwania Sprintu 4.

| Dzień Sprintu | Data (2026) | Pozostało Pracy (Idealnie) | Pozostało Pracy (Faktycznie) | Opis / Zdarzenie |
| :---: | :---: | :---: | :---: | :--- |
| Dzień 0 | 06.06 (Sob) | 15.0 SP | 15.0 SP | Planowanie Sprintu 4, analiza bazy danych |
| Dzień 1 | 07.06 (Nie) | 13.8 SP | 15.0 SP | Weekend |
| Dzień 2 | 08.06 (Pon) | 12.6 SP | 10.0 SP | **Ukończenie US12** (Nowy mechanizm save() i zliczanie chronologiczne) |
| Dzień 3 | 09.06 (Wt) | 11.4 SP | 10.0 SP | Prace nad rozszerzeniem modelu User (UserProfile) |
| Dzień 4 | 10.06 (Śr) | 10.2 SP | 5.0 SP | **Ukończenie US13** (Migracje, UserProfileInline w UserAdmin) |
| Dzień 5 | 11.06 (Czw) | 9.0 SP | 5.0 SP | Wdrożenie stopki przygotowującego w szablonie PDF |
| Dzień 6 | 12.06 (Pią) | 7.8 SP | 3.0 SP | **Ukończenie US14** (Udostępnienie pełnych danych handlowca w stopce) |
| Dzień 7 | 13.06 (Sob) | 6.6 SP | 3.0 SP | Weekend |
| Dzień 8 | 14.06 (Nie) | 5.4 SP | 3.0 SP | Weekend |
| Dzień 9 | 15.06 (Pon) | 4.2 SP | 0.0 SP | **Ukończenie US15** (Protokół file:// dla logo, usunięcie zielonej sumy brutto) |
| Dzień 10 | 16.06 (Wt) | 3.0 SP | 0.0 SP | Testy integracyjne z silnikiem WeasyPrint w kontenerze |
| Dzień 11 | 17.06 (Śr) | 1.8 SP | 0.0 SP | Przegląd bazy danych i czyszczenie profili (one-time data script) |
| Dzień 12 | 18.06 (Czw) | 0.6 SP | 0.0 SP | Aktualizacja instrukcji README i dokumentacji projektowej |
| Dzień 13 | 19.06 (Pią) | 0.0 SP | 0.0 SP | Przegląd i Retrospektywa Końcowa Sprintu 4 |

---

## 🔍 3. Przegląd Sprintu (Sprint Review)
Podczas prezentacji pomyślnie zademonstrowano:
*   **W pełni automatyczną i sekwencyjną numerację**: Zamiast UUID, nowo tworzone oferty automatycznie otrzymują numer w formacie `(numer_w_miesiącu)/(miesiąc)/(rok)`. Kolejność jest zachowana i resetuje się wraz z nadejściem nowego miesiąca kalendarzowego.
*   **Profilowanie Użytkowników**: Rozszerzono profil użytkownika o pole "telefon", dodając do bazy model `UserProfile` połączony relacją `OneToOneField` do `User`. W panelu administracyjnym zintegrowano ten profil jako sekcję `UserProfileInline` w edycji kont użytkowników.
*   **Integrację Handlowca z PDF**: Stopka PDF w bloku "Ofertę przygotował" dynamicznie pobiera i renderuje Imię, Nazwisko, E-mail oraz numer telefonu z profilu osoby logującej się i tworzącej ofertę.
*   **Poprawne ładowanie logo**: Poprawiono sposób wskazywania ścieżki logotypu firmy w Django i szablonie PDF. Użycie bezwzględnej ścieżki z protokołem `file://` pozwoliło ominąć restrykcje sieciowe silnika `WeasyPrint` i poprawnie wczytywać obrazy z dysku.
*   **Uporządkowanie podsumowania finansowego**: Usunięto jaskrawy zielony kolor z kwoty brutto na wydruku PDF. Kwota brutto jest teraz formatowana w kolorze czarnym, co poprawiło elegancję i czytelność dokumentu.

---

## 🔄 4. Retrospektywa Sprintu 4 (Sprint Retrospective)

### Co poszło dobrze (Keep doing / Start):
*   Architektura "Fat Models, Skinny Views" sprawdziła się znakomicie – umieszczenie logiki wyliczania numeru oferty w metodzie `save()` modelu `Offer` zapobiega powielaniu kodu i działa poprawnie zarówno przy dodawaniu ofert przez panel admina, jak i przez formularze frontendowe.
*   Pomyślnie przeniesiono media na dysk lokalny za pomocą schematu `file://`, co pozwoliło na uniezależnienie generowania PDF od wątków sieciowych serwera (brak ryzyka deadlocka w środowisku lokalnym).

### Co poszło źle (Stop):
*   Podczas pierwszego uruchomienia rozszerzonego panelu administracyjnego wystąpił błąd `AttributeError` z powodu wywołania nieistniejącej metody `unbind()` na obiekcie `AdminSite` (powinno być `unregister()`). Błąd ten zablokował na moment działanie serwera deweloperskiego. W przyszłości należy dokładniej weryfikować poprawność nazw metod API frameworka przed restartem usług.

### Akcje naprawcze (Action Items / Continue):
*   Natychmiast podmieniono wadliwą metodę `unbind()` na standardową `unregister(User)` w pliku `admin.py`.
*   Napisano skrypt jednorazowego użytku (data script) uruchomiony w konsoli Django, który automatycznie utworzył brakujące profile `UserProfile` dla dotychczasowych kont w bazie danych, eliminując ryzyko błędów typu `DoesNotExist` przy wyświetlaniu starych dokumentów.
