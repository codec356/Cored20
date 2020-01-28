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
    dt_table = $('#offers-table').dataTable({
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
            "url": OFFERS_LIST_JSON_URL,
            "data": function (d) {
                d.username = document.getElementById('username').value;
            }
        },

        "rowCallback": function (row, data) {
            try {
                row.querySelectorAll('.action_offer').forEach(button => button.addEventListener('click', function () {
                    ActionOffer(this.dataset.offerId, this.dataset.action, dt_table)
                }));
            } catch (e) {
            }
        },
        "columnDefs": [
            {
                targets: [3],
                render: function (data, type, row) {
                    return `${data === 'True' ? 'Да' : 'Нет'}`
                }
            },
            {
                targets: [4, 5],
                render: function (data, type, row) {
                    if (type === "sort" || type === "type") {
                        return data;
                    }//Dec. 23, 2019, 10:16 p.m.
                    return moment(data).format("DD.MM.YYYY hh:mm");
                }
            },
            {
                targets: [6],
                render: function (data, type, row) {
                    let html = '';
                    if (row[3] === 'False') {
                        html += `
                            <button class="btn btn-primary action_offer col-sm-12" 
                                    data-offer-id="${row[6]}"
                                    data-action="publish">
                                Опубликовать
                            </button>`
                    } else {
                        html += `
                            <button class="btn btn-primary action_offer col-sm-12" 
                                    data-offer-id="${row[6]}"
                                    data-action="extend">
                                Продлить
                            </button>`;
                        html += `
                            <button class="btn btn-primary action_offer col-sm-12" 
                                    data-offer-id="${row[6]}"
                                    data-action="delete">
                                Снять с публикации
                            </button>`
                    }
                    return html
                }
            }
        ]

    });


    dt_table.DataTable().ajax.reload();

    document.getElementById('btn-search').addEventListener('click', function () {
        dt_table.DataTable().ajax.reload();
    });

    function ActionOffer(offer_id, action, dt_table) {
        let modal = new tingle.modal({
            footer: true,
            stickyFooter: false,
            closeMethods: ['overlay', 'button', 'escape'],
            closeLabel: "Close",
            cssClass: ["modal-confirm"]
        });
        switch (action) {
            case 'publish':
                modal.setContent(`<h3>Отображать с</h3>
                               <div class="d-flex flex-row date input-daterange" id="range-picker">
                                      <div class="form-group">
                                        <input type="text" name="range-start" class="form-control datepicker-input">
                                      </div>
                                      <div class="flex-grow-0">
                                        <h3>по</h3>
                                      </div>
                                      <div class="form-group">
                                        <input type="text" name="range-end" class="form-control datepicker-input">
                                      </div>
                                </div>`);
                let dateRangePicker = new DateRangePicker(document.getElementById('range-picker'), {
                    "format": 'dd.mm.yyyy'
                    // language: 'ru',
                });
                modal.addFooterBtn('Да', 'tingle-btn tingle-btn--primary', function () {
                    PublishOffer(offer_id, action, dateRangePicker.getDates(), dt_table)
                    modal.close()
                });
                modal.addFooterBtn('Нет', 'tingle-btn tingle-btn--primary', function () {
                    modal.close();
                });
                modal.open();
                break;
            case 'extend':
                modal.setContent(`<h3>Продлить до</h3>
                                  <div class="form-group">
                                    <input type="text" id="extend_to" class="form-control datepicker-input">
                                  </div>`);
                let datePicker = new Datepicker(document.getElementById('extend_to'), {
                    "format": 'dd.mm.yyyy'
                    // language: 'ru',
                });
                modal.addFooterBtn('Да', 'tingle-btn tingle-btn--primary', function () {
                    ExtendOffer(offer_id, action, datePicker.getDate(), dt_table);
                    modal.close()
                });
                modal.addFooterBtn('Нет', 'tingle-btn tingle-btn--primary', function () {
                    modal.close();
                });
                modal.open();
                break;
            case 'delete':
                modal.setContent(`Снять объявление с публикации?`);
                modal.addFooterBtn('Да', 'tingle-btn tingle-btn--primary', function () {
                    DeleteOffer(offer_id, action, dt_table);
                    modal.close()
                });
                modal.addFooterBtn('Нет', 'tingle-btn tingle-btn--primary', function () {
                    modal.close();
                });
                modal.open();
                break;
        }

        function PublishOffer(offer_id, action, dates, dt_table) {
            $.ajax({
                "type": 'POST',
                "url": OFFERS_DO_ACTION,
                "data": {
                    "offer_id": offer_id,
                    "start": dates[0].toJSON(),
                    "end": dates[1].toJSON(),
                    "action": action,
                    "csrfmiddlewaretoken": l_csrf_token,
                },
                "success": function (response) {
                    console.log(response);
                    dt_table.DataTable().ajax.reload();
                },
            });
        }

        function ExtendOffer(offer_id, action, date, dt_table) {
            $.ajax({
                "type": 'POST',
                "url": OFFERS_DO_ACTION,
                "data": {
                    "offer_id": offer_id,
                    "end": date.toJSON(),
                    "action": action,
                    "csrfmiddlewaretoken": l_csrf_token,
                },
                "success": function (response) {
                    console.log(response);
                    dt_table.DataTable().ajax.reload();
                },
            });
        }

        function DeleteOffer(offer_id, action, dt_table) {
            $.ajax({
                "type": 'POST',
                "url": OFFERS_DO_ACTION,
                "data": {
                    "offer_id": offer_id,
                    "action": action,
                    "csrfmiddlewaretoken": l_csrf_token,
                },
                "success": function (response) {
                    console.log(response);
                    dt_table.DataTable().ajax.reload();
                },
            });
        }
    }


    function ConfirmModal(callback) {
        let modal = new tingle.modal({
            footer: true,
            stickyFooter: false,
            closeMethods: ['overlay', 'button', 'escape'],
            closeLabel: "Close",
            cssClass: ["modal-confirm"]
        });
        modal.setContent('Вы уверены?');
        modal.addFooterBtn('Да', 'tingle-btn tingle-btn--primary', callback);
        modal.addFooterBtn('Нет', 'tingle-btn tingle-btn--primary', function () {
            modal.close();
        });
        modal.open()
    }
});

