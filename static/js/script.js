$(document).ready(function () {
  var data,
    tableName = "#example",
    columns,
    str,
    jqxhr = $.ajax({
      url: "/ratemanager/openexhibit",
      error: function (jqXHR, status, thrownError) {
        $("#loadingSpinner").hide();
        alert("Page not found");
      },
    }).done(function () {
      data = JSON.parse(jqxhr.responseText);

      $.each(data.columns, function (k, col0bj) {
        str = "<th>" + col0bj.name + "</th>";
        $(str).appendTo(tableName + ">thead>tr");
      });

      data.columns[0].render = function (data, type, row) {
        return data;
      };
      var table = $(tableName).DataTable({
        data: data.data,
        columns: data.columns,
        searchHighlight: true,
        pageLength: 15,
        deferRender: true,
        orderClasses: false,
        dom: "prftiB",
        buttons: [
          {
            extend: "excel",
            text: "Export to Excel",
          },
        ],
        initComplete: function () {
          $("#searchFilter").on("keyup change clear", function () {
            table.search(this.value).draw();
          });
          this.api()
            .columns()
            .every(function () {
              var column = this;
              var select = $('<select><option value=""></option></select>')
                .appendTo($(column.header()))
                .on("change", function () {
                  var val = $.fn.dataTable.util.escapeRegex($(this).val());
                  column.search(val ? "^" + val + "$" : "", true, false).draw();
                });
              column
                .data()
                .unique()
                .sort()
                .each(function (d, j) {
                  select.append('<option value="' + d + '">' + d + "</option>");
                });
            });

          $(window).scroll(function () {
            if ($(this).scrollTop()) {
              $("#toTop").fadeIn();
            } else {
              $("#toTop").fadeOut();
            }
          });

          $("#toTop").click(function () {
            $("html, body").animate({ scrollTop: 0 }, 1);
          });

          this.api()
            .cells()
            .every(function () {
              if (this.data() == "nan") {
                this.data(" ");
              }
            });

          this.api().on("page.dt", function () {
            $("html, body").animate(
              {
                scrollTop: $(".dataTables_wrapper"),
              },
              "fast"
            );
          });

          $("#loadingSpinner").hide();

          var api = this.api();
        },
      });
    });
});
