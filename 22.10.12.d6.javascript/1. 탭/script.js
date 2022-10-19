// 정한 index를 select_index
let select_index = 0;


$(document).ready(function () {
    // hover 여부
    let enableHover = 1;
    let falseHover  = 0;
    let selectElement = $('ul li');

    // 첫 tab인 구글로 초기화 
    setSelect(select_index);

    // ul의 li가 hover됬을 때 setHover함수 호출
    // mouseenter 됬을 때
    selectElement.hover(function (e) {
        setHover($(this), enableHover);
    // mouseleave 됬을 때
    }, function (e) {
        setHover($(this), falseHover);
    })

    // 클릭 됬을 때 setSelect함수 호출
    selectElement.click(function (e) {
        setSelect($(this).index());
    })
});

// 탭 정하기 (클릭했을 때)
function setSelect(index) {
    let listElement = $('ul li');
    let contentElement = $('.content');

    // list의 index를 정해서 select 클래스 추가하기
    listElement.eq(index).addClass('select');
    // content 보여주기
    contentElement.eq(index).addClass('select').show();

    // 다른 tab을 선택했을 때
    if (index != select_index) {
        // select함수 삭제하기
        listElement.eq(select_index).removeClass('select');
        // 기존 content내용 숨기기
        contentElement.eq(select_index).hide();
        select_index = index;
    }   
}

// hover 기능 (마우스가 올려져 있을때, 삭제될 때)
function setHover(el, add) {
    // 마우스가 위에 있을 때
    if (add == 1) {
        // element의 index를 가져오기
        var el_index = el.index();
        
        // select 됬을 때 배경 pink로 바뀌는 부분
        if (select_index == el_index) {
            el.removeClass('select');
        }
        el.addClass('hover');

        // 애니메이션
        el.animate({
            height: '75px',
            'line-height': '60px'
        });
    //  마우스가 삭제될 때
    } else {
        el.removeClass('hover');
        el.animate({
            height: '40px',
            'line-height': '35px'
        });
        if (select_index == el.index()) {
            el.addClass('select');
        }
    }
}