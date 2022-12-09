// 짝수인지 여부를 판단하는 함수 isEven를 작성하세요. 파라미터 하나를 받습니다.
// 아래 실행 시에 true가 표시되어야 합니다.
// 짝수는 2로 나누었을 때, 나머지가 0입니다. ( % - 나누기 연산)


function isEven(num ){
    if(num%2==0){
        return true;
    }else{
        return false;
    }
}

let number = 2
let result = isEven(number)
console.log(result)
