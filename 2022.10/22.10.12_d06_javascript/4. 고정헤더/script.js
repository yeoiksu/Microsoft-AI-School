//  menu가 페이스북을 지나는 순간 위에 고정되고
// 다시 위로가면 원래위치
$(document).ready(function () {
    let facebookTop = $('ul').offset().top;
    $(window).on('scroll', function(e){
        let scrollTop = $(this).scrollTop();
        if(scrollTop > facebookTop){
            console.log(scrollTop, facebookTop);
            $('ul').css({
                'position' : 'fixed',
                'top' : 0
            });
        }else{
            $('ul').css('position','relative')
        }
    });

});
