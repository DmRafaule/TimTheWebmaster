"use strict";window.addEventListener("load",function(){const e=document.querySelectorAll("fieldset.collapse");for(const[n,t]of e.entries())if(t.querySelectorAll("div.errors, ul.errorlist").length===0){t.classList.add("collapsed");const s=t.querySelector("h2"),e=document.createElement("a");e.id="fieldsetcollapser"+n,e.className="collapse-toggle",e.href="#",e.textContent=gettext("Show"),s.appendChild(document.createTextNode(" (")),s.appendChild(e),s.appendChild(document.createTextNode(")"))}const t=function(e){if(e.target.matches(".collapse-toggle")){e.preventDefault(),e.stopPropagation();const t=e.target.closest("fieldset");t.classList.contains("collapsed")?(e.target.textContent=gettext("Hide"),t.classList.remove("collapsed")):(e.target.textContent=gettext("Show"),t.classList.add("collapsed"))}};document.querySelectorAll("fieldset.module").forEach(function(e){e.addEventListener("click",t)})})