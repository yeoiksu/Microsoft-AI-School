// 홀수인지 여부를 판단하는 함수 isOdd를 작성하세요. 파라미터 하나를 받습니다.
// 아래 실행 시에 true가 표시되어야 합니다.
// 홀수는 2로 나누었을 때, 나머지가 1입니다. ( % - 나누기 연산)

function isOdd(num ){
    if(num%2==1){
        return true;
    }else{
        return false;
    }

}

let number = 3
let result = isOdd(number)
console.log(result)
