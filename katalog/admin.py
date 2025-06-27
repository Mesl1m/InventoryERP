from django.contrib import admin
from .models import (
    Kategori, Produk, Pelanggan, Penjualan, DetailPenjualan, Transaksi,
    Supplier, StokKeluar, StokMasuk, ReturPenjualan, User, Gudang, Diskon,
    LogAktivitas, Pembelian, DetailPembelian, Satuan, Pengiriman, Pembayaran, KategoriSupplier, PenyesuaianStok
)

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'deskripsi', 'aktif', 'dibuat_pada']
    list_editable = ['nama', 'deskripsi', 'aktif']

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'harga', 'stok', 'kategori', 'deskripsi']
    list_editable = ['nama', 'harga', 'stok', 'kategori', 'deskripsi']

@admin.register(Pelanggan)
class PelangganAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'email', 'no_hp', 'alamat', 'jenis_kelamin', 'tanggal_bergabung']
    list_editable = ['nama', 'email', 'no_hp', 'alamat', 'jenis_kelamin']

@admin.register(Penjualan)
class PenjualanAdmin(admin.ModelAdmin):
    list_display = ['id', 'tanggal', 'pelanggan', 'total', 'metode_bayar', 'status']
    list_editable = ['pelanggan', 'total', 'metode_bayar', 'status']

@admin.register(DetailPenjualan)
class DetailPenjualanAdmin(admin.ModelAdmin):
    list_display = ['id', 'penjualan', 'produk', 'qty', 'subtotal', 'catatan']
    list_editable = ['penjualan', 'produk', 'qty', 'subtotal', 'catatan']

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ['id', 'pelanggan', 'produk', 'jumlah', 'tanggal', 'catatan']
    list_editable = ['pelanggan', 'produk', 'jumlah', 'catatan']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'kontak', 'email', 'aktif']
    list_editable = ['nama', 'kontak', 'email', 'aktif']

@admin.register(StokMasuk)
class StokMasukAdmin(admin.ModelAdmin):
    list_display = ['id', 'produk', 'jumlah', 'tanggal', 'supplier', 'keterangan']
    list_editable = ['produk', 'jumlah', 'supplier', 'keterangan']
    
@admin.register(StokKeluar)
class StokKeluarAdmin(admin.ModelAdmin):
    list_display = ['id', 'produk', 'jumlah', 'tanggal', 'alasan', 'keterangan']
    list_editable = ['produk', 'jumlah', 'alasan', 'keterangan']

@admin.register(ReturPenjualan)
class ReturPenjualanAdmin(admin.ModelAdmin):
    list_display = ['id', 'penjualan', 'produk', 'qty', 'tanggal', 'alasan']
    list_editable = ['penjualan', 'produk', 'qty', 'alasan']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'is_active']
    list_editable = ['username', 'email', 'role', 'is_active']

@admin.register(Gudang)
class GudangAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'lokasi', 'penanggung_jawab', 'kapasitas', 'aktif']
    list_editable = ['nama', 'lokasi', 'penanggung_jawab', 'kapasitas', 'aktif']

@admin.register(Diskon)
class DiskonAdmin(admin.ModelAdmin):
    list_display = ['id', 'produk', 'persen', 'mulai', 'sampai', 'aktif']
    list_editable = ['produk', 'persen', 'mulai', 'sampai', 'aktif']

@admin.register(LogAktivitas)
class LogAktivitasAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'aksi', 'waktu', 'objek_terkait']
    list_filter = ['user', 'waktu']
    search_fields = ['aksi', 'objek_terkait']

@admin.register(Pembelian)
class PembelianAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'tanggal', 'total', 'status']
    list_editable = ['supplier', 'total', 'status']

@admin.register(DetailPembelian)
class DetailPembelianAdmin(admin.ModelAdmin):
    list_display = ['id', 'pembelian', 'produk', 'qty', 'harga_beli', 'subtotal']
    list_editable = ['pembelian', 'produk', 'qty', 'harga_beli', 'subtotal']

@admin.register(Satuan)
class SatuanAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'kode', 'deskripsi', 'aktif', 'dibuat_pada']
    list_editable = ['nama', 'kode', 'deskripsi', 'aktif']

@admin.register(Pengiriman)
class PengirimanAdmin(admin.ModelAdmin):
    list_display = ['id', 'penjualan', 'tanggal_pengiriman', 'kurir', 'nomor_resi', 'status']
    list_editable = ['penjualan', 'tanggal_pengiriman', 'kurir', 'nomor_resi', 'status']
    list_filter = ['status', 'kurir']
    search_fields = ['nomor_resi']

@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = ['id', 'penjualan', 'tanggal_pembayaran', 'jumlah_dibayar', 'metode', 'status']
    list_editable = ['penjualan', 'jumlah_dibayar', 'metode', 'status']
    list_filter = ['metode', 'status']

@admin.register(KategoriSupplier)
class KategoriSupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'deskripsi', 'aktif']
    list_editable = ['nama', 'deskripsi', 'aktif']
    search_fields = ['nama']

@admin.register(PenyesuaianStok)
class PenyesuaianStokAdmin(admin.ModelAdmin):
    list_display = ['id', 'produk', 'jumlah_perubahan', 'alasan', 'tanggal', 'user']
    list_editable = ['produk', 'jumlah_perubahan', 'alasan', 'user']
    list_filter = ['tanggal', 'user']
    search_fields = ['alasan']