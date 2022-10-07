// 성적이 90이상 점수들의 평균을 반환하는 함수 avg를 작성하세요

function avg(array){
    let total =0;
    for(let i=0; i<array.length; i++){total += array[i];}
    return (total / array.length);
}

let grads = [90,82,100,70,80]
// let grads = [90,100,80]
let result = avg(grads)
console.log(result)

