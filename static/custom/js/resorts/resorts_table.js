document.addEventListener('DOMContentLoaded', function () {

    let oLanguages = {
        "sEmptyTable": "데이터가 없습니다",
        "sInfo": "_START_ - _END_ / _TOTAL_",
        "sInfoEmpty": "0 - 0 / 0",
        "sInfoFiltered": "(총 _MAX_ 개)",
        "sInfoPostFix": "",
        "sInfoThousands": ",",
        "sLengthMenu": "페이지당 줄수 _MENU_",
        "sLoadingRecords": "읽는중...",
        "sProcessing": "처리중...",
        "sSearch": "검색:",
        "sZeroRecords": "검색 결과가 없습니다",
        "oPaginate": {
            "sFirst": "처음",
            "sLast": "마지막",
            "sNext": "다음",
            "sPrevious": "이전"
        },
        "oAria": {
            "sSortAscending": ": 오름차순 정렬",
            "sSortDescending": ": 내림차순 정렬"
        }
    };

    let dt_table;
    dt_table = $('#resorts-table').dataTable({
        "oLanguage": oLanguages,
        "bFilter": true,
        "searching": false,
        "iDisplayLength": 25,
        oPaginate: true,
        "bAutoWidth": true,
        columns: [
            {
                data: '0',
                visible: false,
                className: "center"
            },
            {
                data: '1',
                className: "center"
            },
            {
                data: '2',
                className: "center"
            }
        ],
        "bProcessing": true,
        "bServerSide": true,
        "bStateSave": true,
        "stripeClasses": [],
        "ajax": {
            "url": RESORT_LIST_JSON_URL,
        },
        "columnDefs": [
            {
                targets: [2],
                render: function (data, type, row) {
                    if (type === "sort" || type === "type") {
                        return data;
                    }//Dec. 23, 2019, 10:16 p.m.
                    return moment(data).format("DD.MM.YYYY HH:mm");
                }
            },
        ],

        "rowCallback": function (row, data) {
            row.addEventListener('click', function () {
                location.href = G_RESORT_PAGE_URL.replace('99999999999999', data[0]);
            })
        }

    });
});
