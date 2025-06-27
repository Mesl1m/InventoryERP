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
  });
