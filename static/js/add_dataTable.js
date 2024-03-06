$(document).ready(function () {
    $('#searchResults').DataTable({
      paging: false,
      searching: false,
      info: false,
      order: [],
      'columnDefs': [ {
                'targets': [0, 7],
                'orderable': false,
          }]
    });
  });