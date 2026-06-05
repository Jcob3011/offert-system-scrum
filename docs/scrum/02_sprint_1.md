# Raport ze Sprintu 1: Fundamenty CRM i Baza Danych

## 📅 Ramy Czasowe i Cel
*   **Czas trwania**: 25 kwietnia 2026 r. – 8 maja 2026 r. (2 tygodnie)
*   **Cel Sprintu (Sprint Goal)**: Zaprojektowanie i wdrożenie bazy danych CRM (podsystemu firm, klientów i wystawców) oraz konfiguracja panelu administracyjnego do zarządzania słownikami.

---

## 🏃‍♂️ 1. Rejestr Zadań Sprintu (Sprint Backlog)
Do realizacji w tym sprincie wybrano następujące historyjki z Rejestru Produktu:
1.  **US1**: Zarządzanie bazą firm partnerskich (3 SP) – *Status: UKOŃCZONE*
2.  **US2**: Baza osób kontaktowych (Klientów) (3 SP) – *Status: UKOŃCZONE*
3.  **US3**: Zarządzanie danymi własnych spółek (Wystawców) (5 SP) – *Status: UKOŃCZONE*

*   **Suma zadeklarowanych Story Points**: 11 SP
*   **Dostarczonych Story Points**: 11 SP (100% realizacji)

---

## 📉 2. Wykres Spalania (Burndown Chart Data)
Poniższa tabela przedstawia stan pozostałych Story Points dzień po dniu podczas trwania Sprintu 1. Możesz użyć tych danych do narysowania wykresu w Excelu.

| Dzień Sprintu | Data (2026) | Pozostało Pracy (Idealnie) | Pozostało Pracy (Faktycznie) | Opis / Zdarzenie |
| :---: | :---: | :---: | :---: | :--- |
| Dzień 0 | 25.04 (Sob) | 11.0 SP | 11.0 SP | Planowanie Sprintu 1, start prac |
| Dzień 1 | 26.04 (Nie) | 10.0 SP | 11.0 SP | Niedziela - brak aktywności |
| Dzień 2 | 27.04 (Pon) | 9.0 SP | 11.0 SP | Prace nad modelami `Company` i `Client` |
| Dzień 3 | 28.04 (Wt) | 8.0 SP | 8.0 SP | **Ukończenie US1** (Zarządzanie firmami) |
| Dzień 4 | 29.04 (Śr) | 7.0 SP | 8.0 SP | Tworzenie kluczy obcych i relacji w bazie |
| Dzień 5 | 30.04 (Czw) | 6.0 SP | 5.0 SP | **Ukończenie US2** (Osoby kontaktowe) |
| Dzień 6 | 01.05 (Pią) | 5.0 SP | 5.0 SP | Święto Pracy - brak aktywności |
| Dzień 7 | 02.05 (Sob) | 4.0 SP | 5.0 SP | Weekend |
| Dzień 8 | 03.05 (Nie) | 3.0 SP | 5.0 SP | Weekend |
| Dzień 9 | 04.05 (Pon) | 2.0 SP | 5.0 SP | Prace nad modelem `Seller` (wystawcy) |
| Dzień 10 | 05.05 (Wt) | 1.0 SP | 5.0 SP | Integracja przesyłania plików logotypów |
| Dzień 11 | 06.05 (Śr) | 0.0 SP | 0.0 SP | **Ukończenie US3** (Wystawcy, logo) |
| Dzień 12 | 07.05 (Czw) | 0.0 SP | 0.0 SP | Konfiguracja widoków panelu Django Admin |
| Dzień 13 | 08.05 (Pią) | 0.0 SP | 0.0 SP | Przegląd i Retrospektywa Sprintu 1 |

---

## 🔍 3. Przegląd Sprintu (Sprint Review)
Podczas prezentacji pomyślnie zademonstrowano:
*   Zaimplementowaną bazę danych w silniku SQLite.
*   Zarejestrowane struktury modeli w Django Admin.
*   Formularze umożliwiające dodawanie nowej Firmy, przypisywanie do niej Klienta z adresem e-mail oraz konfigurowanie własnych spółek handlowych wraz z ich kontami bankowymi.
*   System wgrywania logotypów (obsługiwany przez bibliotekę `Pillow`).

---

## 🔄 4. Retrospektywa Sprintu 1 (Sprint Retrospective)

### Co poszło dobrze (Keep doing / Start):
*   Django okazał się świetnym wyborem pod szybkie prototypowanie modeli. System automatycznych migracji (`makemigrations`/`migrate`) znacznie przyspieszył prace bazodanowe.
*   Wbudowany Django Admin idealnie sprawdził się jako natychmiastowy interfejs do wprowadzania danych testowych.

### Co poszło źle (Stop):
*   Na początku sprintu wystąpił problem z instalacją biblioteki `Pillow` do obsługi grafiki logo. Spowodowało to jednodniowe opóźnienie w US3.

### Akcje naprawcze (Action Items / Continue):
*   Zdecydowano o natychmiastowym dodawaniu nowo zainstalowanych pakietów do pliku `requirements.txt` w celu uniknięcia problemów ze środowiskiem u innych deweloperów lub na produkcji.
