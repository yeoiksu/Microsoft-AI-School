let selected_index = -1;


$(document).ready(function () {

    $('ul li').hover(function (e) {
        // mouseleave 됬을 때

        // hover된 inndex 가져오기
        let index = $(this).index();
        $(this).eq(index).addClass('balloon')

        // var tooltipHtml = []
        // tooltipHtml.push("<div class='.balloon'>");
        // tooltipHtml.push("  " + $(this).eq(index).attr('title'))
        // tooltipHtml.push("</div>");
        // console.log(tooltipHtml.join(""));

        selected_index = index;
        

    }, function (e) {
        $(this).eq(selected_index).removeClass('.balloon');
    })

});

