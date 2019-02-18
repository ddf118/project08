function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$(document).ready(function(){
    $("#real-name").focus(function(){
        $(".error-msg").hide();
    });
    $("#id-card").focus(function(){
        $(".error-msg").hide();
    });
// 显示姓名身份证，存在就隐藏保存按钮
    $.ajax({
        url:'/user/user_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            $('#real-name').attr('value', data.info.id_name);
            $('#id-card').attr('value', data.info.id_card);
            if(data.info.id_card){
                $('#ddf').hide();
                $('#real-name').attr('disabled', 'disabled');
                $('#id-card').attr('disabled', 'disabled');
            }
        }
    })
//    异步传输ajax
    $("#form-auth").submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/auth/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                console.log(data)
                if(data.code == '1001' || data.code == '1002' || data.code == '1003' || data.code == '1004'){
                    $('.error-msg').show();
                    $('.error-msg span').html(data.msg);
                }
                if(data.code == '200'){
                    alert(data.msg);
                    location.reload();
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });
})
