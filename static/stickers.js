var imgHeight = 74;
var imgWidth = 62;
var numImgs = 4;
var cont = 0;
 
var animation = setInterval(function(){
    var xgrid = Math.floor(cont / 2)
    var ygrid = cont - xgrid * 2
    
    var xpos =  -5 - (xgrid*imgWidth);
    var ypos =  -5 - (ygrid*imgHeight);
    $('.animated-sticker').css('background-position', xpos + 'px ' + ypos + 'px');
    
    console.log("this is a test");
    
    cont++;
    if(cont == numImgs){
        cont = 0;
    }
},100);
