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
    dt_table = $('#town-table').dataTable({
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
            }
        ],
        "bProcessing": true,
        "bServerSide": true,
        "bStateSave": true,
        "stripeClasses": [],
        "ajax": {
            "url": TOWN_OFFERS_LIST_JSON_URL,
            "data": function (d) {
                d.town = l_town_id;
                d.category = l_category_id;
                d.region = l_region_id;
                d.name = l_text_search;
            }
        },

        "rowCallback": function (row, data) {
            row.addEventListener('click', function () {
                location.href = G_OFFER_PAGE_URL.replace('99999999999999', data[0]);
            })
        }

    });
    ul_li_listener();
    document.querySelector('#search_btn').addEventListener('click', function () {
        l_text_search = document.querySelector('#search_field').value;
        $('#town-table').DataTable().ajax.reload();
    });
});

function ul_li_listener() {
    let regions_block = document.querySelector('#region-filter');
    let regions = regions_block.querySelectorAll('li');
    [].forEach.call(regions, function (el) {
        el.addEventListener('click', function () {
            [].forEach.call(regions, function (element) {
                element.classList.remove('selected');
            });
            el.classList.add('selected');
            l_region_id = el.dataset.regionId;
            $('#town-table').DataTable().ajax.reload();
        })
    });
    let category_block = document.querySelector('#category-filter');
    let category = category_block.querySelectorAll('li');
    [].forEach.call(category, function (el) {
        el.addEventListener('click', function () {
            [].forEach.call(category, function (element) {
                element.classList.remove('selected');
            });
            el.classList.add('selected');
            l_category_id = el.dataset.categoryId;
            $('#town-table').DataTable().ajax.reload();
        })
    })
}


// document.addEventListener('DOMContentLoaded', function () {
//     ul_li_listener();
//
//     document.querySelector('#search_btn').addEventListener('click', function () {
//         l_text_search = document.querySelector('#search_field').value;
//         getAjaxOffers();
//     });
//     getAjaxOffers();
// });
//
// function getAjaxOffers() {
//     $.ajax({
//         "type": 'POST',
//         "url": l_ajax_get_offers,
//         "data": {
//             "town": l_town_id,
//             "region": l_region_id,
//             "category": l_category_id,
//             "text_search": l_text_search,
//             "page": 0,
//             "csrfmiddlewaretoken": l_csrf_token,
//         },
//         "success": function (response) {
//             console.log(response);
//             refreshOfferBoard(response);
//
//             $(".offer-iframe").click(function () {
//                 if (is_auth) {
//                     $.fancybox.open({
//                         href: is_auth ? g_offer_url.replace('99999999999999', this.dataset.offerId) : login_url,
//                         type: 'iframe',
//                         padding: 0,
//                         height: 800,
//                     });
//                 } else {
//                     location.href = login_url
//                 }
//             });
//             $(".reviews-iframe").click(function () {
//                 if (is_auth) {
//                     $.fancybox.open({
//                         href: is_auth ? g_reviews_url.replace('99999999999999', this.dataset.offerId) : login_url,
//                         type: 'iframe',
//                         padding: 0,
//                         height: 800,
//                         autoSize: false
//                     });
//                 } else {
//                     location.href = login_url
//                 }
//             });
//         },
//     });
// }
//
// function refreshOfferBoard(response) {
//     let board = document.getElementById('opi-board');
//     board.innerHTML = '';
//     for (let rec in response) {
//         if (response.hasOwnProperty(rec)) {
//             board.insertAdjacentHTML("beforeend", createOffer(
//                 response[rec]['offer_avatar'],
//                 response[rec]['name'],
//                 response[rec]['category_name'],
//                 response[rec]['offer_timework'],
//                 response[rec]['offer_phone'],
//                 response[rec]['offer_id']));
//         }
//     }
// }
//
// function ul_li_listener() {
//     let regions_block = document.querySelector('#region-filter');
//     let regions = regions_block.querySelectorAll('li');
//     [].forEach.call(regions, function (el) {
//         el.addEventListener('click', function () {
//             [].forEach.call(regions, function (element) {
//                 element.classList.remove('selected');
//             });
//             el.classList.add('selected');
//             l_region_id = el.dataset.regionId;
//
//             getAjaxOffers();
//         })
//     });
//     let category_block = document.querySelector('#category-filter');
//     let category = category_block.querySelectorAll('li');
//     [].forEach.call(category, function (el) {
//         el.addEventListener('click', function () {
//             [].forEach.call(category, function (element) {
//                 element.classList.remove('selected');
//             });
//             el.classList.add('selected');
//             l_category_id = el.dataset.categoryId;
//             getAjaxOffers();
//         })
//     })
// }
//
// function reloadFilters() {
//
// }
//
//
// function createOffer(avatar, name, category, timework, phone, id) {
//     return `<div class="opi-offer col-sm-3">
//             <ul class="opi-offer-ul">
//                 <li class="opi-offer-image">
//                     <img src="${MEDIA_URL + avatar}" alt="">
//                 </li>
//                 <li class="opi-offer-title">
//                     <p>${name}</p>
//                 </li>
//                 <li class="opi-offer-info">
//                     <ul class="opi-offer-info-ul">
//                         <li class="opi-offer-category">
//                             <p>${category}</p>
//                         </li>
//                         <li class="opi-offer-timework">
//                             <b>영업시간</b> ${timework}
//                         </li>
//                         <li class="opi-offer-phone">
//                             <b>전화번호</b><a href="tel:${phone}"> ${phone}</a>
//                         </li>
//
//                     </ul>
//                 </li>
//                 <li class="opi-offer-actions">
//                     <ul class="opi-offer-action-ul">
//                         <li class="opi-action-li">
//                             <div class="opi-action-fawpforms"><a aria-expanded="true" data-offer-id="${id}"
//                                                                  class="offer-iframe">
//                                 <i class="fab fa-wpforms"></i><br>출근부</a>
//                             </div>
//                         </li>
//                         <li class="opi-action-li">
//                             <div class="opi-action-facomments"><a aria-expanded="true" data-offer-id="${id}"
//                                                                   class="reviews-iframe">
//                                 <i class="far fa-comment"></i><br>후기</a></div>
//                         </li>
//                     </ul>
//                 </li>
//             </ul>
//         </div>`
// }