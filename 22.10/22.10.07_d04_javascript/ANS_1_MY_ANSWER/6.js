// 숫자를 넘겨줬을 때, 1 부터 해당 숫자까지의 총합을 구하는 totalSum함수를 구현하세요
// 0보다 클때까지 반복, i-- 는 1만큼 감소시키는 연산, 아래 결과는 66

function totalSum(n){
    let total = 0;
    for(let i= n ; i > 0 ; i--){total += i;}
    return total;
}

let num = 11
let result = totalSum(num)
console.log(result)

