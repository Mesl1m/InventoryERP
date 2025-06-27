from django.db import models

from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

# Create your models here.
class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    aktif = models.BooleanField(default=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.PositiveIntegerField()
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    deskripsi = models.TextField()

    def clean(self):
        super().clean()
        if self.stok < 0:
            raise ValidationError('Stok tidak boleh negatif.')
        if self.harga < 0:
            raise ValidationError('Harga tidak boleh negatif.')
        return self.nama 


class Pelanggan(models.Model):
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    no_hp = models.CharField(max_length=15)
    alamat = models.TextField()
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    tanggal_bergabung = models.DateField(auto_now_add=True)  # Tambahkan field ini
    def __str__(self):
        return self.nama

class Penjualan(models.Model):
    tanggal = models.DateTimeField(auto_now_add=True)
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    metode_bayar = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'Penjualan {self.id} - {self.pelanggan.nama}'


class DetailPenjualan(models.Model):
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    catatan = models.TextField(blank=True)

    def __str__(self):
        return f'{self.produk.nama} x {self.qty}'


class Transaksi(models.Model):
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    tanggal = models.DateField(auto_now_add=True)
    catatan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.pelanggan.nama} - {self.produk.nama} ({self.tanggal})"

class KategoriSupplier(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.nama

class Supplier(models.Model):
    nama = models.CharField(max_length=100)
    kategori = models.ForeignKey(KategoriSupplier, on_delete=models.SET_NULL, null=True, blank=True)
    kontak = models.CharField(max_length=100)
    alamat = models.TextField()
    email = models.EmailField()
    aktif = models.BooleanField(default=True)

class StokMasuk(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    tanggal = models.DateField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    keterangan = models.TextField()

class StokKeluar(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    tanggal = models.DateField(auto_now_add=True)
    alasan = models.CharField(max_length=100)
    keterangan = models.TextField()

class ReturPenjualan(models.Model):
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    tanggal = models.DateField(auto_now_add=True)
    alasan = models.TextField()

# class User(models.Model):
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    # groups = models.ManyToManyField('accounts.Groups', verbose_name=_("groups"), blank=True, related_name="user_set", related_query_name="user")
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('staff', 'Staff')])
    # aktif = models.BooleanField(default=True)

    objects = CustomUserManager()

class Gudang(models.Model):
    nama = models.CharField(max_length=100)
    lokasi = models.TextField()
    penanggung_jawab = models.CharField(max_length=100)
    kapasitas = models.PositiveIntegerField()
    aktif = models.BooleanField(default=True)

class Diskon(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    persen = models.FloatField()
    mulai = models.DateField()
    sampai = models.DateField()
    aktif = models.BooleanField(default=True)
    def __str__(self):
        return f'Diskon {self.persen}% untuk {self.produk}' 

class LogAktivitas(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aksi = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)
    objek_terkait = models.CharField(max_length=100)

class Pembelian(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    tanggal = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20)
    keterangan = models.TextField()
 
class DetailPembelian(models.Model):
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    harga_beli = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

class Satuan(models.Model):
    nama = models.CharField(max_length=50)
    kode = models.CharField(max_length=10)
    deskripsi = models.TextField()
    aktif = models.BooleanField(default=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)

class Pengiriman(models.Model):
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE)
    tanggal_pengiriman = models.DateField()
    kurir = models.CharField(max_length=100)
    nomor_resi = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('diproses', 'Diproses'),
        ('dikirim', 'Dikirim'),
        ('diterima', 'Diterima'),
        ('dibatalkan', 'Dibatalkan')
    ])

    def __str__(self):
        return f'Pengiriman {self.penjualan.id} - {self.status}'

class Pembayaran(models.Model):
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE)
    tanggal_pembayaran = models.DateField(auto_now_add=True)
    jumlah_dibayar = models.DecimalField(max_digits=12, decimal_places=2)
    metode = models.CharField(max_length=50, choices=[
        ('transfer', 'Transfer Bank'),
        ('cash', 'Cash'),
        ('ewallet', 'E-Wallet'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('lunas', 'Lunas'),
        ('gagal', 'Gagal')
    ])

    def __str__(self):
        return f'Pembayaran {self.penjualan.id} - {self.status}'

class PenyesuaianStok(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah_perubahan = models.IntegerField(help_text="Isi positif untuk penambahan, negatif untuk pengurangan")
    alasan = models.CharField(max_length=100)
    tanggal = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Penyesuaian {self.produk.nama} - {self.jumlah_perubahan}'
