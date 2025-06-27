$(document).ready(function () {
    $('#produkTablePembelian').DataTable({
    layout: {
        topStart: {
        buttons: ['excel', 'pdf']
    },
},
    language: {
        emptyTable: 'Belum ada data pembelian'
    },
    lengthChange: false
});

$('#produkTableDetailPembelian').DataTable({
    layout: {
        topStart: {
            buttons: ['excel', 'pdf']
        }
    },
    language: {
        emptyTable: 'Belum ada data pembelian'
    },
    lengthChange: false
    });
});
