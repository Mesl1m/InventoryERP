  $(document).ready(function () {
    $('#transaksiTable').DataTable({
      layout: {
        topStart: {
            buttons: ['excel', 'pdf']
        }
    },
    language: {
        emptyTable: 'Belum ada data produk'
    },
    lengthChange: false
    });

    // Handle Edit Button Click
    $('.edit-btn').on('click', function () {
        const transaksiId = $(this).data('id');
        $.ajax({
            url: `/transaksi/edit/${transaksiId}/`,  // Update this line to match your URL pattern
            type: 'GET',
            success: function (data) {
                // Populate the modal fields with the transaction data
                $('#edit_pelanggan').val(data.pelanggan.nama); // Assuming pelanggan has a 'nama' attribute
                $('#edit_produk').val(data.produk.nama); // Assuming produk has a 'nama' attribute
                $('#edit_jumlah').val(data.jumlah);
                $('#edit_tanggal').val(data.tanggal);
                $('#edit_catatan').val(data.catatan);
                $('#editTransaksiForm').data('id', transaksiId); // Store id for submit
                $('#editTransaksiModal').modal('show');
                clearEditErrors();
            }
        });
    });

    // Clear validation error messages for edit form
    function clearEditErrors() {
        $('#error_edit_pelanggan').text('');
        $('#error_edit_produk').text('');
        $('#error_edit_jumlah').text('');
        $('#error_edit_tanggal').text('');
        $('#error_edit_catatan').text('');
    }

    // Submit the edit form via AJAX
    $('#editTransaksiForm').on('submit', function (e) {
        e.preventDefault();
        clearEditErrors();
        const transaksiId = $(this).data('id');
        const formData = $(this).serialize();

        $.ajax({
            url: `/transaksi/edit/${transaksiId}/`,  // Update this line to match your URL pattern
            type: 'POST',
            data: formData,
            success: function (response) {
                if (response.success) {
                    $('#editTransaksiModal').modal('hide');
                    location.reload(); // Reload to show updated list
                } else {
                    // Show validation errors returned from backend
                    if (response.errors.pelanggan) $('#error_edit_pelanggan').text(response.errors.pelanggan[0]);
                    if (response.errors.produk) $('#error_edit_produk').text(response.errors.produk[0]);
                    if (response.errors.jumlah) $('#error_edit_jumlah').text(response.errors.jumlah[0]);
                    if (response.errors.tanggal) $('#error_edit_tanggal').text(response.errors.tanggal[0]);
                    if (response.errors.catatan) $('#error_edit_catatan').text(response.errors.catatan[0]);
                }
            }
        });
    });

    $('.delete-btn').on('click', function () {
      const transaksiId = $(this).data('id');
      const deleteUrl = `/transaksi/hapus/${transaksiId}/`;  // Correct URL for deleting a transaction

      Swal.fire({
          title: 'Apakah Anda yakin?',
          text: "Data akan dihapus dan tidak bisa dikembalikan!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          confirmButtonText: 'Hapus',
          cancelButtonText: 'Batal'
      }).then((result) => {
          if (result.isConfirmed) {
              $.ajax({
                  url: deleteUrl,
                  type: 'POST',
                  data: {
                      'csrfmiddlewaretoken': '{{ csrf_token }}',  // Required for POST in Django
                  },
                  success: function (response) {
                      if (response.success) {
                          Swal.fire(
                              'Dihapus!',
                              'Transaksi telah berhasil dihapus.',
                              'success'
                          ).then(() => {
                              location.reload();
                          });
                      } else {
                          Swal.fire('Error', 'Terjadi kesalahan saat menghapus transaksi.', 'error');
                      }
                  },
                  error: function () {
                      Swal.fire('Error', 'Terjadi kesalahan pada server.', 'error');
                  }
              });
          }
      });
    });
  });
