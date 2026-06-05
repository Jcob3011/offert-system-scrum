# Karta Projektu i Założenia Początkowe: System Ofertowania B2B

## 📊 Metryka Projektu
*   **Nazwa Projektu**: System Ofertowania B2B (Django CRM)
*   **Okres Realizacji**: 25 kwietnia 2026 r. – 6 czerwca 2026 r. (6 tygodni, 3 sprinty po 2 tygodnie)
*   **Metodyka**: SCRUM (w formule Solo Scrum)
*   **Technologia**: Python 3.11, Django 5.x, SQLite, WeasyPrint, Bootstrap 5

---

## 🎯 1. Cel i Założenia Biznesowe
Głównym celem projektu jest automatyzacja procesu przygotowywania, weryfikacji oraz zatwierdzania ofert handlowych w sektorze B2B. 

### Dotychczasowy problem (As-Is):
*   Ręczne i czasochłonne tworzenie ofert w arkuszach kalkulacyjnych (Excel).
*   Trudności z wersjonowaniem plików i brak historii wysyłanych ofert.
*   Brak spójnego procesu autoryzacji ofert (mailowy/telefoniczny obieg dokumentów między Handlowcem a CEO).
*   Brak standaryzacji wyliczeń finansowych (częste błędy w stawkach VAT i kwotach brutto).
*   Niespójny wizerunek graficzny dokumentów wysyłanych do klientów.

### Stan docelowy (To-Be):
*   Wdrożenie centralnego systemu CRM online, w którym handlowcy mogą błyskawicznie składać oferty.
*   Zbudowanie sztywnej, zautomatyzowanej logiki finansowej (automatyczne przeliczanie Netto -> VAT -> Brutto).
*   Zaimplementowanie dwustopniowej weryfikacji ofert: handlowiec tworzy ofertę, a CEO zatwierdza lub odrzuca ją (wraz z podaniem powodu).
*   Wprowadzenie statusu "Konsultacja" z działem technicznym w przypadku niestandardowych wycen.
*   Generowanie profesjonalnego i ujednoliconego dokumentu PDF z logotypem firmy jednym kliknięciem za pomocą silnika PDF.

---

## 👥 2. Struktura Zespołu SCRUM (Solo Scrum)
Z uwagi na realizację akademicką w pojedynkę, role w metodyce SCRUM zostały podzielone w formule **Solo Scrum** (gdzie jedna osoba łączy perspektywy biznesową i techniczną):
*   **Product Owner (Jakub)**: Odpowiedzialny za specyfikację wymagań biznesowych, priorytetyzację rejestru produktu (Product Backlog), akceptację historyjek użytkownika w review oraz reprezentowanie potrzeb klienta biznesowego.
*   **Scrum Master (Jakub)**: Odpowiedzialny za pilnowanie procesów zwinnych, organizację spotkań (Planowanie, Retrospektywa), rozwiązywanie przeszkód technologicznych (impediments) i monitorowanie metryk projektu (Burndown Charts).
*   **Developer (Jakub)**: Odpowiedzialny za implementację kodu backendowego (Python/Django), bazodanowego (SQL) oraz frontendowego (HTML/CSS/JS), a także testy jednostkowe i integracyjne.

---

## 📝 3. Wymagania i Zakres Projektu

### Wymagania Funkcjonalne (Functional Requirements):
1.  **Zarządzanie Baza Klientów i Firm (CRM)**:
    *   Baza firm zewnętrznych (NIP, Adres, Nazwa).
    *   Baza osób kontaktowych przypisanych do firm (Imię, Nazwisko, Email, Telefon).
    *   Słownik własnych spółek wystawiających oferty (Nazwa, Dane adresowe, Bank, Logo).
2.  **Kreator Ofert**:
    *   Tworzenie nowej oferty z wyborem klienta, wystawcy i określeniem warunków płatności (metoda, ważność oferty).
    *   Dynamiczne dodawanie wielu pozycji kosztorysu (Nazwa produktu/usługi, Ilość, Cena jednostkowa, opcjonalna cena EUR).
    *   Automatyczne wyliczanie sumy Netto, VAT (23%) oraz ostatecznej kwoty Brutto.
3.  **Obieg Dokumentu (State Machine)**:
    *   Przejścia między statusami: `Robocza (Draft)` -> `Oczekuje (Pending)` -> `Zatwierdzona (Approved)` / `Odrzucona (Rejected)` / `Konsultacja (Consultation)`.
    *   Blokada edycji ofert, które zostały już zatwierdzone lub czekają na akceptację (ACL).
    *   Mechanizm odrzucenia przez CEO z wymogiem wpisania powodu (feedback loop).
4.  **Generator PDF**:
    *   Renderowanie dokumentu PDF na podstawie szablonu HTML za pomocą biblioteki `WeasyPrint`.
    *   Automatyczne dołączanie logotypu wystawcy, pełnych danych nabywcy oraz dynamicznych wyliczeń netto/brutto.

### Wymagania Niefunkcjonalne (Non-functional Requirements):
1.  **Wydajność**: Generowanie PDF i przeliczanie kwot na serwerze poniżej 2 sekund.
2.  **Responsywność (RWD)**: Interfejs przystosowany do przeglądarek mobilnych (Bootstrap 5).
3.  **Bezpieczeństwo**: Wymóg uwierzytelnienia (login/hasło) dla wszystkich widoków aplikacji (brak dostępu anonimowego).

---

## 🏁 4. Definition of Done (DoD)
Dla każdego zadania w sprincie uznaje się je za ukończone (Done), gdy spełnione są następujące kryteria:
1.  Kod jest napisany i zgodny ze standardami PEP8 (dla Pythona) oraz waliduje się poprawnie (brak błędów HTML/CSS).
2.  Logika biznesowa przechodzi pomyślnie testy manualne.
3.  Zmiany są zatwierdzone i zacommitowane do lokalnego repozytorium Git z jasną wiadomością zgodną z konwencją *Conventional Commits*.
4.  Wymagania i Kryteria Akceptacji (Acceptance Criteria) zdefiniowane w historyjce użytkownika są w 100% zrealizowane.
