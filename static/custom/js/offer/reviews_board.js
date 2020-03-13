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
    dt_table = $('#reviews-table').dataTable({
        "oLanguage": oLanguages,
        "bFilter": true,
        "iDisplayLength": 25,
        "searching": false,
        oPaginate: true,
        "bAutoWidth": true,
        columns: [
            {
                data: '0',
                className: "center"
            },
            {
                data: '1',
                visible: false,
                className: "center"
            },
            {
                data: '2',
                visible: false,
                className: "center"
            },
            {
                data: '3',
                visible: false,
                className: "center"
            },
            {
                data: '4',
                className: "center"
            },
            {
                data: '5',
                className: "center"
            },
            {
                data: '6',
                className: "center"
            },
            {
                data: '7',
                className: "center"
            },
        ],
        "bProcessing": true,
        "bServerSide": true,
        "bStateSave": true,
        "stripeClasses": [],
        "ajax": {
            "url": USERS_LIST_JSON_URL,
            "data": function (d) {
                d.town = l_town_id;
                d.category = l_category_id;
                d.region = l_region_id;
            }
        },

        "rowCallback": function (row, data) {
            row.addEventListener('click', function () {
                location.href = G_REVIEW_PAGE_URL.replace('99999999999999', data[0]);
            })
        },
        "columnDefs": [
            {
                targets: 4,
                render: function (data, type, row) {
                    return `[${row[1]} - ${row[2]}] ${row[3]} - ${row[4]}`;
                }
            },
            {
                targets: 6,
                render: function (data, type, row) {
                    if (type === "sort" || type === "type") {
                        return data;
                    }//Dec. 23, 2019, 10:16 p.m.
                    return moment(data).format("MMM. DD, YYYY");
                }
            },
        ]

    });
    ul_li_listener()
});

function ul_li_listener() {
    let regions_block = document.querySelector('#region-filter');
    let regions = regions_block.querySelectorAll('a');
    [].forEach.call(regions, function (el) {
        el.addEventListener('click', function () {
            [].forEach.call(regions, function (element) {
                element.children[0].classList.remove('cat_menu_btn_a');
                element.children[0].classList.add('cat_menu_btn');
            });
            el.children[0].classList.remove('cat_menu_btn');
            el.children[0].classList.add('cat_menu_btn_a');
            l_region_id = el.dataset.regionId;
            $('#reviews-table').DataTable().ajax.reload();
        })
    });
    let category_block = document.querySelector('#category-filter');
    let category = category_block.querySelectorAll('a');
    [].forEach.call(category, function (el) {
        el.addEventListener('click', function () {
            [].forEach.call(category, function (element) {
                element.children[0].classList.remove('cat_menu_btn2_a');
                element.children[0].classList.add('cat_menu_btn2');
            });
            el.children[0].classList.remove('cat_menu_btn2');
            el.children[0].classList.add('cat_menu_btn2_a');
            l_category_id = el.dataset.categoryId;
            $('#reviews-table').DataTable().ajax.reload();
        })
    })
}
