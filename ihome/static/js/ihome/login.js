function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
//        异步提交登录请求，ajax
        $.ajax({
            url:'/user/my_login/',
            type:'GET',
            dataType:'json',
            data:{'mobile': mobile, 'passwd': passwd},
            success:function(data){
                console.log(data)
                if(data.code == '1002'){
                    $('#mobile-err span').html(data.msg);
                    $("#mobile-err").show();
                }
                if(data.code == '1003' || data.code == '1001'){
                    $('#password-err span').html(data.msg);
                    $("#password-err").show();
                }
                if(data.code == '200'){
//                    $(location).attr('href', '/home/index/');
                    location.href = '/home/index/';
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });
})