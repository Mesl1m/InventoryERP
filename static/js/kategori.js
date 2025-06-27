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

    $('#produkTableSatuan').DataTable({
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

    $('#produkTableDiskon').DataTable({
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
