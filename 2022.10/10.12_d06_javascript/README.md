# Day6. Javascript & jQuery

1. 탭 메뉴와 패널 과제<br>
    - [x] 메뉴 아이템 hover 시, 배경색 pink, 높이 75px 변경, hover 벗어나면 원래대로
    - [x] 메뉴 아이템 click 시, 배경색 lightseagreen, 글자 색 white 해당 콘텐츠 출력
2. 아코디언
    - [x] 메뉴 클릭 시, 배경색과 콘텐츠 출력<
    - [x] 다른 메뉴 클릭 시, 기존에 열렸던 창이 닫히고 클릭된 메뉴 열림<
    - [x] 열린 메뉴 클릭 시, 다시 닫힘
3. 툴팁
    - [] 마우스가 각 요소 hover시에, title 속성의 값을 마우스의 위치를 따라가면서 출력, 마우스가 요소를 벗어나면 안보임
    - [] 관련 이벤트: mouseenter, mouseleave, mousemove
    - [] 마우스 위치: event.pageX, event.pageY
4. 고정헤더
    - [] 스크롤 위치 가져오기 $(window).scrollTop()
    - [] 요소의 위치를 가져오는 방법 $(‘el’).offset().top
    - [] 스크롤 이벤트 처리 $(window).on(‘scroll’, function(e){})
5. 구구단
    - [x] 숫자 버튼을 누르면 해당하는 구구단을 출력
6. 계산기
    - [x] 버튼을 누르면 해당 수와 연산자가 스크린에 표시된다.
    - [x] '='버튼을 누르면 결과값이 스크린에 표시된다. 사칙연산의 우선순위는 고려하지 않는다
    - [x] 'c' 버튼을 누르면 모두 지워진다
    - [x] '=' 버튼을 누르면 결과값이 스크린에 표시 된 상태에서도 연산이 가능해진다
    - [x] 자리수의 상관없이 계산 가능
