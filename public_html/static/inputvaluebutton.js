class InputValueButton{constructor(e,t){this.elements=document.querySelectorAll(e),this.elements.forEach(e=>{e.addEventListener("change",function(e){var n=e.target.value,s=e.target.dataset.field;t(n,s)})})}update(e){for(var t=0;t<this.elements.length;t++)this.elements[t].value=e[t]}}