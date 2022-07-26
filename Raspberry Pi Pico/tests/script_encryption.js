
//Author: bermejo4

function funcioncolor(numero){
    if(numero>=0){
        return "greenyellow";
    }else{
        return "deeppink";
    }
}

function CalcularEnDinero(){
    var porcentaje=document.getElementById('resultadofinal').textContent.substring(0,5).valueOf();
    var cantidad=document.getElementById('campodedinero').value;
    var dineronuevo=cantidad*(porcentaje/100);
    if(dineronuevo>=0){
        document.getElementById('DineroNuevo').innerHTML="La ganancia ha sido de: "+ "+".fontcolor(funcioncolor(dineronuevo))+
        dineronuevo.toFixed(2).fontcolor(funcioncolor(dineronuevo))+ " "+ document.getElementById('tipoDeMoneda').value.fontcolor(funcioncolor(dineronuevo));
    }else{
     document.getElementById('DineroNuevo').innerHTML="La perdida ha sido de:"+
     dineronuevo.toFixed(2).fontcolor(funcioncolor(dineronuevo))+ " "+ document.getElementById('tipoDeMoneda').value.fontcolor(funcioncolor(dineronuevo)); 
    }
    var dinerototal=parseFloat(cantidad)+parseFloat(dineronuevo);
    document.getElementById('DineroTotal').innerHTML="Ahora cuenta con: "+dinerototal+ " "+ document.getElementById('tipoDeMoneda').value;

}

function desactivarboton(id) {
    document.getElementById(this.id).disabled = true;
}

function calculo(num1, num2){
    var solucion=0;
    console.log('num1:'+num1);
    console.log('num2:'+num2);
    solucion=((num2-num1)/num1)*100;
    console.log('sol:'+solucion);
    return solucion.toFixed(3);
}
