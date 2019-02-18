//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    //    请求我的订单数据
    $.get('/order/my_orders/',function(data){
        if(data.code == '200'){
            for(index in data.orders_list){
                var order = data.orders_list[index]
//                组装订单参数
                var li_info = '<li>创建时间：' + order.create_date + '</li>'
                li_info += '<li>入住日期：' + order.begin_date + '</li>'
                li_info += '<li>离开日期：' + order.end_date + '</li>'
                li_info += '<li>合计金额：' + order.amount + '元(共' + order.days + '晚)</li>'
                li_info += '<li>订单状态：<span>' + order.status + '</span></li>'
                li_info += '<li>客户评价：' + order.comment + '</li>'
//                组装接单按钮和拒单按钮
                var accept_info = '<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal">接单</button>'
                var reject_info = '<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal">拒单</button>'
//                创建order-content div1标签
                var div1Node = $('<div></div>').attr('class', 'order-content')
                var img1Node = $('<img>').attr('src', order.image)
                var div11Node = $('<div></div>').attr('class', 'order-text')
                var ulNode = $('<ul></ul>')
                ulNode.html(li_info)
                div11Node.append($('<h3></h3>').html(order.house_title))
                div11Node.append(ulNode)
                div1Node.append(img1Node)
                div1Node.append(div11Node)
//                创建order-title div2标签
                var div2Node = $('<div></div>').attr('class', 'order-title')
                var div21Node = $('<div></div>').attr('class', 'fr order-operate')
                div21Node.attr('id', order.order_id)
//                隐藏我的评价
                div21Node.attr('style', 'display:none;')
                var h3Node = $('<h3></h3>').html('订单编号：' + order.order_id)
                div21Node.html(accept_info+reject_info)
                div2Node.append(h3Node)
                div2Node.append(div21Node)
//                创建li标签
                var liNode = $('<li></li>').attr('order-id', order.order_id)
                liNode.append(div2Node)
                liNode.append(div1Node)
                $('.orders-list').append(liNode)
////                显示我的评价
                if(order.status == 'WAIT_ACCEPT'){
                    $('#' + order.order_id).show()
                }
        }
//            接单按钮点击事件
            $(".order-accept").on("click", function(){
                alert('点击了接单')
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });
//            拒单按钮点击事件
            $(".order-reject").on("click", function(){
                alert('点击了拒单')
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });
        }

    });

    //    确定接单点击事件
    $('.modal-accept').click(function(){
        alert('确定接单了啊')
//        获取当前订单id值
        var order_id = $('.modal-accept').attr('order-id')
        data = {'order_id': order_id, 'status': 'WAIT_PAYMENT'}
        //订单参数——异步传输
        $.ajax({
        url:'/order/order/',
        type:'PATCH',
        dataType:'json',
        data: data,
        success:function(data){
            if(data.code == '200'){
                alert('接单成功')
                location.reload()
            }
        }
    })
    });

    //    拒单点击事件
    $('.modal-reject').click(function(){
        alert('确定拒单了啊')
//        获取当前订单id值
        var order_id = $('.modal-reject').attr('order-id')
//        获取拒单原因
        var reject_reason = $('#reject-reason').val()
        data = {'order_id': order_id, 'status': 'REJECTED', 'reject_reason':reject_reason}
        //订单参数——异步传输
        $.ajax({
        url:'/order/order/',
        type:'PATCH',
        dataType:'json',
        data: data,
        success:function(data){
            if(data.code == '200'){
                alert('拒单成功')
                location.reload()
            }
        }
    })
    });
});