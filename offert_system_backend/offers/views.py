"""
Widoki REST API (ViewSety) obsługujące moduł CRM, obieg ofert oraz generowanie dokumentów PDF.
"""
import logging
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from weasyprint import CSS, HTML
from .models import Client, Company, Offer, OfferItem, Seller
from .serializers import (
    ClientSerializer,
    CompanySerializer,
    OfferItemSerializer,
    OfferSerializer,
    SellerSerializer,
)

logger = logging.getLogger(__name__)


class CompanyViewSet(viewsets.ModelViewSet):
    """Endpointy REST API do zarządzania bazą firm (kontrahentów)."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ClientViewSet(viewsets.ModelViewSet):
    """Endpointy REST API do zarządzania osobami kontaktowymi (klientami)."""
    queryset = Client.objects.select_related('company').all()
    serializer_class = ClientSerializer


class SellerViewSet(viewsets.ModelViewSet):
    """Endpointy REST API do zarządzania naszymi spółkami (wystawcami)."""
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class OfferItemViewSet(viewsets.ModelViewSet):
    """Endpointy REST API do zarządzania pozycjami kosztorysu."""
    queryset = OfferItem.objects.select_related('offer').all()
    serializer_class = OfferItemSerializer


class OfferViewSet(viewsets.ModelViewSet):
    """
    Główny ViewSet obsługujący oferty handlowe wraz z maszyną stanów,
    kontrolą uprawnień edycji (ACL) oraz generowaniem dokumentu PDF.
    """
    queryset = Offer.objects.select_related('seller', 'client', 'created_by').prefetch_related('items').all()
    serializer_class = OfferSerializer

    def perform_create(self, serializer: OfferSerializer) -> None:
        """Automatycznie przypisuje zalogowanego użytkownika jako twórcę oferty."""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer: OfferSerializer) -> None:
        """Blokuje edycję oferty przez API, jeśli została już wysłana lub zatwierdzona (ACL)."""
        offer: Offer = self.get_object()
        editable_statuses = [Offer.Status.DRAFT, Offer.Status.IN_CONSULTATION, Offer.Status.REJECTED]
        if offer.status not in editable_statuses:
            raise PermissionDenied("Nie można edytować oferty, która została już wysłana lub zatwierdzona.")
        serializer.save()

    @action(detail=True, methods=['post'])
    def submit(self, request: Request, pk: int | None = None) -> Response:
        """Przesyła ofertę roboczą do akceptacji CEO (POST /api/offers/{id}/submit/)."""
        offer: Offer = self.get_object()
        success, message = offer.submit_for_approval()
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message, 'status': offer.status}, status=http_status)

    @action(detail=True, methods=['post'])
    def approve(self, request: Request, pk: int | None = None) -> Response:
        """Zatwierdza ofertę – wymaga uprawnień superusera/CEO (POST /api/offers/{id}/approve/)."""
        offer: Offer = self.get_object()
        success, message = offer.approve(request.user)
        if not success and "uprawnień" in message:
            return Response({'success': False, 'message': message}, status=status.HTTP_403_FORBIDDEN)
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message, 'status': offer.status}, status=http_status)

    @action(detail=True, methods=['post'])
    def reject(self, request: Request, pk: int | None = None) -> Response:
        """Odrzuca ofertę z podaniem powodu (POST /api/offers/{id}/reject/)."""
        offer: Offer = self.get_object()
        reason: str = request.data.get('rejection_reason', '')
        success, message = offer.reject(reason)
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message, 'status': offer.status}, status=http_status)

    @action(detail=True, methods=['post'])
    def return_to_draft(self, request: Request, pk: int | None = None) -> Response:
        """Cofa odrzuconą lub konsultowaną ofertę do wersji roboczej (POST /api/offers/{id}/return_to_draft/)."""
        offer: Offer = self.get_object()
        success, message = offer.return_to_draft()
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message, 'status': offer.status}, status=http_status)

    @action(detail=True, methods=['post'])
    def consult(self, request: Request, pk: int | None = None) -> Response:
        """Kieruje ofertę roboczą do konsultacji technicznej IT (POST /api/offers/{id}/consult/)."""
        offer: Offer = self.get_object()
        success, message = offer.send_to_consultation()
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message, 'status': offer.status}, status=http_status)

    @action(detail=True, methods=['get'])
    def pdf(self, request: Request, pk: int | None = None) -> HttpResponse:
        """Generuje i zwraca dokument PDF dla wybranej oferty (GET /api/offers/{id}/pdf/)."""
        offer: Offer = self.get_object()

        if not settings.DEBUG:
            css_path = os.path.join(settings.STATIC_ROOT, 'offers', 'pdf_style.css')
        else:
            css_path = os.path.join(settings.BASE_DIR, 'offers', 'static', 'offers', 'pdf_style.css')

        logo_url = f"file://{offer.seller.logo.path}" if (offer.seller and offer.seller.logo) else None

        html_string = render_to_string('offers/offer_pdf.html', {
            'offer': offer,
            'logo_url': logo_url,
        })
        html = HTML(string=html_string, base_url='')

        stylesheets = [CSS(filename=css_path)] if os.path.exists(css_path) else []
        pdf_file = html.write_pdf(stylesheets=stylesheets)

        safe_number = offer.offer_number.replace('/', '_')
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Oferta_{safe_number}.pdf"'
        return response
