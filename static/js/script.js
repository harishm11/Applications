$(document).ready(function() {
    var data,
        tableName = '#example',
        columns,
        str,
        jqxhr = $.ajax({
            url: '/myapp3/opentable',
            "error": function(jqXHR, status, thrownError) {
                $('#loadingSpinner').hide();
                alert("Page not found");
            },
        })
        .done(function() {
                data = JSON.parse(jqxhr.responseText);
                $.each(data.columns, function(k, colobj) {
                        $('#tfooter tr').append('<td><input type="text" placeholder="Search ' + colobj.name + '" /> < /td>')
                        }); 
                        // Iterate each column and print table headers for Datatables 
                        $.each(data.columns, function(k, col0bj) {
                    str = '<th>' + col0bj.name + '</th>'; 
                    $(str).appendTo(tableName + '>thead>tr');
                    });



                data.columns[0].render = function(data, type, row) {
                        return data ;
                }
                        var table = $(tableName).DataTable({
                                    "data": data.data,
                                    "columns": data.columns,
                                    "searchHighlight": true,
                                    "pageLength": 50,
                                    "deferRender": true,
                                    "orderClasses": false,
                                    "dom": 'prftpBi', 
                                    buttons: [ {
                                        "extend": 'excel',
                                        "text": 'Export to Excel',
                                        "className": 'btn btn-secondary'
                                    }

                                ],

                                    initComplete: function() {

                                            $('#searchFilter').on('keyup change clear', function() {
                                                table.search(this.value).draw();
                                            });

                                            $(window).scroll(function() {
                                                if ($(this).scrollTop()) {
                                                    $('#toTop').fadeIn();
                                                } else {
                                                    $('#toTop').fadeOut();
                                                }
                                            });

                                            $("#toTop").click(function() {
                                            $("html, body").animate({ scrollTop: 0}, 1);
                                            });
                                            
                                            this.api().cells().every(function() {
                                                    if (this.data() == 'nan') {
                                                        this.data(" ");
                                                    }
                                                    }); 
                                                    
                                            this.api().on('page.dt', function() {
                                                    $('html, body').animate({
                                                        scrollTop: $(".dataTables_wrapper")
                                                    }, 'fast');
                                                }); 
                                                
                                                $('#loadingSpinner').hide();

                                                var api = this.api();
                                                if (api.rows().count() > 30) {
                                                    api.buttons().disable();
                                                }
                                                    $('#clearsearchFilter').on('click', function() {
                                                        $('input').val('');
                                                        $('#searchFilter').val();
                                                        api.search().draw();
                                                        api.columns().search().draw();
                                                    });
                                                        
                                                                    this.api().columns().every(function() {
                                                                        var that =this;
                                                                        $('input', this.footer()).on('keyup change clear', function() {
                                                                            if (that.search() != this.value) {
                                                                                that.search(this.value).draw();

                                                                            }
                                                                        });
                                                                    });
                                                                }
                                                            });

                                                    });

                                                });
                                   