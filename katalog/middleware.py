# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        # Daftar URL yang tidak memerlukan autentikasi
        exempt_urls = [reverse('login'), reverse('signup')]  # Ganti dengan nama URL login dan signup Anda
        # Cek apakah pengguna tidak terautentikasi dan bukan di halaman login atau signup
        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('login')  # Ganti dengan nama URL login Anda
        response = self.get_response(request)
        return response