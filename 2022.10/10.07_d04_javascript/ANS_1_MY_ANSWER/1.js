// 배열을 넘겨받았을 때 배열 안의 요소들의 총합을 구하는 함수 sum을 만드세요
// 60이 출력되어야 합니다.

function sum_total( array ){
    let total = 0
    for (let i=0; i<array.length; i++){total += array[i]}
    return total;    
}

let numbers = [10,20,30]
let result = sum_total(numbers)
console.log(result)
