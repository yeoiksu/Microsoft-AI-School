// 카운트를 하고 싶은 과목명과 배열을 넘겨줬을 때 해당 과목명의 수를 세는 countSubject함수를 구현하세요, 아래 결과는 1이 출력됩니다

function countSubject(subject,array){
    let count = 0;
    for(let i =0; i<array.length ; i++){
        if(array[i]==subject){count +=1;}
    }
    return count;
}

let subs = ['국어','수학','영어','국어','과학']
// let subs = ['국어','수학','영어','국어','과학','수학']
let result = countSubject('수학', subs)
console.log(result)
