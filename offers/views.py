from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import uuid
from django.conf import settings
from .models import Offer, OfferItem
from .forms import OfferForm, OfferItemFormSet
from weasyprint import HTML, CSS
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from datetime import timedelta
from django.contrib import messages
import os
import logging

logger = logging.getLogger(__name__)

@login_required
def home(request):
    """Widok dashboardu (kafelki)."""
    return render(request, 'offers/home.html')

@login_required
def offer_list(request):
    """Widok listy wszystkich ofert."""
    offers = Offer.objects.all().order_by('-created_at')
    return render(request, 'offers/offer_list.html', {'offers': offers})

@login_required
def offer_detail(request, pk):
    """Widok szczegółów oferty."""
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'offers/offer_details.html', {'offer': offer})

@login_required
def offer_create(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)

        if form.is_valid():
            offer = form.save(commit=False)
            offer.created_by = request.user
            offer.save()  # Zapisujemy, żeby mieć ID. Numer oferty generuje się automatycznie w save() modelu.

            # Podpinamy produkty pod ofertę
            formset = OfferItemFormSet(request.POST, instance=offer)

            if formset.is_valid():
                formset.save()

                return redirect('offer_detail', pk=offer.pk)
            else:
                logger.error(f"Błąd formsetu produktów: {formset.errors}")
                offer.delete()  # Usuwamy pustą ofertę
        else:
            logger.error(f"Błąd formularza głównego: {form.errors}")

    else:
        form = OfferForm()
        formset = OfferItemFormSet()

    return render(request, 'offers/offer_create.html', {
        'form': form,
        'formset': formset
    })


# --- WIDOK: EDYCJA OFERTY ---
@login_required
def offer_edit(request, pk):
    offer = get_object_or_404(Offer, pk=pk)

    # --- SECURITY CHECK ---
    # Jeśli oferta nie jest w trybie DRAFT i nie jest ODRZUCONA, blokujemy edycję
    # --- POPRAWKA: Pozwalamy edytować też w trakcie konsultacji ---
    if offer.status not in [Offer.Status.DRAFT, Offer.Status.IN_CONSULTATION, Offer.Status.REJECTED]:
        messages.error(request, "Nie można edytować oferty, która została już wysłana lub zatwierdzona.")
        return redirect('offer_detail', pk=pk)
    # ----------------------

    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        formset = OfferItemFormSet(request.POST, instance=offer)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            return redirect('offer_detail', pk=offer.pk)
        else:
            logger.error(f"Błąd edycji. Form errors: {form.errors}, Formset errors: {formset.errors}")

    else:
        form = OfferForm(instance=offer)
        formset = OfferItemFormSet(instance=offer)

    return render(request, 'offers/offer_create.html', {
        'form': form,
        'formset': formset,
        'offer': offer
    })


# --- WIDOK: PDF  ---
@login_required
def offer_pdf(request, pk):
    offer = get_object_or_404(Offer, pk=pk)

    # --- KONFIGURACJA ŚCIEŻEK ---

    if not settings.DEBUG:
        # --- PRODUKCJA (PythonAnywhere) ---
        css_path = '/home/jakub3011/offert_system_basic/staticfiles/offers/pdf_style.css'
    else:
        # --- LOKALNIE (Docker) ---
        css_path = os.path.join(settings.BASE_DIR, 'offers', 'static', 'offers', 'pdf_style.css')

    # Logo z dysku (WeasyPrint wymaga ścieżki lokalnej file://)
    if offer.seller and offer.seller.logo:
        logo_url = 'file://' + offer.seller.logo.path
    else:
        logo_url = None

    logger.debug(f"Generowanie PDF: TRYB={'PRODUKCJA' if not settings.DEBUG else 'LOKALNY'}, CSS={css_path}")

    # --- RENDEROWANIE ---
    context = {
        'offer': offer,
        'logo_url': logo_url,
    }

    html_string = render_to_string('offers/offer_pdf.html', context)

    # base_url='' - nie pozwalamy WeasyPrintowi błądzić po sieci
    html = HTML(string=html_string, base_url='')

    if os.path.exists(css_path):
        try:
            css = CSS(filename=css_path)
            pdf_file = html.write_pdf(stylesheets=[css])
            logger.debug("CSS załadowany poprawnie.")
        except Exception as e:
            logger.error(f"Błąd ładowania CSS: {e}")
            pdf_file = html.write_pdf()
    else:
        logger.warning("Plik CSS nie istnieje. Generowanie PDF bez stylów.")
        pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="Oferta_{offer.offer_number}.pdf"'
    return response


def offer_reject(request, pk):
    """Widok do podania powodu odrzucenia oferty."""
    offer = get_object_or_404(Offer, pk=pk)

    if request.method == 'POST':
        reason = request.POST.get('rejection_reason')
        success, message = offer.reject(reason)
        if success:
            messages.warning(request, message)
            return redirect('offer_list')
        else:
            messages.error(request, message)

    return render(request, 'offers/offer_reject.html', {'offer': offer})


@login_required
def offer_change_status(request, pk, action):
    """Zmiana statusu oferty z uwzględnieniem logiki i uprawnień."""
    offer = get_object_or_404(Offer, pk=pk)

    if action == 'submit':
        success, message = offer.submit_for_approval()
        if success:
            messages.success(request, message)
        else:
            messages.warning(request, message)

    elif action == 'approve':
        success, message = offer.approve(request.user)
        if success:
            messages.success(request, message)
        else:
            if "uprawnień" in message:
                messages.error(request, message)
            else:
                messages.warning(request, message)

    elif action == 'reject':
        if request.method == 'POST':
            reason = request.POST.get('rejection_reason')
            success, message = offer.reject(reason)
            if success:
                messages.warning(request, message)
                return redirect('offer_list')
            else:
                messages.error(request, message)
        return render(request, 'offers/offer_reject.html', {'offer': offer})

    elif action == 'draft':
        success, message = offer.return_to_draft()
        if success:
            messages.info(request, message)
        else:
            messages.warning(request, message)

    return redirect('offer_list')
