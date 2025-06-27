from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Produk
from .models import Pelanggan
from .models import Transaksi
from .models import User
from .models import Kategori
from .models import Satuan
from .models import Diskon
from .models import Supplier
from .models import Gudang
from .models import ReturPenjualan
from .models import StokMasuk
from .models import StokKeluar
from .models import Pembelian
from .models import DetailPembelian

ROLE_CHOICES = [
    ('staff', 'Staff'),
    ('admin', 'Admin'),
]

class PelangganForm(forms.ModelForm):
    class Meta:
        model = Pelanggan
        fields = ['nama', 'email', 'no_hp', 'alamat', 'jenis_kelamin']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
        }

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama', 'harga', 'stok', 'kategori', 'deskripsi']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'harga': forms.NumberInput(attrs={'class': 'form-control'}),
            'stok': forms.NumberInput(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['pelanggan', 'produk', 'jumlah', 'catatan']
        widgets = {
            'pelanggan': forms.Select(attrs={'class': 'form-select'}),
            'produk': forms.Select(attrs={'class': 'form-select'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control'}),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama', 'deskripsi', 'aktif']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class SatuanForm(forms.ModelForm):
    class Meta:
        model = Satuan
        fields = ['nama', 'kode', 'deskripsi', 'aktif']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama satuan'
            }),
            'kode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan kode satuan'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Masukkan deskripsi satuan'
            }),
            'aktif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nama': 'Nama Satuan',
            'kode': 'Kode Satuan',
            'deskripsi': 'Deskripsi',
            'aktif': 'Status Aktif'
        }
        
class DiskonForm(forms.ModelForm):
    class Meta:
        model = Diskon
        fields = ['produk', 'persen', 'mulai', 'sampai', 'aktif']
        widgets = {
            'produk': forms.Select(attrs={
                'class': 'form-control'
            }),
            'persen': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan persen diskon'
            }),
            'mulai': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'sampai': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'aktif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'produk': 'Produk',
            'persen': 'Persen Diskon',
            'mulai': 'Tanggal Mulai',
            'sampai': 'Tanggal Sampai',
            'aktif': 'Status Aktif'
        }
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['nama', 'kontak', 'alamat', 'email', 'aktif']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama supplier'
            }),
            'kontak': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan kontak supplier'
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Masukkan alamat supplier'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan email supplier'
            }),
            'aktif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nama': 'Nama Supplier',
            'kontak': 'Kontak Supplier',
            'alamat': 'Alamat Supplier',
            'email': 'Email Supplier',
            'aktif': 'Status Aktif'
        }

class GudangForm(forms.ModelForm):
    class Meta:
        model = Gudang
        fields = ['nama', 'lokasi', 'penanggung_jawab', 'kapasitas', 'aktif']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama gudang'
            }),
            'lokasi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Masukkan lokasi gudang'
            }),
            'penanggung_jawab': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama penanggung jawab'
            }),
            'kapasitas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan kapasitas gudang'
            }),
            'aktif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nama': 'Nama Gudang',
            'lokasi': 'Lokasi Gudang',
            'penanggung_jawab': 'Penanggung Jawab',
            'kapasitas': 'Kapasitas Gudang',
            'aktif': 'Status Aktif'
        }
        
class ReturPenjualanForm(forms.ModelForm):
    class Meta:
        model = ReturPenjualan
        fields = ['penjualan', 'produk', 'qty', 'alasan']
        widgets = {
            'penjualan': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Pilih penjualan'
            }),
            'produk': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Pilih produk'
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan jumlah retur',
                'min': 1
            }),
            'alasan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Masukkan alasan retur'
            }),
        }
        labels = {
            'penjualan': 'Nomor Penjualan',
            'produk': 'Produk',
            'qty': 'Jumlah Retur',
            'alasan': 'Alasan Retur'
        }

class StokMasukForm(forms.ModelForm):
    class Meta:
        model = StokMasuk
        fields = ['produk', 'jumlah', 'supplier', 'keterangan']
        widgets = {
            'produk': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Pilih produk'
            }),
            'jumlah': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan jumlah',
                'min': 1
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Pilih supplier'
            }),
            'keterangan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Masukkan keterangan'
            }),
        }
        labels = {
            'produk': 'Produk',
            'jumlah': 'Jumlah Stok Masuk',
            'supplier': 'Supplier',
            'keterangan': 'Keterangan'
        }
        
        
class StokKeluarForm(forms.ModelForm):
    class Meta:
        model = StokKeluar
        fields = ['produk', 'jumlah', 'alasan', 'keterangan']
        widgets = {
            'produk': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Pilih produk'
            }),
            'jumlah': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan jumlah',
                'min': 1
            }),
            'alasan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan alasan'
            }),
            'keterangan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Masukkan keterangan'
            }),
        }
        labels = {
            'produk': 'Produk',
            'jumlah': 'Jumlah Stok Keluar',
            'alasan': 'Alasan',
            'keterangan': 'Keterangan'
        }
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan email'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Konfirmasi password'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Konfirmasi Password',
            'role': 'Role',
        }
        
class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan email'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'role': 'Role',
        }
        
class PembelianForm(forms.ModelForm):
    class Meta:
        model = Pembelian
        fields = ['supplier', 'total', 'status', 'keterangan']
        widgets = {
            'keterangan': forms.Textarea(attrs={'rows': 3}),
        }
    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total < 0:
            raise forms.ValidationError("Total tidak boleh negatif.")
        return total
    
class DetailPembelianForm(forms.ModelForm):
    class Meta:
        model = DetailPembelian
        fields = ['pembelian', 'produk', 'qty', 'harga_beli', 'subtotal']
    
    def clean_qty(self):
        qty = self.cleaned_data.get('qty')
        if qty <= 0:
            raise forms.ValidationError("Jumlah harus lebih dari nol.")
        return qty
    def clean_harga_beli(self):
        harga_beli = self.cleaned_data.get('harga_beli')
        if harga_beli < 0:
            raise forms.ValidationError("Harga beli tidak boleh negatif.")
        return harga_beli
    def clean_subtotal(self):
        qty = self.cleaned_data.get('qty')
        harga_beli = self.cleaned_data.get('harga_beli')
        if qty and harga_beli:
            subtotal = qty * harga_beli
            return subtotal
        return 0  # Atau bisa juga raise ValidationError jika ingin