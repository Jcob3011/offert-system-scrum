from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from offers import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='api-company')
router.register(r'clients', views.ClientViewSet, basename='api-client')
router.register(r'sellers', views.SellerViewSet, basename='api-seller')
router.register(r'offers', views.OfferViewSet, basename='api-offer')
router.register(r'offer-items', views.OfferItemViewSet, basename='api-offeritem')

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- REST API, JWT & SWAGGER (Wersja 2.0 Headless Backend) ---
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
