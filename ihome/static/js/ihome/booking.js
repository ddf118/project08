function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },2000)
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            var days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

//    预订——异步请求
    var url = location.search
    var house_id = url.split('=')[1]
    $.get('/order/booking/'+ house_id +'/',function(data){
            console.log(data.house)
            $('.house-info img').attr('src', data.house.image)
            $('.house-text span').html(data.house.price)
            $('.house-text h3').html(data.house.title)
    });

//    提交提单点击事件
    $('.submit-btn').click(function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        if(startDate == '' || endDate == ''){
            showErrorMsg()
        }
        data = {'house_id': house_id, 'end_date':endDate, 'begin_date': startDate};
        //订单参数——异步传输
        $.post('/order/order/', data, function(data){
            alert('提交成功')
            location.href = '/order/orders/'
        });
    });
})

//订单点击传输
//function order_submit() {
//    var startDate = $("#start-date").val();
//    var endDate = $("#end-date").val();
//    var sd = new Date(startDate);
//    var ed = new Date(endDate);
//    var days = (ed - sd)/(1000*3600*24) + 1;
//    var price = $(".house-text>p>span").html();
//    var amount = days * parseFloat(price);
//    //订单参数——异步传输
//    $.ajax({
//    url:'/order/create_order/',
//    type:'POST',
//    dataType:'json',
//    data:{'amount': amount,'house_price': price, 'days': days,
//          'end_date':endDate, 'begin_date': startDate},
//    success:function(data){
//        console.log(data)
//        if(data.code == '200'){
//            alert('传输成功')
//        }
//    },
//    error:function(data){
//        alert('请求失败')
//    }
//})
//}


//预订——异步请求
//$.get('/home/booking/', function(data){
//        var search = document.location.search
//        id = search.split('=')[1]
//        $.get('/home/booking/'+ id +'/',function(data){
//            console.log(data.house)
//            $('.house-info img').attr('src', data.house.image)
//            $('.house-text span').html(data.house.price)
//            $('.house-text h3').html(data.house.title)
//        })
//})

