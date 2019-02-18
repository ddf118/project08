function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url:'/user/user_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            if(data.code == '200'){
                $('#user-avatar').attr('src', '/static/media/'+data.info.avatar);
                $('#user-name').html(data.info.name);
                $('#user-mobile').html(data.info.phone);
            }
        }
    })
})