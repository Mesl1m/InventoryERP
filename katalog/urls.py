from django.urls import path
from . import views

urlpatterns = [
    #dashboard
    # path('', views.dashboard, name='dashboard'),

    #produk
    path('produk/', views.list_produk, name='list_produk'),
    path('tambah/', views.tambah_produk, name='tambah_produk'),
    path('edit/<int:pk>/', views.edit_produk, name='edit_produk'),
    path('hapus/<int:pk>/', views.hapus_produk, name='hapus_produk'),
    # path('transaksi/', views.list_transaksi, name='list_transaksi'),


    #pelanggan
    path('pelanggan/', views.list_pelanggan, name='list_pelanggan'),
    path('pelanggan/tambah/', views.tambah_pelanggan, name='tambah_pelanggan'),
    path('pelanggan/edit/<int:pk>/', views.edit_pelanggan, name='edit_pelanggan'),
    path('pelanggan/hapus/<int:pk>/', views.hapus_pelanggan, name='hapus_pelanggan'),


    #transaksi
    path('transaksi/', views.list_transaksi, name='list_transaksi'),
    path('transaksi/tambah/', views.tambah_transaksi, name='tambah_transaksi'),
    path('transaksi/edit/<int:pk>/', views.edit_transaksi, name='edit_transaksi'),
    path('transaksi/hapus/<int:pk>/', views.hapus_transaksi, name='hapus_transaksi'),
    
    #kategori
    path('kategori/', views.list_kategori, name='list_kategori'),  # Gabungkan semua di sini
    path('kategori/tambah-kategori/', views.tambah_kategori, name='tambah_kategori'),
    path('kategori/tambah-satuan/', views.tambah_satuan, name='tambah_satuan'),
    path('kategori/tambah-diskon/', views.tambah_diskon, name='tambah_diskon'),
    path('kategori/edit-kategori/<int:pk>/', views.edit_kategori, name='edit_kategori'),
    path('kategori/edit-satuan/<int:pk>/', views.edit_satuan, name='edit_satuan'),
    path('kategori/edit-diskon/<int:pk>/', views.edit_diskon, name='edit_diskon'),
    path('kategori/hapus/<int:pk>/', views.hapus_kategori, name='hapus_kategori'),
    path('kategori/hapus-diskon/<int:pk>/', views.hapus_diskon, name='hapus_diskon'),
    path('kategori/hapus-satuan/<int:pk>/', views.hapus_satuan, name='hapus_satuan'),

    #supplier
    path('supplier/', views.list_supplier, name='list_supplier'),
    path('supplier/tambah-supplier/', views.tambah_supplier, name='tambah_supplier'),
    path('supplier/tambah-gudang/', views.tambah_gudang, name='tambah_gudang'),
    path('supplier/tambah-retur/', views.tambah_retur, name='tambah_retur'),
    path('supplier/edit-supplier/<int:pk>/', views.edit_supplier, name='edit_supplier'),
    path('supplier/edit-gudang/<int:pk>/', views.edit_gudang, name='edit_gudang'),
    path('supplier/edit-retur/<int:pk>/', views.edit_retur, name='edit_retur'),
    path('supplier/hapus/<int:pk>/', views.hapus_supplier, name='hapus_supplier'),
    path('supplier/hapus-gudang/<int:pk>/', views.hapus_gudang, name='hapus_gudang'),
    path('supplier/hapus-retur/<int:pk>/', views.hapus_retur, name='hapus_retur'),
    
      
    path('stok/', views.list_stok, name='list_stok'),
    path('stok/tambah-stok_masuk/', views.tambah_stok_masuk, name='tambah_stok_masuk'),
    path('stok/tambah-stok_keluar/', views.tambah_stok_keluar, name='tambah_stok_keluar'),
    path('stok/edit-stok-masuk/<int:pk>/', views.edit_stok_masuk, name='edit_stok_masuk'),
    path('stok/edit-stok-keluar/<int:pk>/', views.edit_stok_keluar, name='edit_stok_keluar'),
    path('stok/hapus/<int:pk>/', views.hapus_stok_masuk, name='hapus_stok_masuk'),
    path('stok/hapus-stok-keluar/<int:pk>/', views.hapus_stok_keluar, name='hapus_stok_keluar'),
    
    path('user/', views.list_user, name='list_user'),
    path('user/tambah/', views.tambah_user, name='tambah_user'),
    path('user/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('user/hapus/<int:pk>/', views.hapus_user, name='hapus_user'),


    path('log-aktivitas/', views.list_log_aktivitas, name='list_log_aktivitas'),
    
    path('pembelian/', views.list_pembelian, name='list_pembelian'),
    path('pembelian/tambah/', views.create_pembelian, name='tambah_pembelian'),
    path('detail-pembelian/tambah/', views.create_detail_pembelian, name='tambah_detail_pembelian'),

    path('signup/', views.signup_view, name='signup'),
    

]
