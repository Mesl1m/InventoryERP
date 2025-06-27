from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from .decorators import role_required


import datetime
import json

from .models import (
    Produk,
    Pelanggan,
    Penjualan,
    Supplier,
    Transaksi,
    Kategori,
    StokMasuk,
    StokKeluar,
    ReturPenjualan,
    User,
    Gudang,
    Diskon,
    LogAktivitas,
    Pembelian,
    DetailPembelian,
    Satuan,
)
from .forms import (
    ProdukForm,
    PelangganForm,
    TransaksiForm,
    # RegisterForm,
    KategoriForm,
    SatuanForm,
    DiskonForm,
    SupplierForm,
    GudangForm,
    ReturPenjualanForm,
    StokKeluarForm,
    StokMasukForm,
    UserRegistrationForm,
    UserEditForm,
    DetailPembelianForm,
    PembelianForm,
)

# Create your views here.
def dashboard(request):
    total_produk = Kategori.objects.all().count()
    total_pelanggan = Kategori.objects.all().count()
    total_transaksi_hari_ini = Kategori.objects.all().count()
    total_kategori = Kategori.objects.all().count()
    context = {
        'total_produk': total_produk,
        'total_pelanggan': total_pelanggan,
        'total_transaksi_hari_ini': total_transaksi_hari_ini,
        'total_kategori': total_kategori,
    }
    return render(request, 'katalog/dashboard.html', context)


#produk
def list_produk(request):
    produk_list = Produk.objects.all()

    # Buat instance dari ProdukForm
    form = ProdukForm()

    return render(request, 'katalog/list_produk.html', {
        'produk_list': produk_list,
        'form': form,  # Kirimkan form ke template
    })

def tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_produk')
    else:
        form = ProdukForm()

    return render(request, 'katalog/list_produk.html', {
        'produk_list': Produk.objects.all(),
        'form': form,
    })

def edit_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_produk')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'nama': produk.nama,
            'harga': produk.harga,
            'stok': produk.stok,
            'kategori': produk.kategori.id,
            'deskripsi': produk.deskripsi,
        }
        return JsonResponse(data)
    form = ProdukForm(instance=produk)
    return render(request, 'katalog/list_produk.html', {'form': form, 'judul': 'Edit Produk'})

def hapus_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        produk.delete()
        return redirect('list_produk')
    return render(request, 'katalog/list_produk.html', {'produk': produk})


#pelangan
def list_pelanggan(request):
    # Ambil semua data pelanggan
    all_pelanggan = Pelanggan.objects.all()
    # Ambil data pelanggan bulanan
    today = timezone.now().date()
    start_date = today - datetime.timedelta(days=30)
    monthly_counts = Pelanggan.objects.filter(
        tanggal_bergabung__range=[start_date, today]
    ).annotate(
        day=TruncDay('tanggal_bergabung')
    ).values('day').annotate(count=Count('id')).order_by('day')
    # Format data untuk chart
    labels = [item['day'].strftime('%d %b') for item in monthly_counts]
    print("labels", labels)
    data = [item['count'] for item in monthly_counts]
    print("data", data)
    # Buat form untuk pelanggan baru
    form = PelangganForm()
    # Siapkan konteks untuk dikirim ke template
    context = {
        'pelanggan': all_pelanggan,  # Kirim semua pelanggan
        'form': form,
        'monthly_labels': labels,  # Kirim label untuk chart
        'monthly_data': data       # Kirim data untuk chart
    }
    print(context)  # Tambahkan ini untuk debugging
    return render(request, 'katalog/list_pelanggan.html', context)

def daftar_pelanggan(request):
    pelanggan = Pelanggan.objects.all()
    # Ambil data pelanggan bulanan
    today = timezone.now().date()
    start_date = today - datetime.timedelta(days=30)
    monthly_counts = Pelanggan.objects.filter(
        tanggal_bergabung__range=[start_date, today]
    ).annotate(
        day=TruncDay('tanggal_bergabung')
    ).values('day').annotate(count=Count('id')).order_by('day')
    # Format data untuk chart
    labels = [item['day'].strftime('%d %b') for item in monthly_counts]
    print("labels", labels)
    data = [item['count'] for item in monthly_counts]
    context = {
        'pelanggan': pelanggan,
        'monthly_labels': labels,
        'monthly_data': data,
    }
    print(context)  # Tambahkan ini untuk debugging
    return render(request, 'list_pelanggan.html', context)

def tambah_pelanggan(request):
    if request.method == 'POST':
        form = PelangganForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_pelanggan')
    else:
        form = PelangganForm()

    return render(request, 'katalog/list_pelanggan.html', {
        'data' : Pelanggan.objects.all(),
        'form': form,
        'judul': 'Tambah Pelanggan'
    })

def edit_pelanggan(request, pk):
    pelanggan = get_object_or_404(Pelanggan, pk=pk)

    if request.method == 'POST':
        form = PelangganForm(request.POST, instance=pelanggan)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_pelanggan')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'nama': pelanggan.nama,
            'email': pelanggan.email,
            'no_hp': pelanggan.no_hp,
            'alamat': pelanggan.alamat,
            'jenis_kelamin': pelanggan.jenis_kelamin,
        }
        return JsonResponse(data)

    form = PelangganForm(instance=pelanggan)
    return render(request, 'katalog/list_pelanggan.html', {'form': form, 'judul': 'Edit Pelanggan'})

def hapus_pelanggan(request, pk):
    pelanggan = get_object_or_404(Pelanggan, pk=pk)
    if request.method == 'POST':
        pelanggan.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('list_pelanggan')
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)



#transaksi
def list_transaksi(request):
    transaksi_list = Transaksi.objects.all()
    form = TransaksiForm()
    return render(request, 'katalog/list_transaksi.html', {
        'transaksi': transaksi_list,
        'form' : form
    })

def tambah_transaksi(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_transaksi')
    else:
        form = TransaksiForm()

    return render(request, 'katalog/list_transaksi.html', {
        'transaksi_list' : Transaksi.objects.all(),
        'form': form,
        'judul': 'Tambah Transaksi'
    })

def edit_transaksi(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)

    if request.method == 'POST':
        form = TransaksiForm(request.POST, instance=transaksi)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_transaksi')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'pelanggan': {'nama': transaksi.pelanggan.nama},  # Adjust based on your model
            'produk': {'nama': transaksi.produk.nama},  # Adjust based on your model
            'jumlah': transaksi.jumlah,
            'tanggal': transaksi.tanggal,
            'catatan': transaksi.catatan,
        }
        return JsonResponse(data)

    form = TransaksiForm(instance=transaksi)
    return render(request, 'list_pelanggan.html', {'form': form})

def hapus_transaksi(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    if request.method == 'POST':
        transaksi.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('list_transaksi')
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


#kategori
@role_required('admin')
def list_kategori(request):
    kategori_list = Kategori.objects.all()
    diskon_list = Diskon.objects.all()
    satuan_list = Satuan.objects.all()
    
    formKategori = KategoriForm()
    formSatuan = SatuanForm()
    formDiskon = DiskonForm()
     
    return render(request, 'katalog/list_kategori.html', {
        'kategori' : kategori_list,
        'diskon': diskon_list,
        'satuan': satuan_list,
        'formKategori' : formKategori,
        'formSatuan' : formSatuan,
        'formDiskon' : formDiskon
    })
    
def tambah_kategori(request):
    if request.method == 'POST':
        formKategori = KategoriForm(request.POST)
        if formKategori.is_valid():
            formKategori.save()
            return redirect('list_kategori')
    else:
        formKategori = KategoriForm()

    return render(request, 'katalog/list_kategori.html', {
        'kategori_list' : Kategori.objects.all(),
        'formKategori': formKategori,
        'judul': 'Tambah Kategori'
    })
    
def tambah_satuan(request):
       if request.method == 'POST':
           formSatuan = SatuanForm(request.POST)
           if formSatuan.is_valid():
               formSatuan.save()
               return redirect('list_kategori')  # Tetap redirect ke list_kategori.html
       else:
           formSatuan = SatuanForm()
       
       # Tetap render list_kategori.html tapi dengan semua data
       return render(request, 'katalog/list_kategori.html', {
           'kategori': Kategori.objects.all(),
           'satuan': Satuan.objects.all(),
           'formSatuan': formSatuan
       })
       
def tambah_diskon(request):
    if request.method == 'POST':
        formDiskon = DiskonForm(request.POST)
        if formDiskon.is_valid():
            formDiskon.save()
            return redirect('list_kategori')  # Redirect ke list_kategori setelah berhasil menyimpan
    else:
        formDiskon = DiskonForm()  # Inisialisasi form jika bukan POST
    # Render list_kategori.html dengan data kategori, satuan, dan formDiskon
    return render(request, 'katalog/list_kategori.html', {
        'kategori': Kategori.objects.all(),
        'satuan': Satuan.objects.all(),
        'formDiskon': formDiskon  # Ganti formSatuan dengan formDiskon
    })

def edit_kategori(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_kategori')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'nama': kategori.nama,
            'deskripsi': kategori.deskripsi,
            'aktif': kategori.aktif,
        }
        return JsonResponse(data)
    form = KategoriForm(instance=kategori)
    return render(request, 'edit_kategori.html', {
        'formKategori': form, 
        'kategori': kategori
    })

def edit_satuan(request, pk):
    satuan = get_object_or_404(Satuan, pk=pk)
    if request.method == 'POST':
        form = SatuanForm(request.POST, instance=satuan)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('satuan_list')  # Ganti dengan URL yang sesuai jika perlu
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'nama': satuan.nama,
            'kode': satuan.kode,
            'deskripsi': satuan.deskripsi,
            'aktif': satuan.aktif,
        }
        return JsonResponse(data)
    
    form = SatuanForm(instance=satuan)
    return render(request, 'edit_satuan.html', {
        'formSatuan': form, 
        'satuan': satuan
    })
    
def edit_diskon(request, pk):
    diskon = get_object_or_404(Diskon, pk=pk)
    if request.method == 'POST':
        form = DiskonForm(request.POST, instance=diskon)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('diskon_list')  # Ganti dengan URL yang sesuai jika perlu
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'produk': diskon.produk.id,  # Mengembalikan ID produk
            'persen': diskon.persen,
            'mulai': diskon.mulai,
            'sampai': diskon.sampai,
            'aktif': diskon.aktif,
        }
        return JsonResponse(data)
    
    form = DiskonForm(instance=diskon)
    return render(request, 'edit_diskon.html', {
        'formDiskon': form, 
        'diskon': diskon
    })

def hapus_kategori(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    if request.method == 'POST':
        kategori.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

def hapus_diskon(request, pk):
    diskon = get_object_or_404(Diskon, pk=pk)  # Ganti dengan model Diskon
    if request.method == 'POST':
        diskon.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

def hapus_satuan(request, pk):
    satuan = get_object_or_404(Satuan, pk=pk)  # Ganti dengan model Satuan
    if request.method == 'POST':
        satuan.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})


#supplier
@role_required('admin')
def list_supplier(request):
    supplier_list = Supplier.objects.all()
    gudang_list = Gudang.objects.all()
    retur_penjualan_list = ReturPenjualan.objects.all()
    
    formSupplier = SupplierForm()
    formGudang = GudangForm()
    formRetur = ReturPenjualanForm()
    
    return render(request, 'katalog/list_supplier.html', {
        'supplier': supplier_list,
        'gudang': gudang_list,
        'retur_penjualan': retur_penjualan_list,
        'formSupplier' : formSupplier,
        'formGudang' : formGudang,
        'formRetur' : formRetur,
    })
    
def tambah_supplier(request):
    if request.method == 'POST':
        formSupplier = SupplierForm(request.POST)
        if formSupplier.is_valid():
            formSupplier.save()
            return redirect('list_supplier')
    else:
        formSupplier = SupplierForm()

    return render(request, 'katalog/list_supplier.html', {
        'supplier_list' : Supplier.objects.all(),
        'formSupplier': formSupplier,
        'judul': 'Tambah Kategori'
    })
    
def tambah_gudang(request):
    if request.method == 'POST':
        formGudang = GudangForm(request.POST)
        if formGudang.is_valid():
            formGudang.save()
            return redirect('list_supplier')  # Ganti dengan URL yang sesuai untuk daftar gudang
    else:
        formGudang = GudangForm()
    return render(request, 'katalog/list_supplier.html', {
        'gudang_list': Gudang.objects.all(),
        'formGudang': formGudang,
        'judul': 'Tambah Gudang'
    })
    
def tambah_retur(request):
    if request.method == 'POST':
        formRetur = ReturPenjualanForm(request.POST)
        if formRetur.is_valid():
            formRetur.save()
            return redirect('list_supplier')  # Ganti dengan URL yang sesuai untuk daftar retur
    else:
        formRetur = ReturPenjualanForm()
    return render(request, 'katalog/list_supplier.html', {
        'retur_list': ReturPenjualan.objects.all(),
        'formRetur': formRetur,
        'judul': 'Tambah Retur Penjualan'
    })

def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_supplier')  # Ganti dengan URL yang sesuai jika perlu
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'nama': supplier.nama,
            'kontak': supplier.kontak,
            'alamat': supplier.alamat,
            'email': supplier.email,
            'aktif': supplier.aktif,
        }
        return JsonResponse(data)
    
    form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {
        'formSupplier': form, 
        'supplier': supplier
    })

def edit_gudang(request, pk):
    gudang = get_object_or_404(Gudang, pk=pk)
    if request.method == 'POST':
        form = GudangForm(request.POST, instance=gudang)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_supplier')  # Ganti dengan URL yang sesuai jika perlu
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'nama': gudang.nama,
            'lokasi': gudang.lokasi,
            'penanggung_jawab': gudang.penanggung_jawab,
            'kapasitas': gudang.kapasitas,
            'aktif': gudang.aktif,
        }
        return JsonResponse(data)
    
    form = GudangForm(instance=gudang)
    return render(request, 'list_supplier.html', {
        'formGudang': form, 
        'gudang': gudang
    })
    
def edit_retur(request, pk):
    retur = get_object_or_404(ReturPenjualan, pk=pk)
    if request.method == 'POST':
        form = ReturPenjualanForm(request.POST, instance=retur)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_retur')  # Ganti dengan URL yang sesuai jika perlu
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'penjualan': retur.penjualan.id,  # Mengembalikan ID penjualan
            'produk': retur.produk.id,        # Mengembalikan ID produk
            'qty': retur.qty,
            'alasan': retur.alasan,
        }
        return JsonResponse(data)
    
    form = ReturPenjualanForm(instance=retur)
    return render(request, 'list_supplier.html', {
        'formRetur': form, 
        'retur': retur
    })

def hapus_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

def hapus_gudang(request, pk):
    gudang = get_object_or_404(Gudang, pk=pk)  # Ganti dengan model Diskon
    if request.method == 'POST':
        gudang.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

def hapus_retur(request, pk):
    retur = get_object_or_404(ReturPenjualan, pk=pk)  # Ganti dengan model retur
    if request.method == 'POST':
        retur.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

#stok
def list_stok(request):
    stok_keluar_list = StokKeluar.objects.all()
    stok_masuk_list = StokMasuk.objects.all()
    
    formStokMasuk = StokMasukForm()
    formStokKeluar = StokKeluarForm()
    return render(request, 'katalog/list_stok.html', {
        'stok_keluar': stok_keluar_list,
        'stok_masuk': stok_masuk_list,
        'formStokMasuk' : formStokMasuk,
        'formStokKeluar' : formStokKeluar,
    })
    
def tambah_stok_masuk(request):
    if request.method == 'POST':
        formStokMasuk = StokMasukForm(request.POST)
        if formStokMasuk.is_valid():
            formStokMasuk.save()
            return redirect('list_stok')  # Ganti dengan URL yang sesuai untuk daftar stok
    else:
        formStokMasuk = StokMasukForm()
    return render(request, 'katalog/list_stok.html', {
        'stok_keluar': StokKeluar.objects.all(),
        'stok_masuk': StokMasuk.objects.all(),
        'formStokMasuk': formStokMasuk,
        'formStokKeluar': StokKeluarForm,
    })
    
def tambah_stok_keluar(request):
    if request.method == 'POST':
        formStokKeluar = StokKeluarForm(request.POST)
        if formStokKeluar.is_valid():
            formStokKeluar.save()
            return redirect('list_stok')  # Ganti dengan URL yang sesuai untuk daftar stok
    else:
        formStokKeluar = StokKeluarForm()

    return render(request, 'katalog/list_stok.html', {
        'stok_keluar': StokKeluar.objects.all(),
        'stok_masuk': StokMasuk.objects.all(),
        'formStokMasuk': StokMasukForm(),
        'formStokKeluar': formStokKeluar,
    })
    
def edit_stok_masuk(request, pk):
    stok_masuk = get_object_or_404(StokMasuk, pk=pk)
    if request.method == 'POST':
        form = StokMasukForm(request.POST, instance=stok_masuk)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_stok')  # Ganti dengan URL yang sesuai jika perlu
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'produk': stok_masuk.produk.id,  # Mengembalikan ID produk
            'jumlah': stok_masuk.jumlah,
            'supplier': stok_masuk.supplier.id,  # Mengembalikan ID supplier
            'keterangan': stok_masuk.keterangan,
        }
        return JsonResponse(data)

    form = StokMasukForm(instance=stok_masuk)
    return render(request, 'edit_stok_masuk.html', {
        'formStokMasuk': form,
        'stok_masuk': stok_masuk
    })
    
def edit_stok_keluar(request, pk):
    stok_keluar = get_object_or_404(StokKeluar, pk=pk)
    if request.method == 'POST':
        form = StokKeluarForm(request.POST, instance=stok_keluar)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('list_stok')  # Ganti dengan URL yang sesuai jika perlu
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'produk': stok_keluar.produk.id,  # Mengembalikan ID produk
            'jumlah': stok_keluar.jumlah,
            'alasan': stok_keluar.alasan,
            'keterangan': stok_keluar.keterangan,
        }
        return JsonResponse(data)

    form = StokKeluarForm(instance=stok_keluar)
    return render(request, 'edit_stok_keluar.html', {
        'formStokKeluar': form,
        'stok_keluar': stok_keluar
    })

def hapus_stok_masuk(request, pk):
    stokMasuk = get_object_or_404(StokMasuk, pk=pk)  # Ganti dengan model Diskon
    if request.method == 'POST':
        stokMasuk.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

def hapus_stok_keluar(request, pk):
    stokKeluar = get_object_or_404(StokKeluar, pk=pk)  # Ganti dengan model stokKeluar
    if request.method == 'POST':
        stokKeluar.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

#user
@role_required('admin')
def list_user(request):
    user_list = User.objects.all()
    form = UserRegistrationForm()
    return render(request, 'katalog/list_user.html', {
        'user': user_list,
        'form': form,
    })

def tambah_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User  berhasil ditambahkan')
            return redirect('list_user')  # Ganti dengan URL yang sesuai untuk daftar user
        else:
            # Jika form tidak valid, tidak perlu redirect, cukup render kembali dengan form dan error
            return render(request, 'katalog/list_user.html', {
                'user': User.objects.all(),
                'form': form,
                'judul': 'Tambah User'
            })
    else:
        form = UserRegistrationForm()
    return render(request, 'katalog/list_user.html', {
        'user': User.objects.all(),
        'form': form,
        'judul': 'Tambah User'
    })
    
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'User  berhasil diupdate')
            return redirect('list_user')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'errors': form.errors
                })
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Untuk permintaan AJAX (mengisi modal edit)
            data = {
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
            return JsonResponse(data)
        
        form = UserEditForm(instance=user)
    
    context = {
        'formUser ': form,
        'user_obj': user,
    }
    return render(request, 'katalog/edit_user.html', context)
def hapus_user(request, pk):
    user = get_object_or_404(User, pk=pk)  # Ganti dengan model user
    if request.method == 'POST':
        user.delete()
        return JsonResponse({'success': True})  # Mengembalikan respons JSON
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})

#log_aktivitas
@role_required('admin')
def list_log_aktivitas(request):
    log_aktivitas_list = LogAktivitas.objects.all()
    return render(request, 'katalog/list_log_aktivitas.html', {'log_aktivitas': log_aktivitas_list})

#pembelian
@role_required('admin')
def list_pembelian(request):
    pembelian_list = Pembelian.objects.all()
    detail_pembelian_list = DetailPembelian.objects.all()
    return render(request, 'katalog/list_pembelian.html', {
        'pembelian': pembelian_list,
        'detail_pembelian': detail_pembelian_list
    })
    
def create_pembelian(request):
    if request.method == 'POST':
        form = PembelianForm(request.POST)
        if form.is_valid():
            pembelian = form.save()
            return redirect('list_pembelian')  # Ganti dengan view yang sesuai
    else:
        form = PembelianForm()
    
    return render(request, 'katalog/list_pembelian..html', {'form': form})

def create_detail_pembelian(request):
    if request.method == 'POST':
        form = DetailPembelianForm(request.POST)
        if form.is_valid():
            detail_pembelian = form.save()
            return redirect('list_pembelian')  # Ganti dengan view yang sesuai
    else:
        form = DetailPembelianForm()
    
    return render(request, 'katalog/list_pembelian.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')  # Ganti dengan URL yang sesuai setelah signup
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})