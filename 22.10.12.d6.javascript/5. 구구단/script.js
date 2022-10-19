$(document).ready(function (){
    let buttonElements = $('button')
    let resultElement = $('#result')

    buttonElements.click(function(){
        let divContent = '';
        let targetNumber = $(this).text();
        // resultElement.empty();

        for(let i =1; i<10 ; i++){
            divContent += '<p>' + targetNumber + ' X '+  i + ' = ' 
                        + (targetNumber*i) + '</p>'
        }
        resultElement.html(divContent);
    });
});

