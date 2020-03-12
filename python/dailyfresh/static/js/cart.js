$(function () {
    // 计算选中
    function update_page_info() {
        tatol_count = 0;
        tatol_price = 0;
        $('.cart_list_td').find(':checked').parents('ul').each(function () {
            count = $(this).find('.num_show').val()
            amount = $(this).children('.col07').text()
            tatol_count += parseInt(count);
            tatol_price += parseFloat(amount);
        });
        $('.settlements').find('em').text(tatol_price.toFixed(2));
        $('.settlements').find('b').text(tatol_count);
    };

    // 计算小记
    function update_goods_amount(sku_ul) {
        count = sku_ul.find('.num_show').val();
        price = sku_ul.children('.col05').text();
        amount = parseInt(count) * parseFloat(price);
        sku_ul.children('.col07').text(amount.toFixed(2) + '元');
    };
    // ajax function
    error_update = false;
    tatol = 0;

    function update_ajax(sku_id, count) {
        csrf = $('input[name="csrfmiddlewaretoken"]').val();
        params = {'sku_id': sku_id, 'count': count, 'csrfmiddlewaretoken': csrf};
        $.ajaxSettings.async = false;
        $.post('/cart/update', params, function (data) {
            if (data.res == 5) {
                error_update = false
                tatol = data.total_count
            } else {
                error_update = true
                alert(data.errmsg)
            }
        });
        $.ajaxSettings.async = true;
    };


    // 全选
    $('.settlements').find(':checkbox').change(function () {
        is_checked = $(this).prop('checked');
        $('.cart_list_td').find(':checkbox').each(function () {
            $(this).prop('checked', is_checked);
        });
        update_page_info();
    });
    //
    $('.cart_list_td').find(':checkbox').change(function () {
        all_length = $('.cart_list_td').length;
        checked_length = $('.cart_list_td').find(':checked').length;
        if (checked_length < all_length) {
            $('.settlements').find(':checkbox').prop('checked', false);
        } else {
            $('.settlements').find(':checkbox').prop('checked', true);
        }
        update_page_info();
    });
    // ajax
    $('.add').click(function () {
        sku_id = $(this).next().attr('sku_id');
        count = parseInt($(this).next().val()) + 1;
        update_ajax(sku_id, count);
        if (error_update == false) {
            $(this).next().val(count);
            update_goods_amount($(this).parents('ul'));
            update_page_info();
            $('.total_count>em').text(tatol);
        }
    });
    $('.minus').click(function () {
        sku_id = $(this).prev().attr('sku_id');
        count = parseInt($(this).prev().val()) - 1;
        if (count <= 0) {
            count = 1;
        }
        update_ajax(sku_id, count);
        if (error_update == false) {
            $(this).prev().val(count);
            update_goods_amount($(this).parents('ul'));
            update_page_info();
            $('.total_count>em').text(tatol)
        }
    });
    pre_count = 0;
    $('.num_show').focus(function () {
        pre_count = $(this).val();
    });
    $('.num_show').blur(function () {
        sku_id = $(this).attr('sku_id');
        count = $(this).val();
        if (parseInt(count) <= 0 || isNaN(count) || count.trim().length == 0) {
            $(this).val(pre_count);
            return
        }
        count = parseInt(count);
        update_ajax(sku_id, count);
        if (error_update == false) {
            $(this).val(count);
            update_goods_amount($(this).parents('ul'));
            update_page_info();
            $('.total_count>em').text(tatol)
        } else {
            $(this).val(pre_count);
        }
    });
    // delete
    $('.cart_list_td').children('.col08').children('a').click(function () {
        sku_id = $(this).parents('ul').find('.num_show').attr('sku_id');
        csrf = $('input[name="csrfmiddlewaretoken"]').val();
        params = {'sku_id': sku_id, 'csrfmiddlewaretoken': csrf};
        sku_ul = $(this).parents('ul');
        $.post('/cart/delete', params, function (data) {
            if (data.res == 3) {
                sku_ul.remove();
                update_page_info();
                $('.total_count>em').text(tatol);
            } else {
                alert(data.errmsg);
            }
        });
    });
});