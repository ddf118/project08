function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $(".form-control").focus(function(){
        $(".text-center").hide();
    });
    $("#house-image").focus(function(){
        $(".text-center1").hide();
    });
//    显示房屋信息
    $.ajax({
        url:'/home/area_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            if(data.code == '200'){
                for(index in data.areas_list){
                    var area = data.areas_list[index]
                    var optionNode = $('<option value=' + area.id + '>' + area.name + '</option>')
                    $('#area-id').append(optionNode)
                }
            }
        }
    })

//    显示配套设施信息
    $.ajax({
        url:'/home/facility_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            if(data.code == '200'){
                for(index in data.facilities_list){
                    var facility = data.facilities_list[index]
                    var liNode = $('<li></li>')
                    var divNode = $('<div class="checkbox"></div>')
                    var labelNode = $('<label></label>')
                    var inputNode = $('<input type="checkbox" name="facility" value=' + facility.id + '>')
                    var spanNode = $('<span>'+ facility.name + '</span>')
                    labelNode.append(inputNode)
                    labelNode.append(spanNode)
                    divNode.append(labelNode)
                    liNode.append(divNode)
                    $('.clearfix').append(liNode)
                }
            }
        }
    })

//    异步提交房屋信息
    $("#form-house-info").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/home/newhouse/newhouse_info/',
            type:'POST',
            dataType:'json',
            success:function(data){
                console.log(data)
                if(data.code == '1001'){
                    $('.text-center span').html(data.msg);
                    $('.text-center').show();
                }
                if(data.code == '200'){
                    $('#form-house-image').show()
                    $('#form-house-info').hide()
                    $('#house-id').attr('value', data.house_id)
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });

//    异步提交房屋图片
    $("#form-house-image").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/home/newhouse/newhouse_picture/',
            type:'POST',
            dataType:'json',
            success:function(data){
                console.log(data)
                if(data.code == '1001'){
                    $('.text-center1 span').html(data.msg);
                    $('.text-center1').show();
                }
                if(data.code == '200'){
                    var imgNode = $('<img/>').attr('src', data.image_url)
                    $('#form-house-image').prepend(imgNode)
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });
})