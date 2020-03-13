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
            "searching": false,
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
                },
                {
                    data: '4',
                    className: "center"
                },
                {
                    data: '5',
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
                    d.section_type = l_section_type_id;
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
                    targets: 1,
                    render: function (data, type, row) {
                        return `<img src="${MEDIA_ULR}${data}" style="max-height: 70px;min-height: 70px;">`;
                    }
                },
                {
                    targets: 4,
                    render: function (data, type, row) {
                        if (type === "sort" || type === "type") {
                            return data;
                        }//Dec. 23, 2019, 10:16 p.m.
                        return moment(data).format("MMM. DD, YYYY, hh:mm a");
                    }
                },
            ]

        });

        ul_li_listener();


        function ul_li_listener() {
            let regions_block = document.querySelector('#section-filter');
            let sections = regions_block.querySelectorAll('a');
            [].forEach.call(sections, function (el) {
                el.addEventListener('click', function () {
                    [].forEach.call(sections, function (element) {
                        element.children[0].classList.remove('cat_menu_btn_a');
                        element.children[0].classList.add('cat_menu_btn');
                    });
                    el.children[0].classList.remove('cat_menu_btn');
                    el.children[0].classList.add('cat_menu_btn_a');
                    l_section_id = el.dataset.sectionId;
                    $('#forum-table').DataTable().ajax.reload();
                })
            });
        }
    }
);
