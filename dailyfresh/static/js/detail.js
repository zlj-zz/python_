$(function () {
    // 计算商品总价
    function update_goods_amount() {
        price = parseFloat($('.show_pirze>em').text());
        count = parseInt($('.num_show').val());

        amount = price * count;

        $('.total>em').text(amount.toFixed(2) + '￥');


    };
    update_goods_amount();

    $('.add').click(function () {
        count = parseInt($('.num_show').val()) + 1;
        $('.num_show').val(count);
        update_goods_amount();
    });

    $('.minus').click(function () {
        count = parseInt($('.num_show').val()) - 1;
        if (count <= 0) {
            count = 1;
        }
        $('.num_show').val(count);
        update_goods_amount();
    });

    $('.num_show').blur(function () {
        count = ($(this).val());
        if (isNaN(count) || count.trim().length == 0 || parseInt(count) <= 0) {
            count = 1;
        }
        $(this).val(parseInt(count));
        update_goods_amount();
    });
    // ***************************

    var $add_x = $('#add_cart').offset().top;
    var $add_y = $('#add_cart').offset().left;

    var $to_x = $('#show_count').offset().top;
    var $to_y = $('#show_count').offset().left;

    $('#add_cart').click(function () {
        // ajax - post request
        sku_id = $(this).attr('sku_id');
        console.log(sku_id)
        count = $('.num_show').val();
        csrf = $('input[name=csrfmiddlewaretoken]').val();
        params = {'sku_id': sku_id, 'count': count, 'csrfmiddlewaretoken': csrf};
        $.post('/cart/add', params, function (data) {
            if (data.res == 5) {
                $(".add_jump").css({'left': $add_y + 80, 'top': $add_x + 10, 'display': 'block'})
                $(".add_jump").stop().animate({
                        'left': $to_y + 7,
                        'top': $to_x + 7
                    },
                    "fast", function () {
                        $(".add_jump").fadeOut('fast', function () {
                            // 重新设置购物车商品数
                            $('#show_count').html(data.total_count);
                        });
                    });
            } else {
                alert(data.errmsg);
            }
        });
    });
})