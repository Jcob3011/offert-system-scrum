from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.contrib.auth.models import User
from decimal import Decimal

"""
Modele odpowiadające za system CRM oraz tworzenie ofert.
"""

class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa Firmy")
    nip = models.CharField(max_length=20, blank=True, null=True, verbose_name="NIP")
    address = models.TextField(verbose_name="Adres", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Baza Firm"


class Client(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees', verbose_name="Firma")
    first_name = models.CharField(max_length=100, verbose_name="Imię")
    last_name = models.CharField(max_length=100, verbose_name="Nazwisko")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    position = models.CharField(max_length=100, blank=True,
                                verbose_name="Stanowisko")  # np. "Dyrektor IT" vs "Serwisant"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company.name})"

    class Meta:
        verbose_name = "Klient / Kontakt"
        verbose_name_plural = "Baza Klientów"


class Seller(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa Naszej Firmy")
    nip = models.CharField(max_length=20, verbose_name="NIP")
    address = models.TextField(verbose_name="Adres")
    email = models.EmailField(verbose_name="Email kontaktowy", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Telefon", blank=True)
    bank_account = models.CharField(max_length=50, verbose_name="Konto Bankowe", blank=True)

    # Logo - ważne! Wymaga biblioteki Pillow
    logo = models.ImageField(upload_to='company_logos/', verbose_name="Logo", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Nazwa Firmy"
        verbose_name_plural = "Nasze Firmy"



class Offer(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Robocza')
        PENDING = 'pending', _('Oczekuje na akceptację')
        IN_CONSULTATION = 'consultation', _('Konsultacja')
        APPROVED = 'approved', _('Zatwierdzona')
        SENT = 'sent', _('Wysłana')
        REJECTED = 'rejected', _('Odrzucona')

    class PaymentMethod(models.TextChoices):  # NOWOŚĆ (6)
        TRANSFER = 'transfer', _('Przelew tradycyjny')
        SPLIT_PAYMENT = 'split', _('Przelew (Split Payment)')
        CASH = 'cash', _('Gotówka')
        CARD = 'card', _('Karta płatnicza')

    # Powiązania
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, verbose_name="Wystawca", null=True)
    offer_number = models.CharField(max_length=50, unique=True, verbose_name="Numer oferty")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Klient", null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name="Status")
    description = RichTextField(null=True, blank=True, help_text="Wstęp/Opis oferty")
    
    # Finanse
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Suma PLN")
    currency_rate = models.DecimalField(max_digits=6, decimal_places=4, default=1.0000,
                                        verbose_name="Kurs EUR (dla informacji)")

    # Terminy i Płatności
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validity_days = models.PositiveIntegerField(default=14, verbose_name="Ważność oferty (dni)")
    payment_deadline_days = models.PositiveIntegerField(default=7, verbose_name="Termin płatności (dni)")
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.TRANSFER,
                                      verbose_name="Metoda płatności")

    # Informacje dodatkowe
    rejection_reason = models.TextField(blank=True, null=True, verbose_name="Powód odrzucenia (CEO)")

    external_file = models.FileField(upload_to='offers_archive/', null=True, blank=True, verbose_name="Archiwalny PDF")
    # Kto utworzył oferte
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utworzył")

    def update_total(self):
        """
        Przelicza sumę oferty na podstawie pozycji.
        """
        # 1. Pobieramy wszystkie pozycje tej oferty
        offer_items = self.items.all()

        # 2. Sumujemy (używając property total_price z items)
        new_total = sum(item.total_price for item in offer_items)

        # 3. Zapisujemy wynik w bazie
        self.total_price = new_total
        # Używamy update_fields, żeby nie nadpisywać innych pól (optymalizacja)
        self.save(update_fields=['total_price'])

    def __str__(self):
        return f"{self.offer_number}"

    # Metoda pomocnicza do szablonu - kiedy wygasa?
    @property
    def valid_until_date(self):
        return self.created_at.date() + timedelta(days=self.validity_days)

    @property
    def css_class(self):
        return f"status-{self.status}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Oferta"
        verbose_name_plural = "Baza Ofert"
    def get_total_vat(self):
        """Oblicza kwotę samego podatku VAT (23%)"""
        return (self.total_price * Decimal('0.23')).quantize(Decimal('0.01'))

    def get_total_gross(self):
        """Oblicza kwotę Brutto (Netto + VAT)"""
        return (self.total_price * Decimal('1.23')).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        """Generuje sekwencyjny numer oferty X/MM/YYYY przed pierwszym zapisem."""
        if not self.offer_number:
            from django.utils import timezone
            now = timezone.now()
            current_month = now.month
            current_year = now.year

            # Liczymy istniejące oferty z tego samego miesiąca i roku
            count = Offer.objects.filter(
                created_at__month=current_month,
                created_at__year=current_year
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

    def submit_for_approval(self):
        """Przesyła ofertę do akceptacji."""
        if self.status == self.Status.DRAFT:
            self.status = self.Status.PENDING
            self.save(update_fields=['status'])
            return True, f"Oferta {self.offer_number} wysłana do akceptacji."
        return False, "Tylko szkic można wysłać do akceptacji."

    def approve(self, user):
        """Zatwierdza ofertę (wymagane uprawnienia superusera)."""
        if not user.is_superuser:
            return False, "Brak uprawnień (wymagany CEO)."
        if self.status == self.Status.PENDING:
            self.status = self.Status.APPROVED
            self.save(update_fields=['status'])
            return True, "Oferta zatwierdzona! Można generować PDF."
        return False, "Zatwierdzić można tylko oczekującą ofertę."

    def reject(self, reason):
        """Odrzuca ofertę wraz z podaniem powodu."""
        if reason:
            self.status = self.Status.REJECTED
            self.rejection_reason = reason
            self.save(update_fields=['status', 'rejection_reason'])
            return True, f"Oferta odrzucona. Powód: {reason}"
        return False, "Musisz podać powód odrzucenia!"

    def return_to_draft(self):
        """Cofa ofertę odrzuconą z powrotem do wersji roboczej."""
        if self.status == self.Status.REJECTED:
            self.status = self.Status.DRAFT
            self.save(update_fields=['status'])
            return True, "Oferta przywrócona do edycji."
        return False, "Nie można cofnąć do edycji."

class OfferItem(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200, verbose_name="Nazwa produktu")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Ilość")

    # Cena jednostkowa w PLN (ostateczna)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena jedn. PLN")

    # Opcjonalnie: Oryginalna cena w EUR (tylko do podglądu)
    price_in_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       verbose_name="Cena katalogowa EUR")

    @property
    def total_price(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return self.description


@receiver(post_save, sender=OfferItem)
@receiver(post_delete, sender=OfferItem)
def recalculate_offer_total(sender, instance, **kwargs):
    offer = instance.offer
    offer.update_total()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Użytkownik")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")

    def __str__(self):
        return f"Profil: {self.user.username}"

    class Meta:
        verbose_name = "Profil Użytkownika"
        verbose_name_plural = "Profile Użytkowników"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()
