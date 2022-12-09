// 객체를 넘겨 받았을 때, 객체의 number 속성이 홀수인 인 것들의 number의 총합을 계산하는 함수 objectSum을 구현하세요. 
// 아래 결과 값은 22입니다.

function objectSum(numO){
    let total = 0;
    for(let i = 0; i < numO.length; i++){
        if(i % 2 == 1){total += numO[i]['number'];}
    }
    return total;
}

// let numObject = [{'name':'lee', 'number':22}, {'name':'park','number':11}, {'name':'yeo','number':33}, {'name':'ik','number':44}]
let numObject = [{'name':'lee', 'number':22}, {'name':'park','number':11}]
let result = objectSum(numObject)
console.log(result)
