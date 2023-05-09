// let contador = 0;
// const boton = document.querySelector("#boton");
// const spanContador = document.querySelector("#contador");
            
// boton.addEventListener("click", () => {
//     contador++;
//     spanContador.textContent = contador;
// });



console.log('hello world')
const timer = document.getElementById('displaytimer')
console.log(timer.textContent)
const inputtag = document.getElementById('timer')


t=0

setInterval(()=>{
    t+=1
    timer.innerHTML ="<b>Este es mi timer: " +t+" seconds</b>"
    inputtag.value = t
},1000)