"use strict";{const n=["BUTTON","INPUT","SELECT","TEXTAREA"],e=document.getElementById("django-admin-form-add-constants").dataset.modelName;let t=!1;if(e){const s=document.getElementById(e+"_form");s.addEventListener("submit",e=>{if(e.preventDefault(),t){const e=window.confirm(gettext("You have already submitted this form. Are you sure you want to submit it again?"));if(!e)return}e.target.submit(),t=!0});for(const e of s.elements)if(n.includes(e.tagName)&&!e.disabled&&e.offsetParent){e.focus();break}}}