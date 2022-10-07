// 성적이 90이상게 몇개인지를 반환하는 함수 countGrade를 작성하세요

function countGrade(array){
    let count = 0;
    for (let i=0; i<array.length; i++){
        if(array[i] >= 90){count +=1;}
    }
    return count;
}

let grads = [90,82,100,70,80]
// let grads = [90,82,100,70,80,95]
let result = countGrade(grads)
console.log(result)
