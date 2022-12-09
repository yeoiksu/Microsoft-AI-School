// 배열을 넘겨 받았을 때, 짝수인 수들의 총합을 계산하는 evenSum함수를 구현하세요.
// 아래는 40이 출력됩니다.

function evenSum(array){
    let total = 0;
    for(let i=0; i < array.length; i++){
        if(array[i]%2==0){total += array[i];}
    }
    return total;
}

let numbers = [10,21,30]
let result = evenSum(numbers)
console.log(result)
