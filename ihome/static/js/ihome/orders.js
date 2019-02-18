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
                li_info += '<li>我的评价：' + order.comment + '</li>'
                li_info += '<li>拒单原因：</li>'
//                组装评价评价
                var comment_info = '<button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button>'
//                创建order-content div1标签
                var div1Node = $('<div></div>').attr('class', 'order-content')
                var img1Node = $('<img>').attr('src', order.image)
                var div11Node = $('<div></div>').attr('class', 'order-text')
                var ulNode = $('<ul></ul>')
                ulNode.html(li_info)
                div11Node.append($('<h3>订单</h3>'))
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
                div21Node.html(comment_info)
                div2Node.append(h3Node)
                div2Node.append(div21Node)
//                创建li标签
                var liNode = $('<li></li>').attr('order-id', order.order_id)
                liNode.append(div2Node)
                liNode.append(div1Node)
                $('.orders-list').append(liNode)
//                显示我的评价
                if(order.status == 'WAIT_COMMENT'){
                    $('#' + order.order_id).show()
                }
        }
        }
        //    发表评价点击事件
        $(".order-comment").click(function(){
//        获取li标签的orderId的id值
            var orderId = $(this).parents("li").attr("order-id");
//        给发表评价标签添加orderId
            $(".modal-comment").attr("order-id", orderId);
        });
    });

//    发表评价确定点击事件
    $('.modal-comment').click(function(){
//        获取评论参数
        var comment = $('#comment').val()
//        获取当前订单id值
        var order_id = $('.modal-comment').attr('order-id')
        data = {'comment': comment, 'order_id': order_id}
        //订单参数——异步传输
        $.ajax({
        url:'/order/order/',
        type:'PATCH',
        dataType:'json',
        data: data,
        success:function(data){
            if(data.code == '200'){
                alert('发表评价成功')
                location.reload()
            }
        }
    })
    });

});