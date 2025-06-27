    $(document).ready(function () {
        $('#produkTableSupplier').DataTable({
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

        $('#produkTableGudang').DataTable({
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

        $('#produkTableRetur').DataTable({
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
