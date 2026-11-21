import pytest
from  decimal import Decimal
from .models import Seller, Company, Client, Offer, OfferItem
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def sample_offer(db) -> Offer:
    seller = Seller.objects.create(name="Nasza Spółka", nip="111", address="Warszawa")
    company = Company.objects.create(name="Klinet SP.Z.O.O", nip="2222", address="Kraków")
    client= Client.objects.create(company=company, first_name="Jan", last_name="Nowak", email="jan@klient.pl")
    return Offer.objects.create(seller=seller, client=client)

def test_financial_calculations(sample_offer: Offer) -> None:
    OfferItem.objects.create(
        offer=sample_offer,
        description="Usługa IT",
        quantity=2,
        price_per_unit=Decimal("100.00")
        )

    assert sample_offer.total_price == Decimal("200.00")
    assert sample_offer.get_total_vat() == Decimal("46.00")
    assert sample_offer.get_total_gross() == Decimal("246.00")


def test_send_to_consulation(sample_offer: Offer) -> None:
    success, message = sample_offer.send_to_consultation()
    assert success == True
    assert sample_offer.status == Offer.Status.IN_CONSULTATION

def test_send_to_user_cannot_approve_offer(sample_offer: Offer) -> None:
    success, message = sample_offer.submit_for_approval()
    handlowiec = User.objects.create_user(username="handlowiec", password="123")
    success, message = sample_offer.approve(handlowiec)
    assert success == False
    assert sample_offer.status == Offer.Status.PENDING

def test_ceo_can_approve_offer(sample_offer: Offer) -> None:
    success, message = sample_offer.submit_for_approval()
    assert success == True
    CEO = User.objects.create_superuser(username="CEO", password="123")
    success, message = sample_offer.approve(CEO)
    assert success == True

@pytest.mark.django_db
def test_api_blocks_unauthorized(sample_offer: Offer) -> None:
    client = APIClient()
    response = client.get('/api/offers/')
    assert response.status_code == 401
