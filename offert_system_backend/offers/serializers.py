from rest_framework import serializers
from .models import Company, Client, Seller, Offer , OfferItem


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'nip', 'address']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'company', 'first_name', 'last_name', 'email', 'phone', 'position']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'nip', 'address', 'email', 'phone', 'bank_account', 'logo']

class OfferItemSerializer(serializers.ModelSerializer):
    # Pole tylko do odczytu (wyliczane przez @property w modelu!)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = OfferItem
        fields = ['id', 'description', 'quantity', 'price_per_unit', 'price_in_eur', 'total_price']

class OfferSerializer(serializers.ModelSerializer):

    items = OfferItemSerializer(many=True, read_only=True)

    total_vat = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_total_vat', read_only=True)
    total_gross = serializers.DecimalField(max_digits=10, decimal_places=2, source='get_total_gross', read_only=True)

    class Meta:
        model = Offer
        fields = [ 'id', 'offer_number', 'seller', 'client', 'status',
            'description', 'total_price', 'total_vat', 'total_gross',
            'currency_rate', 'validity_days', 'payment_deadline_days',
            'payment_method', 'rejection_reason', 'created_by',
            'created_at', 'valid_until_date', 'items']

        read_only_fields = ['id', 'offer_number', 'total_price', 'created_by', 'created_at', 'valid_until_date']
