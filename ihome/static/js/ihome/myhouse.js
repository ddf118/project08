$(document).ready(function(){
    $(".auth-warn").show();
    $("#houses-list").hide();

//    进行实名认证后，隐藏去实名认证
    $.ajax({
        url:'/user/user_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            if(data.info.id_card){
                $('.auth-warn').hide();
                $("#houses-list").show();
            }
        }
    })

//    显示房屋信息
    $.ajax({
        url:'/home/home_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            if(data.code == '200'){
                for(index in data.simple_houses){
                    console.log(data.simple_houses[index])
                    house = data.simple_houses[index]
                    var liNode = $('<li></li>')
                    var ddf = '/home/detail/?house=' + house.id
                    console.log(ddf)
                    var aNode = $('<a></a>').attr('href', ddf)
                    var div1Node = $('<div class="house-title"></div>')
                    var h3Node = $('<h3></h3>').html('房屋ID:'+house.id+' —— ' + house.title)
                    var div2Node = $('<div class="house-content"></div>')
                    var imgNode = $('<img/>').attr('src', house.image)
                    var div3Node = $('<div class="house-text">')
                    var ulNode = $('<ul></ul>')
                    var li1Node = $('<li></li>')
                    ulNode.append($('<li></li>').html('位于：' + house.area))
                    ulNode.append($('<li></li>').html('价格：￥' + house.price + '/晚'))
                    ulNode.append($('<li></li>').html('发布时间：' + house.create_time))
                    div3Node.append(ulNode)
                    div2Node.append(imgNode)
                    div2Node.append(div3Node)
                    div1Node.append(h3Node)
                    aNode.append(div1Node)
                    aNode.append(div2Node)
                    liNode.append(aNode)
                    $('#houses-list').append(liNode)
                }
            }
        }
    })
})