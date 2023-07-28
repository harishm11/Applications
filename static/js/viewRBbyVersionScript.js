$(document).ready(function () {
  $('#example').DataTable({
    paging: false,
    searching: false,
    info: false,
    order: [[9, 'desc']],
    'columnDefs': [ {
              'targets': [0],
              'orderable': false,
        }]
  });
});
$('input[type=checkbox]').on('change', function (e) {
    if ($('input[type=checkbox]:checked').length > 2)
    {
      $(this).prop('checked', false);
      alert("Max allowed selections is 2");
      $("#export_template_button").prop("disabled", true);
    }
    else if ($('input[type=checkbox]:checked').length == 2)
    {
      $("#export_template_button").prop("disabled", true);
      const values = Array.from(
        document.querySelectorAll(
          "input[type=checkbox]:checked"
          ),
          e => e.value
        );
      rb1 = values[0].split("_");
      rb2 = values[1].split("_")
      if((rb1[rb1.length-1] != rb2[rb2.length-1]) || (rb1[rb1.length-2] != rb2[rb2.length-2]))
      {
        $(this).prop('checked', false);
        alert("Please Select Same State and Product Code");
      }
      else
      {
      $("#compare_button").prop("disabled", false);
      }
    }
    else if ($('input[type=checkbox]:checked').length == 1){
        $("#export_template_button").prop("disabled", false);
        $("#compare_button").prop("disabled", true);
    }
    else
    {
      $("#compare_button").prop("disabled", true);
      $("#export_template_button").prop("disabled", true);
    }
});
