// 배열을 넘겼을 때 배열의 요소 중에 ‘국어’의 갯수를 반환하는 함수 countKorean을 작성하세요

function countKorean(array){
    let count = 0;
    for(let i =0; i<array.length ; i++){
        if(array[i]=='국어'){count +=1;}
    }
    return count;
}

let subs = ['국어','수학','영어','국어','과학']
// let subs = ['국어','수학','영어','국어','과학','국어','국어']
let result = countKorean(subs)
console.log(result)
