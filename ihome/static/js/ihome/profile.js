function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
//展示曾用名和图片
    $.ajax({
        url:'/user/user_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            if(data.code == '200'){
                $('#user-avatar').attr('src', '/static/media/'+data.info.avatar);
                $('#user-name').attr('placeholder', data.info.name);
            }
        }
    })

    $("#user-name").focus(function(){
        $("#name-err").hide();
        $("#avatar-err").hide();
    });
    $("#user-image").focus(function(){
        $("#avatar-err").hide();
        $("#name-err").hide();
    });
    $("#form-avatar").submit(function(e){
        e.preventDefault();
//        异步提交图片，ajax
        $(this).ajaxSubmit({
            url:'/user/profile/picture_profile/',
            type:'PATCH',
            dataType:'json',
            success:function(data){
                console.log(data)
                if(data.code == '1001'){
                    $('#avatar-err span').html(data.msg);
                    $("#avatar-err").show();
                }
                if(data.code == '200'){
                    alert(data.msg)
//                    $('#user-avatar').attr('src', '/static/media/'+data.ddf);
                    $(location).attr('href', '/user/my/');
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });
    $("#form-name").submit(function(e){
        e.preventDefault();
        name = $("#user-name").val();
//        异步提交用户名，ajax
        $.ajax({
            url:'/user/profile/user_profile/',
            type:'PATCH',
            dataType:'json',
            data:{'name': name},
            success:function(data){
                console.log(data)
                if(data.code == '1002' || data.code == '1001'){
                    $('#name-err span').html(data.msg);
                    $("#name-err").show();
                }
                if(data.code == '200'){
                    alert(data.msg)
                    $(location).attr('href', '/user/my/');
                }
            },
            error:function(data){
                alert('error')
            }
        })
    });
})