
  $(document).ready(function () {
    $('#pelangganTable').DataTable({
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

    // Open edit modal and load data via AJAX
    $('.edit-btn').on('click', function(){
      const pelangganId = $(this).data('id');

      $.ajax({
        url: `/pelanggan/edit/${pelangganId}/`,  // Update if your URL pattern differs
        type: 'GET',
        success: function(data){
          $('#edit_nama').val(data.nama);
          $('#edit_email').val(data.email);
          $('#edit_no_hp').val(data.no_hp);
          $('#edit_alamat').val(data.alamat);
          $('#edit_jenis_kelamin').val(data.jenis_kelamin);
          $('#editPelangganForm').data('id', pelangganId); // store id for submit
          $('#editPelangganModal').modal('show');
          clearErrors();
        }
      });
    });

    // Clear validation error messages
    function clearErrors(){
      $('#error_nama').text('');
      $('#error_email').text('');
      $('#error_no_hp').text('');
      $('#error_alamat').text('');
      $('#error_jenis_kelamin').text('');
    }

    // Submit the edit form via AJAX
    $('#editPelangganForm').on('submit', function(e){
      e.preventDefault();
      clearErrors();
      const pelangganId = $(this).data('id');
      const formData = $(this).serialize();

      $.ajax({
        url: `/pelanggan/edit/${pelangganId}/`,
        type: 'POST',
        data: formData,
        success: function(response){
          if(response.success){
            $('#editPelangganModal').modal('hide');
            location.reload(); // Reload to show updated list
          }
          else{
            // Show validation errors returned from backend
            if(response.errors.nama) $('#error_nama').text(response.errors.nama[0]);
            if(response.errors.email) $('#error_email').text(response.errors.email[0]);
            if(response.errors.no_hp) $('#error_no_hp').text(response.errors.no_hp[0]);
            if(response.errors.alamat) $('#error_alamat').text(response.errors.alamat[0]);
            if(response.errors.jenis_kelamin) $('#error_jenis_kelamin').text(response.errors.jenis_kelamin[0]);
          }
        }
      });
    });


    $('.delete-btn').on('click', function () {
      const customerId = $(this).data('id');
      const deleteUrl = `/pelanggan/hapus/${customerId}/`; // Adjust this URL to match your delete view

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
              // Send AJAX request to delete the customer
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
                              'Pelanggan telah dihapus.',
                              'success'
                          ).then(() => {
                              location.reload(); // Reload the page to see changes
                          });
                      }
                  },
                  error: function () {
                      Swal.fire(
                          'Gagal!',
                          'Terjadi kesalahan saat menghapus pelanggan.',
                          'error'
                      );
                  }
              });
            }
        });
    });
  });
