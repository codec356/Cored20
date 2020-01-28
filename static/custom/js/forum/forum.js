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

    let dt_table = $('#forum-table').dataTable({
        "oLanguage": oLanguages,
        "bFilter": true,
        "iDisplayLength": 25,
        oPaginate: true,
        "bAutoWidth": true,
        columns: [
            {
                data: '0',
                className: "center"
            },
            {
                data: '1',
                className: "center"
            },
            {
                data: '2',
                className: "center"
            },
            {
                data: '3',
                className: "center"
            }
        ],
        "bProcessing": true,
        "bServerSide": true,
        "bStateSave": true,
        "stripeClasses": [],
        "ajax": {
            "url": TOPIC_LIST_JSON_URL,
            "data": function (d) {
                d.section = l_section_id;
            }
        },

        "rowCallback": function (row, data) {
            row.addEventListener('click', function () {
                location.href = G_TOPIC_PAGE_URL.replace('99999999999999', data[0]);
            })
        },
        "columnDefs": [
            {
                targets: 3,
                render: function (data, type, row) {
                    if (type === "sort" || type === "type") {
                        return data;
                    }//Dec. 23, 2019, 10:16 p.m.
                    return moment(data).format("MMM. DD, YYYY, hh:mm a");
                }
            },
        ]

    });
});
