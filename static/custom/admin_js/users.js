document.addEventListener('DOMContentLoaded', function () {

    let dt_table;
    let langs = {
        "processing": "Подождите...",
        "search": "Поиск:",
        "lengthMenu": "Показать _MENU_ записей",
        "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
        "infoEmpty": "Записи с 0 до 0 из 0 записей",
        "infoFiltered": "(отфильтровано из _MAX_ записей)",
        "infoPostFix": "",
        "loadingRecords": "Загрузка записей...",
        "zeroRecords": "Записи отсутствуют.",
        "emptyTable": "В таблице отсутствуют данные",
        "paginate": {
            "first": "Первая",
            "previous": "Предыдущая",
            "next": "Следующая",
            "last": "Последняя"
        },
        "aria": {
            "sortAscending": ": активировать для сортировки столбца по возрастанию",
            "sortDescending": ": активировать для сортировки столбца по убыванию"
        },
        "select": {
            "rows": {
                "_": "Выбрано записей: %d",
                "0": "Кликните по записи для выбора",
                "1": "Выбрана одна запись"
            }
        }
    };
    dt_table = $('#users-table').dataTable({
        "bFilter": true,
        "oLanguage": langs,
        "iDisplayLength": 25,
        oPaginate: true,
        "bAutoWidth": true,
        "bProcessing": true,
        "bServerSide": true,
        "bStateSave": true,
        "searching": false,
        "stripeClasses": [],
        "ajax": {
            "url": USERS_LIST_JSON_URL,
            "data": function (d) {
                d.is_fake = document.getElementById('is_fake').checked ? 'True' : 'False';
                d.is_staff = document.getElementById('is_staff').checked ? 'True' : 'False';
                d.is_want_staff = document.getElementById('is_want_staff').checked ? 'True' : 'False';
                d.username = document.getElementById('username').value;
                d.email = document.getElementById('email').value;
            }
        },

        "rowCallback": function (row, data) {
            try {
                row.querySelector('.change_staff_status').addEventListener('click', function () {
                    ChangeStaffStatus(this.dataset.userId, this.dataset.staffStatus, dt_table)
                });
                row.querySelector('.check_user_offers').addEventListener('click', function () {
                    location.href = USER_OFFERS_URL.replace('999999', data[0]);
                })
            } catch (e) {
            }
        },
        "columnDefs": [
            {
                targets: [4, 5, 6],
                render: function (data, type, row) {
                    return data === 'True' ? 'Да' : 'Нет';
                    // return `[${row[1]} - ${row[2]}] ${row[3]} - ${row[4]}`;
                }
            },
            {
                targets: [7],
                render: function (data, type, row) {
                    let html = '';
                    if (row[4] === 'False') {
                        html += `<button class="btn btn-primary change_staff_status col-sm-12" data-user-id="${row[7]}" data-staff-status="true">
                                    Сделать диллером
                                 </button>`
                    } else {
                        html += `<button class="btn btn-primary change_staff_status col-sm-12" data-user-id="${row[7]}" data-staff-status="false">
                                    Сделать пользователем
                                 </button>`
                        html += `<button class="btn btn-primary check_user_offers col-sm-12" data-user-id="${row[7]}">
                                    Посмотреть объявления
                                 </button>`
                    }
                    return html
                }
            }
        ]

    });

    document.getElementById('btn-search').addEventListener('click', function () {
        dt_table.DataTable().ajax.reload();
    });

    function ChangeStaffStatus(user_id, staff_status, dt_table) {
        let modal = new tingle.modal({
            footer: true,
            stickyFooter: false,
            closeMethods: ['overlay', 'button', 'escape'],
            closeLabel: "Close",
            cssClass: ["modal-confirm"]
        });
        modal.setContent('Вы уверены?');
        modal.addFooterBtn('Да', 'tingle-btn tingle-btn--primary', function () {
            $.ajax({
                "type": 'POST',
                "url": USER_STAFF_STATUS_URL,
                "data": {
                    "user_id": user_id,
                    "is_staff": staff_status,
                    "csrfmiddlewaretoken": l_csrf_token,
                },
                "success": function (response) {
                    console.log("success")
                },
            });
            dt_table.DataTable().ajax.reload();
            modal.close();
        });
        modal.addFooterBtn('Нет', 'tingle-btn tingle-btn--primary', function () {
            modal.close();
        });
        modal.open()
    }
});

