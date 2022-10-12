$(document).ready(function () {
    let facebook_top = $('ul').offset().top;
    $(window).on('scroll', function (e) {
        let scroll_top = $(this).scrollTop();
        if(scroll_top > facebook_top){
            $('ul').css({
                'position': 'fixed',
                'top': 0
            });
        }else{
            $('ul').css('position', 'relative');
        }
    })
});