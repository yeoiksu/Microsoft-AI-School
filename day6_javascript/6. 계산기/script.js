$(document).ready(function (){
    let numArray = [];
    let opArray  = [];

    let totalElement = '';
    let finalResult = 0;

    let valueElement  = 'value';
    let screenElement = $('.screen');
    let numElements   = $('.num');
    let opElements    = $('.op');
    

    numElements.click(function(){
        let numValue = parseInt( $(this).attr(valueElement)); 
        displayScreen(screenElement,numValue);
    })

    opElements.click(function(){
        let opValue = $(this).attr(valueElement);
        // operator가 = 일 때
        if(opValue == '='){
            
            // screen에 있는 텍스트를 가져옴
            totalElement = screenElement.text();
            // string을 regression(+,-,*,/)을 활용하여 split하고 Number로 map함
            numArray = totalElement.split(/[+,*,/,-]/).map(Number);
            opArray.push(opValue);     
            
            // 두개의 배열의 순서를 뒤집음
            numArray.reverse();
            opArray.reverse();

            console.log(numArray)
            if(finalResult < 0){
                numArray.pop();
                numArray.pop();

                console.log(numArray)
                numArray.push(finalResult);
                console.log(numArray)
            }

            console.log(numArray);
            // console.log(opArray);
            // console.log(finalResult);

            // 연산이 끝날 때 까지 반복하기
            for(let i = opArray.length-1; i > 0; i-- ){
                // numArray의 마지막 2개와 opArray의 마지막 1개를 calculator를 사용하여 연산
                let result = caculator(numArray[i], numArray[i-1], opArray[i]);
                // 연산후 numArray 마지막 2개의 요소를 pop하고 연산결과를 마지막에 push함  
                numArray.pop();
                numArray.pop();
                numArray.push(result);
            }
                
            opArray.length  = 0;
            finalResult = numArray[0]
            screenElement.empty();
            displayScreen(screenElement,finalResult);

        // clear일 때
        }else if(opValue == 'clear'){
            reset(numArray,opArray,screenElement);
        
        // 그 외 operation일 때
        }else{
            opArray.push(opValue);
            displayScreen(screenElement,opValue);
        }
    })

    function caculator(num1,num2,op){
        if (op == '+'){
            return num1+num2;
        }else if(op == '-'){
            return num1-num2;
        }else if(op == '*'){
            return num1*num2;
        }else if(op == '/'){   
            if(num2 ==0){
                reset(numArray,opArray,screenElement);
                alert('분모는 0이 될 수 없습니다');
            }else{
                return num1/num2;
            }    
        }else{
            return 0;
        }
    }

    function reset(arr1,arr2,el){
        arr1.length = 0;
        arr2.length = 0;
        el.empty();
    }

    function displayScreen($el,content){
        $el.append(content);
    }

    // function seperateNumOp(arr){
    //     let numAry = [];
    //     let opAry  = [];
    //     let tepIndex = 0;

    //     for (let i=0; i < arr.length; i++){
    //         if(typeof(arr[i]) == 'string'){
    //             opAry.push(arr[i]);

    //             let tempNum = 0;
    //             for(let j= tepIndex; j < i; j++){
    //                 tempNum += arr[j] * (10**(i-j) );
    //             }
    //             numAry.push(tempNum);
    //             tepIndex = i;
    //         }

    //     }

    //     return numAry, opAry;
    // }

});



