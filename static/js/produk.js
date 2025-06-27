  $(document).ready(function () {
    $('#produkTable').DataTable({
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
      const productId = $(this).data('id');
      $.ajax({
        url: `/edit/${productId}/`,  // Update this line to match your URL pattern
        type: 'GET',
        success: function (data) {
            // Populate the modal fields with the product data
            $('#edit_nama').val(data.nama);
            $('#edit_harga').val(data.harga);
            $('#edit_stok').val(data.stok);
            $('#edit_kategori').val(data.kategori); // Assuming you have a way to get the category ID
            $('#edit_deskripsi').val(data.deskripsi);
            $('#editProdukModal').modal('show');
          }
      });
    });


    // Handle Edit Form Submission
    $('#editForm').on('submit', function (e) {
      e.preventDefault();
      const formData = $(this).serialize();
      const productId = $('.edit-btn').data('id'); // Get the product ID again
      $.ajax({
        url: `/produk/${productId}/edit/`,  // Adjust the URL to your edit view
        type: 'POST',
        data: formData,
        success: function (response) {
          if (response.success) {
            $('#editProdukModal').modal('hide');
            location.reload(); // Reload the page to see changes
          } else {
            // Handle validation errors
            $('#edit_nama_error').text(response.errors.nama || '');
            $('#edit_harga_error').text(response.errors.harga || '');
            $('#edit_stok_error').text(response.errors.stok || '');
            $('#edit_kategori_error').text(response.errors.kategori || '');
            $('#edit_deskripsi_error').text(response.errors.deskripsi || '');
          }
        }
      });
    });


    // Handle Delete Button Click
    $('.delete-btn').on('click', function () {
      const productId = $(this).data('id');
      const deleteUrl = `/hapus/${productId}/`; // Adjust this URL to match your delete view

      Swal.fire({
        title: 'Apakah Anda yakin?',
        text: "Anda tidak dapat mengembalikan ini!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Hapus!',
        cancelButtonText: 'Batal'
      }).then((result) => {
        if (result.isConfirmed) {
          // Send AJAX request to delete the product
          $.ajax({
            url: deleteUrl,
            type: 'POST',
            data: {
              'csrfmiddlewaretoken': '{{ csrf_token }}'  // Include CSRF token
            },
            success: function (response) {
              if (response.success) {
                Swal.fire(
                  'Dihapus!',
                  'Produk telah dihapus.',
                  'success'
                ).then(() => {
                  location.reload(); // Reload the page to see changes
                });
              }
            },
            error: function () {
              Swal.fire(
                'Gagal!',
                'Terjadi kesalahan saat menghapus produk.',
                'error'
              );
            }
          });
        }
      });
    });
  });
