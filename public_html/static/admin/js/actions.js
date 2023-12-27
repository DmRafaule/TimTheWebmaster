"use strict";{function show(e){document.querySelectorAll(e).forEach(function(e){e.classList.remove("hidden")})}function hide(e){document.querySelectorAll(e).forEach(function(e){e.classList.add("hidden")})}function showQuestion(e){hide(e.acrossClears),show(e.acrossQuestions),hide(e.allContainer)}function showClear(e){show(e.acrossClears),hide(e.acrossQuestions),document.querySelector(e.actionContainer).classList.remove(e.selectedClass),show(e.allContainer),hide(e.counterContainer)}function reset(e){hide(e.acrossClears),hide(e.acrossQuestions),hide(e.allContainer),show(e.counterContainer)}function clearAcross(e){reset(e);const t=document.querySelectorAll(e.acrossInput);t.forEach(function(e){e.value=0}),document.querySelector(e.actionContainer).classList.remove(e.selectedClass)}function checker(e,t,n){n?showQuestion(t):reset(t),e.forEach(function(e){e.checked=n,e.closest("tr").classList.toggle(t.selectedClass,n)})}function updateCounter(e,t){const n=Array.from(e).filter(function(e){return e.checked}).length,s=document.querySelector(t.counterContainer),i=Number(s.dataset.actionsIcnt);s.textContent=interpolate(ngettext("%(sel)s of %(cnt)s selected","%(sel)s of %(cnt)s selected",n),{sel:n,cnt:i},!0);const o=document.getElementById(t.allToggleId);o.checked=n===e.length,o.checked?showQuestion(t):clearAcross(t)}const e={actionContainer:"div.actions",counterContainer:"span.action-counter",allContainer:"div.actions span.all",acrossInput:"div.actions input.select-across",acrossQuestions:"div.actions span.question",acrossClears:"div.actions span.clear",allToggleId:"action-toggle",selectedClass:"selected"};window.Actions=function(t,n){n=Object.assign({},e,n);let o=!1,s=null,i=!1;document.addEventListener("keydown",e=>{i=e.shiftKey}),document.addEventListener("keyup",e=>{i=e.shiftKey}),document.getElementById(n.allToggleId).addEventListener("click",function(){checker(t,n,this.checked),updateCounter(t,n)}),document.querySelectorAll(n.acrossQuestions+" a").forEach(function(e){e.addEventListener("click",function(e){e.preventDefault();const t=document.querySelectorAll(n.acrossInput);t.forEach(function(e){e.value=1}),showClear(n)})}),document.querySelectorAll(n.acrossClears+" a").forEach(function(e){e.addEventListener("click",function(e){e.preventDefault(),document.getElementById(n.allToggleId).checked=!1,clearAcross(n),checker(t,n,!1),updateCounter(t,n)})});function r(e,n){const r=s&&n&&s!==e;if(!r)return[e];const o=Array.from(t),i=o.findIndex(t=>t===e),a=o.findIndex(e=>e===s),c=Math.min(i,a),l=Math.max(i,a),d=o.filter((e,t)=>c<=t&&t<=l);return d}Array.from(document.getElementById("result_list").tBodies).forEach(function(e){e.addEventListener("change",function(e){const a=e.target;if(a.classList.contains("action-select")){const e=r(a,i);checker(e,n,a.checked),updateCounter(t,n),s=a}else o=!0})}),document.querySelector("#changelist-form button[name=index]").addEventListener("click",function(e){if(o){const t=confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));t||e.preventDefault()}});const a=document.querySelector("#changelist-form input[name=_save]");a&&a.addEventListener("click",function(e){if(document.querySelector("[name=action]").value){const t=gettext(o?"You have selected an action, but you haven’t saved your changes to individual fields yet. Please click OK to save. You’ll need to re-run the action.":"You have selected an action, and you haven’t made any changes on individual fields. You’re probably looking for the Go button rather than the Save button.");confirm(t)||e.preventDefault()}})};function ready(e){document.readyState!=="loading"?e():document.addEventListener("DOMContentLoaded",e)}ready(function(){const e=document.querySelectorAll("tr input.action-select");e.length>0&&Actions(e)})}