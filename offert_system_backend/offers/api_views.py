from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Company, Client, Seller, Offer, OfferItem
from .serializers import (
    CompanySerializer,
    ClientSerializer,
    SellerSerializer,
    OfferSerializer,
    OfferItemSerializer,
)


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
    Główny ViewSet obsługujący oferty handlowe wraz z maszyną stanów
    i kontrolą uprawnień edycji (ACL).
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
        """Cofa odrzuconą ofertę do wersji roboczej (POST /api/offers/{id}/return_to_draft/)."""
        offer: Offer = self.get_object()
        success, message = offer.return_to_draft()
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message, 'status': offer.status}, status=http_status)

    @action(detail=True, methods=['post'])
    def consult(self, request:Request, pk: int | None = None) -> Response:
        offer: Offer = self.get_object()
        success, message = offer.send_to_consultation()
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({'success': success, 'message': message, 'status': offer.status},status=http_status)
