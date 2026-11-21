"""
Modele domenowe systemu CRM oraz modułu ofertowania B2B.
"""
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    """Reprezentuje firmę kontrahenta (klienta biznesowego)."""
    name = models.CharField(max_length=200, verbose_name="Nazwa Firmy")
    nip = models.CharField(max_length=20, blank=True, null=True, verbose_name="NIP")
    address = models.TextField(verbose_name="Adres", blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Baza Firm"


class Client(models.Model):
    """Reprezentuje osobę kontaktową przypisaną do firmy kontrahenta."""
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='employees', verbose_name="Firma"
    )
    first_name = models.CharField(max_length=100, verbose_name="Imię")
    last_name = models.CharField(max_length=100, verbose_name="Nazwisko")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    position = models.CharField(max_length=100, blank=True, verbose_name="Stanowisko")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.company.name})"

    class Meta:
        verbose_name = "Klient / Kontakt"
        verbose_name_plural = "Baza Klientów"


class Seller(models.Model):
    """Reprezentuje spółkę wystawiającą ofertę (naszą firmę)."""
    name = models.CharField(max_length=200, verbose_name="Nazwa Naszej Firmy")
    nip = models.CharField(max_length=20, verbose_name="NIP")
    address = models.TextField(verbose_name="Adres")
    email = models.EmailField(verbose_name="Email kontaktowy", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Telefon", blank=True)
    bank_account = models.CharField(max_length=50, verbose_name="Konto Bankowe", blank=True)
    logo = models.ImageField(upload_to='company_logos/', verbose_name="Logo", blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Nasza Firma"
        verbose_name_plural = "Nasze Firmy"


class Offer(models.Model):
    """Główny dokument oferty handlowej wraz z maszyną stanów obiegu akceptacji."""

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Robocza')
        PENDING = 'pending', _('Oczekuje na akceptację')
        IN_CONSULTATION = 'consultation', _('Konsultacja')
        APPROVED = 'approved', _('Zatwierdzona')
        SENT = 'sent', _('Wysłana')
        REJECTED = 'rejected', _('Odrzucona')

    class PaymentMethod(models.TextChoices):
        TRANSFER = 'transfer', _('Przelew tradycyjny')
        SPLIT_PAYMENT = 'split', _('Przelew (Split Payment)')
        CASH = 'cash', _('Gotówka')
        CARD = 'card', _('Karta płatnicza')

    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, verbose_name="Wystawca", null=True)
    offer_number = models.CharField(max_length=50, unique=True, verbose_name="Numer oferty")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Klient", null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name="Status"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Opis zakresu prac (SOW)")

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Suma Netto PLN"
    )
    currency_rate = models.DecimalField(
        max_digits=6, decimal_places=4, default=Decimal('1.0000'), verbose_name="Kurs EUR"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validity_days = models.PositiveIntegerField(default=14, verbose_name="Ważność oferty (dni)")
    payment_deadline_days = models.PositiveIntegerField(default=7, verbose_name="Termin płatności (dni)")
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.TRANSFER,
        verbose_name="Metoda płatności",
    )

    rejection_reason = models.TextField(blank=True, null=True, verbose_name="Powód odrzucenia (CEO)")
    external_file = models.FileField(
        upload_to='offers_archive/', null=True, blank=True, verbose_name="Archiwalny PDF"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utworzył"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Oferta"
        verbose_name_plural = "Baza Ofert"

    def __str__(self) -> str:
        return f"{self.offer_number}"

    @property
    def valid_until_date(self) -> date:
        """Zwraca datę wygaśnięcia oferty."""
        base_date = self.created_at.date() if self.created_at else timezone.now().date()
        return base_date + timedelta(days=self.validity_days)

    def update_total(self) -> None:
        """Przelicza sumę netto oferty na podstawie przypisanych pozycji kosztorysu."""
        offer_items = self.items.all()
        new_total = sum((item.total_price for item in offer_items), Decimal('0.00'))
        self.total_price = new_total
        self.save(update_fields=['total_price'])

    def get_total_vat(self) -> Decimal:
        """Oblicza kwotę podatku VAT (23%)."""
        return (self.total_price * Decimal('0.23')).quantize(Decimal('0.01'))

    def get_total_gross(self) -> Decimal:
        """Oblicza kwotę Brutto (Netto + VAT 23%)."""
        return (self.total_price * Decimal('1.23')).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs) -> None:
        """Generuje sekwencyjny numer oferty X/MM/YYYY przed pierwszym zapisem."""
        if not self.offer_number:
            now = timezone.now()
            current_month = now.month
            current_year = now.year

            count = Offer.objects.filter(
                created_at__month=current_month,
                created_at__year=current_year,
            ).count()

            next_number = count + 1
            while True:
                candidate = f"{next_number}/{current_month:02d}/{current_year}"
                if not Offer.objects.filter(offer_number=candidate).exists():
                    self.offer_number = candidate
                    break
                next_number += 1

            if 'update_fields' in kwargs and kwargs['update_fields'] is not None:
                fields = list(kwargs['update_fields'])
                if 'offer_number' not in fields:
                    fields.append('offer_number')
                kwargs['update_fields'] = fields

        super().save(*args, **kwargs)

    # --- MASZYNA STANÓW (STATE MACHINE) ---

    def submit_for_approval(self) -> tuple[bool, str]:
        """Przesyła ofertę roboczą do akceptacji CEO."""
        if self.status == self.Status.DRAFT:
            self.status = self.Status.PENDING
            self.save(update_fields=['status'])
            return True, f"Oferta {self.offer_number} wysłana do akceptacji."
        return False, "Tylko szkic można wysłać do akceptacji."

    def approve(self, user: User) -> tuple[bool, str]:
        """Zatwierdza ofertę (wymagane uprawnienia superusera/CEO)."""
        if not user.is_superuser:
            return False, "Brak uprawnień (wymagany CEO)."
        if self.status == self.Status.PENDING:
            self.status = self.Status.APPROVED
            self.save(update_fields=['status'])
            return True, "Oferta zatwierdzona! Można generować PDF."
        return False, "Zatwierdzić można tylko oczekującą ofertę."

    def reject(self, reason: str) -> tuple[bool, str]:
        """Odrzuca ofertę wraz z podaniem obowiązkowego powodu."""
        if reason:
            self.status = self.Status.REJECTED
            self.rejection_reason = reason
            self.save(update_fields=['status', 'rejection_reason'])
            return True, f"Oferta odrzucona. Powód: {reason}"
        return False, "Musisz podać powód odrzucenia!"

    def return_to_draft(self) -> tuple[bool, str]:
        """Cofa ofertę odrzuconą lub konsultowaną z powrotem do wersji roboczej."""
        if self.status in [self.Status.REJECTED, self.Status.IN_CONSULTATION]:
            self.status = self.Status.DRAFT
            self.save(update_fields=['status'])
            return True, "Oferta przywrócona do edycji."
        return False, "Nie można cofnąć tej oferty do edycji."

    def send_to_consultation(self) -> tuple[bool, str]:
        """Kieruje ofertę roboczą do konsultacji technicznej IT."""
        if self.status == self.Status.DRAFT:
            self.status = self.Status.IN_CONSULTATION
            self.save(update_fields=['status'])
            return True, "Oferta skierowana do konsultacji IT."
        return False, "Tylko szkic można skierować do konsultacji IT."


class OfferItem(models.Model):
    """Pojedyncza pozycja kosztorysu przypisana do oferty."""
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200, verbose_name="Nazwa produktu / usługi")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Ilość")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena jedn. PLN")
    price_in_eur = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Cena katalogowa EUR"
    )

    @property
    def total_price(self) -> Decimal:
        """Zwraca wartość netto pozycji (ilość * cena jednostkowa)."""
        return self.quantity * self.price_per_unit

    def __str__(self) -> str:
        return self.description


@receiver(post_save, sender=OfferItem)
@receiver(post_delete, sender=OfferItem)
def recalculate_offer_total(sender, instance: OfferItem, **kwargs) -> None:
    """Automatycznie aktualizuje sumę oferty po zmianie jej pozycji."""
    instance.offer.update_total()


class UserProfile(models.Model):
    """Rozszerzenie profilu użytkownika (Handlowca) o dodatkowe dane kontaktowe."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name="Użytkownik"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")

    def __str__(self) -> str:
        return f"Profil: {self.user.username}"

    class Meta:
        verbose_name = "Profil Użytkownika"
        verbose_name_plural = "Profile Użytkowników"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance: User, created: bool, **kwargs) -> None:
    """Automatycznie tworzy lub zapisuje profil przy zapisie obiektu User."""
    if created or not hasattr(instance, 'profile'):
        UserProfile.objects.get_or_create(user=instance)
    else:
        instance.profile.save()
