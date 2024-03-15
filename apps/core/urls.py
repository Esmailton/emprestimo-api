from django.urls import path
from apps.core.api.views.access_token import GenerateTokenView

app_name = "core"

urlpatterns = [
    path('api/generate-token/', GenerateTokenView.as_view(), name='generate_token'),
]
