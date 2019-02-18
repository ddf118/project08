function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
//    var mySwiper = new Swiper ('.swiper-container', {
//        loop: true,
//        autoplay: 2000,
//        autoplayDisableOnInteraction: false,
//        pagination: '.swiper-pagination',
//        paginationType: 'fraction'
//    })
    $(".book-house").show();
    $.get('/home/detail/', function(data){
        var search = document.location.search
        id = search.split('=')[1]
        $.get('/home/detail/'+ id +'/',function(data){
            console.log(data.house)
//            获取当前用户的图片并填充
            for(index in data.house.images){
                image = data.house.images[index]
                var imgNode = $('<img/>').attr('src', image)
                var liNode = $('<li></li>').attr('class', 'swiper-slide')
                liNode.append(imgNode)
                $('.swiper-wrapper').append(liNode)
            }
//            轮播
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
            $('.house-price span').html(data.house.price)
            console.log('/static/media/' + data.house.user_avatar)
            $('.landlord-pic').html('<img src="'+ '/static/media/' + data.house.user_avatar + '">')
            $('.landlord-name span').html(data.house.user_name)
            $('.house-info-list>text-center li').html(data.house.address)
            $('#p1 span').html(data.house.acreage)
            $('#p2 span').html(data.house.unit)
            $('#capacity').html('宜住' + data.house.capacity + '人')
            $('#beds').html(data.house.beds)
            var house_info_style = '<li>收取押金<span>' + data.house.deposit + '</span></li>'
            house_info_style += '<li>最少入住天数<span>' + data.house.min_days + '</span></li>'
            house_info_style += '<li>最多入住天数<span>' + data.house.max_days + '</span></li>'
            $('.house-info-list').html(house_info_style)
            for(index in data.house.facilities){
                facility = data.house.facilities[index]
                var spanNode1 = $('<span class="' + facility.css + '"></span>')
                var spanNode2 = $('<span>' + facility.name + '</span>')
                var liNode1 = $('<li></li>')
                liNode1.append(spanNode1)
                liNode1.append(spanNode2)
                $('.house-facility-list').append(liNode1)
            }
            $('.book-house').attr('href',  '/order/booking/?house=' + data.house.id)
        })
    })
})


