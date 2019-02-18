var cur_page = 1; // 当前页
var next_page = 1; // 下一页
var total_page = 1;  // 总页数
var house_data_querying = true;   // 是否正在向后台获取数据

// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

// 更新用户点选的筛选条件
function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}


// 更新房源列表信息
// action表示从后端请求的数据在前端的展示方式
// 默认采用追加方式
// action=renew 代表页面数据清空从新展示
function updateHouseData(action) {
    // 每次点击能重新生成相应的
    $(".house-list").empty();
    var areaId = $(".filter-area>li.active").attr("area-id");
    if (undefined == areaId) areaId = "";
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var sortKey = $(".filter-sort>li.active").attr("sort-key");
    var params = {
        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
    };
    console.log(params)
    if(params.aid){
        //    发起ajax请求，获取数据，并显示在模板中
        $.get('/home/my_search/', params, function(data){
            if(data.code == '200'){
                for(index in data.houses_list){
                    house = data.houses_list[index]
                    //组装信息
                    var info = '<span class="house-title">' + house.title +  house.id + '</span>'
                    info += '<em>出租' + house.room + '间 - 1次入住 - ' + house.address + '</em>'
                    var liNode = $('<li class="house-item"></li>')
                    var aNode = $('<a><img src="'+ house.image +'"></a>').attr('href', '/home/detail/?house='+ house.id)
                    var divNode11 = $('<div class="landlord-pic"><img src="/static/media/' + house.user_avatar + '"></div>')
                    var divNode12 = $('<div class="house-price">￥<span>' + house.price + '</span>/晚</div>')
                    var divNode13 = $('<div class="house-intro"></div>').html(info)
                    var divNode1 = $('<div class="house-desc"></div>')
                    divNode1.append(divNode11)
                    divNode1.append(divNode12)
                    divNode1.append(divNode13)
                    liNode.append(aNode)
                    liNode.append(divNode1)
                    $('.house-list').append(liNode)
                }
            }
        })
    }
}

$(document).ready(function(){
    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start-date").val(startDate);
    $("#end-date").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName) areaName = "位置区域";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function(e){
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
        }
    });
    $(".display-mask").on("click", function(e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        cur_page = 1;
        next_page = 1;
        total_page = 1;
        updateHouseData("renew");
    });
    $(".filter-item-bar>.filter-area").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
    $(".filter-item-bar>.filter-sort").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(2).children("span").eq(0).html($(this).html());
        }
    });

    // 第一次跳转过来的页面
    $.get('/home/my_search/', queryData , function(data){
        if(data.code == '200'){
            for(index in data.houses_list){
                house = data.houses_list[index]
                //组装信息
                var info = '<span class="house-title">' + house.title +  house.id + '</span>'
                info += '<em>出租' + house.room + '间 - 1次入住 - ' + house.address + '</em>'
                var liNode = $('<li class="house-item"></li>')
                var aNode = $('<a><img src="'+ house.image +'"></a>').attr('href', '/home/detail/?house='+ house.id)
                var divNode11 = $('<div class="landlord-pic"><img src="/static/media/' + house.user_avatar + '"></div>')
                var divNode12 = $('<div class="house-price">￥<span>' + house.price + '</span>/晚</div>')
                var divNode13 = $('<div class="house-intro"></div>').html(info)
                var divNode1 = $('<div class="house-desc"></div>')
                divNode1.append(divNode11)
                divNode1.append(divNode12)
                divNode1.append(divNode13)
                liNode.append(aNode)
                liNode.append(divNode1)
                $('.house-list').append(liNode)
            }
        }
    })
})

//各地区信息接口
$.get('/home/area_info/',function(data){
    if(data.code == '200'){
        for(index in data.areas_list){
            area = data.areas_list[index]
            var liNode = $('<li></li>').attr('area-id', area.id).html(area.name)
//            info = '<li area-id="' + area.id + '">' + area.name + '</li>'
            $('.filter-area').append(liNode)
        }
    }
})




