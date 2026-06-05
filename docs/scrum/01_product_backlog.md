# Rejestr Produktu (Product Backlog): System Ofertowania B2B

Rejestr zawiera historyjki użytkownika (User Stories) zdefiniowane w procesie rozwoju oprogramowania. Każde zadanie zostało poddane estymacji w **Story Points (SP)** oraz spriorytetyzowane metodą **MoSCoW**.

---

## 🏗️ 1. Epik: Moduł CRM i Fundamenty Bazy Danych

### US1: Zarządzanie bazą firm partnerskich
*   **Opis**: Jako *Handlowiec*, chcę wprowadzać i edytować dane firm partnerskich (kontrahentów) w systemie CRM, aby łatwo przypisywać je do powstających ofert.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 3 SP
*   **Kryteria Akceptacji (Acceptance Criteria)**:
    *   *Given*: Handlowiec jest zalogowany w panelu zarządzania.
    *   *When*: Próbuje dodać nową firmę podając Nazwę, Adres oraz opcjonalny NIP.
    *   *Then*: System waliduje dane i zapisuje nową firmę w bazie danych.

### US2: Baza osób kontaktowych (Klientów)
*   **Opis**: Jako *Handlowiec*, chcę przypisywać konkretnych pracowników (kontakty) do zarejestrowanych firm, aby wiedzieć, z kim prowadzę rozmowy handlowe i do kogo kierować ofertę.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 3 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Istnieje zarejestrowana firma w bazie.
    *   *When*: Handlowiec dodaje osobę kontaktową określając Imię, Nazwisko, Adres E-mail, Telefon i Stanowisko (np. Dyrektor IT).
    *   *Then*: Osoba kontaktowa zostaje poprawnie przypisana do wybranej firmy w bazie danych.

### US3: Zarządzanie danymi własnych spółek (Wystawców)
*   **Opis**: Jako *Manager / Administrator*, chcę zarządzać danymi naszych własnych firm wystawiających oferty, w tym dodawać logotypy i konta bankowe, aby wygenerowane oferty posiadały kompletne dane prawne.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 5 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Istnieją uprawnienia administracyjne.
    *   *When*: Administrator dodaje nową firmę wystawiającą ofertę, wgrywając logotyp (plik graficzny) oraz konto bankowe.
    *   *Then*: System zapisuje logotyp na dysku deweloperskim i wyświetla go w danych wystawcy.

---

## ✍️ 2. Epik: Kreator Ofert i Logika Finansowa

### US4: Tworzenie nagłówka oferty
*   **Opis**: Jako *Handlowiec*, chcę zainicjować nową ofertę, określając Wystawcę, Klienta, opis/zakres prac (SOW), walutę oraz terminy ważności i płatności, aby stworzyć szkielet dokumentu.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 5 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Handlowiec jest zalogowany w systemie.
    *   *When*: Handlowiec tworzy ofertę, uzupełnia pole tekstowe opisujące zakres prac (za pomocą edytora CKEditor) i zapisuje formularz.
    *   *Then*: System automatycznie nadaje ofercie unikalny numer (np. `OF/YYYYMMDD/XXXX`), ustawia status na `Robocza (Draft)` i przypisuje autora.

### US5: Dynamiczne pozycje kosztorysu
*   **Opis**: Jako *Handlowiec*, chcę dodawać wiele pozycji (towary/usługi) do oferty w formie tabeli z określeniem ilości i ceny jednostkowej, aby precyzyjnie wycenić zakres prac.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 8 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Handlowiec edytuje nowo utworzoną ofertę.
    *   *When*: Klika przycisk "+ Dodaj kolejną pozycję" i wprowadza Nazwę usługi, Ilość oraz Cenę jednostkową PLN.
    *   *Then*: JavaScript dynamicznie klonuje wiersz formularza, a Django poprawnie waliduje cały zestaw formularzy (inline formset).

### US6: Automatyczne kalkulacje finansowe (Netto, VAT, Brutto)
*   **Opis**: Jako *Handlowiec*, chcę, aby system automatycznie podsumowywał wartość netto pozycji kosztorysu oraz wyliczał podatek VAT (23%) i sumę brutto, abym nie musiał wykonywać obliczeń ręcznie.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 3 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Istnieje oferta z kilkoma pozycjami kosztorysu.
    *   *When*: Dowolna pozycja zostanie dodana, zmodyfikowana lub usunięta.
    *   *Then*: Sygnał bazodanowy (`post_save`/`post_delete`) automatycznie przelicza sumę netto oferty, a wbudowane właściwości wyliczają dynamicznie VAT i ostateczną kwotę brutto.

---

## 🔄 3. Epik: Workflow, Akceptacje i Dokument PDF

### US7: Zwinny obieg dokumentów i blokada edycji
*   **Opis**: Jako *Handlowiec*, chcę wysłać gotową ofertę do akceptacji menedżerskiej, a jako *CEO* chcę móc ją zatwierdzić, co zablokuje jej dalszą edycję i pozwoli na generowanie dokumentów.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 5 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Oferta ma status `Robocza`.
    *   *When*: Handlowiec klika "Wyślij do akceptacji", a CEO następnie klika "Zatwierdź".
    *   *Then*: Status oferty zmienia się kolejno na `Oczekuje` oraz `Zatwierdzona`. Oferty w tych statusach stają się nieedytowalne dla handlowca (Readonly).

### US8: System odrzucania ofert z feedbackiem
*   **Opis**: Jako *CEO*, chcę mieć możliwość odrzucenia oferty z podaniem pisemnego powodu decyzji, aby Handlowiec wiedział, co należy poprawić.
*   **Priorytet MoSCoW**: SHOULD HAVE
*   **Estymacja**: 3 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Oferta ma status `Oczekuje na akceptację`.
    *   *When*: CEO odrzuca ofertę, co wymaga obowiązkowego wpisania powodu odrzucenia w formularzu.
    *   *Then*: Status oferty zmienia się na `Odrzucona`, a Handlowiec widzi duży czerwony komunikat z pisemnym powodem odrzucenia, po czym może przywrócić ofertę do edycji.

### US9: Moduł konsultacji technicznych
*   **Opis**: Jako *Handlowiec*, chcę mieć możliwość skierowania oferty do statusu "Konsultacja" z Senior Developerem IT, aby zweryfikować wykonalność techniczną przed wysłaniem dokumentu do CEO.
*   **Priorytet MoSCoW**: COULD HAVE
*   **Estymacja**: 2 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Oferta jest w trybie edycji.
    *   *When*: Handlowiec klika "Skieruj do konsultacji IT".
    *   *Then*: Status zmienia się na `Konsultacja`, co sygnalizuje działowi technicznemu konieczność weryfikacji.

### US10: Generator PDF z logotypem firmy
*   **Opis**: Jako *Handlowiec*, chcę generować ujednolicony i profesjonalny plik PDF oferty handlowej jednym kliknięciem, aby móc wysłać go bezpośrednio do klienta.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 8 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Oferta została zatwierdzona przez CEO.
    *   *When*: Użytkownik klika przycisk "Pobierz PDF".
    *   *Then*: Silnik `WeasyPrint` renderuje widok HTML do pliku PDF, pobierając logotyp spółki, dane nabywcy oraz dynamiczne kwoty finansowe.

### US11: Polerowanie UX i poprawki błędów wyglądu (Sprint 3 Refinement)
*   **Opis**: Jako *Użytkownik*, chcę, aby interfejs aplikacji ładował się szybko i poprawnie (bez brakujących plików CSS), a kwoty finansowe netto i brutto były precyzyjnie opisane i czytelne.
*   **Priorytet MoSCoW**: MUST HAVE
*   **Estymacja**: 3 SP
*   **Kryteria Akceptacji**:
    *   *Given*: Użytkownik przegląda szczegóły oferty.
    *   *When*: Arkusze stylów CSS są ładowane z poprawnych ścieżek statycznych aplikacji.
    *   *Then*: Karta podsumowania poprawnie rozbija sumę na Netto, VAT i Brutto, a badże statusów otrzymują ujednolicone kolory ze stylów CSS.
