function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

// 随机线
function drawline (canvas, context) {
    context.moveTo(Math.floor(Math.random() * canvas.width), Math.floor(Math.random() * canvas.height)); //随机线的起点x坐标是画布x坐标0位置，y坐标是画布高度的随机数
    context.lineTo(Math.floor(Math.random() * canvas.width), Math.floor(Math.random() * canvas.height)); //随机线的终点x坐标是画布宽度，y坐标是画布高度的随机数
    context.lineWidth = 0.5; //随机线宽
    context.strokeStyle = 'rgba(50,50,50,0.3)'; //随机线描边属性
    context.stroke(); //描边，即起点描到终点
}

// 随机点(所谓画点其实就是画1px像素的线，方法不再赘述)
function drawDot (canvas, context) {
    var px = Math.floor(Math.random() * canvas.width);
    var py = Math.floor(Math.random() * canvas.height);
    context.moveTo(px, py);
    context.lineTo(px + 1, py + 1);
    context.lineWidth = 0.2;
    context.stroke();
}

// 绘制图片
function convertCanvasToImage (canvas) {
    document.getElementById("verifyCanvas").style.display = "none";
    var image = document.getElementById("code_img");
    image.src = canvas.toDataURL("image/png");
    return image;
}

//绘制图片验证码
function drawCode(data){
    var canvas = document.getElementById("verifyCanvas")//获取HTML端画布
    var context = canvas.getContext('2d')//获取画布2D上下文
    context.fillStyle = "cornflowerblue"; //画布填充色
    context.fillRect(0, 0, canvas.width, canvas.height); //清空画布
    context.fillStyle = "white"; //设置字体颜色
    context.font = "25px Arial"; //设置字体
    context.fillText(data, 20, 30);
    //画3条随机线
    for (var i = 0; i < 3; i++) {
        drawline(canvas, context);
    }
    // 画30个随机点
    for (var i = 0; i < 30; i++) {
        drawDot(canvas, context);
    }
    convertCanvasToImage(canvas);
}

// 点击图片刷新
document.getElementById('code_img').onclick = function() {
    resetCode();
}

function resetCode () {
    $('#verifyCanvas').remove();
    $('#code_img').before('<canvas width="100" height="41" id="verifyCanvas"></canvas>')
    verVal = drawCode();
}

function generateImageCode() {
//获取验证码，并渲染页面
    $.ajax({
        url:'/user/code/',
        dataType: 'json',
        type: 'GET',
        success:function(data){
//            渲染验证码
//            $('.image-code p').html(data.data)
//            TODO: 将字符串生成图片
              drawCode(data.data)
        }
    })
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    $.get("/api/smscode", {mobile:mobile, code:imageCode, codeId:imageCodeId},
        function(data){
            if (0 != data.errno) {
                $("#image-code-err span").html(data.errmsg);
                $("#image-code-err").show();
                if (2 == data.errno || 3 == data.errno) {
                    generateImageCode();
                }
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            }
            else {
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒");
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码');
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60);
            }
    }, 'json');
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        imagecode = $("#imagecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
//        异步提交注册请求，ajax
        $.ajax({
            url:'/user/register/',
            type:'POST',
            dataType:'json',
            data:{'mobile': mobile, 'imagecode': imagecode,
            'passwd': passwd, 'passwd2': passwd2},
            success:function(data){
//                console.log(data)
                if(data.code == '1002'){
                    $('#mobile-err span').html(data.msg);
                    $("#mobile-err").show();
                }
                if(data.code == '1003'){
                    $('#image-code-err span').html(data.msg);
                    $("#image-code-err").show();
                }
                if(data.code == '1004'){
                    $('#password-err span').html(data.msg);
                    $("#password-err").show();
                }
                if(data.code == '1001'){
                    $('#password2-err span').html(data.msg);
                    $("#password2-err").show();
                }
                if(data.code == '200'){
                    $(location).attr('href', '/user/login/');
                }
            },
            error:function(data){
                alert('error')
            }
        })
    });
})