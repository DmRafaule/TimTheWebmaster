"use strict";{const e=django.jQuery;let n=0;const t=[];function dismissChildPopups(){t.forEach(function(e){e.closed||(e.dismissChildPopups(),e.close())})}function setPopupIndex(){if(document.getElementsByName("_popup").length>0){const e=window.name.lastIndexOf("__")+2;n=parseInt(window.name.substring(e))}else n=0}function addPopupIndex(e){return e=e+"__"+(n+1),e}function removePopupIndex(e){return e=e.replace(new RegExp("__"+(n+1)+"$"),""),e}function showAdminPopup(e,n,s){const a=addPopupIndex(e.id.replace(n,"")),o=new URL(e.href);s&&o.searchParams.set("_popup",1);const i=window.open(o,a,"height=500,width=800,resizable=yes,scrollbars=yes");return t.push(i),i.focus(),!1}function showRelatedObjectLookupPopup(e){return showAdminPopup(e,/^lookup_/,!0)}function dismissRelatedLookupPopup(e,n){const o=removePopupIndex(e.name),s=document.getElementById(o);s.classList.contains("vManyToManyRawIdAdminField")&&s.value?s.value+=","+n:document.getElementById(o).value=n;const i=t.indexOf(e);i>-1&&t.splice(i,1),e.close()}function showRelatedObjectPopup(e){return showAdminPopup(e,/^(change|add|delete)_/,!1)}function updateRelatedObjectLinks(t){const s=e(t),n=s.nextAll(".view-related, .change-related, .delete-related");if(!n.length)return;const o=s.val();o?n.each(function(){const t=e(this);t.attr("href",t.attr("data-href-template").replace("__fk__",o))}):n.removeAttr("href")}function updateRelatedSelectsOptions(e,t,n,s,o){const i=t.location.pathname,a=i.split("/")[i.split("/").length-(n?4:3)],r=document.querySelectorAll(`[data-model-ref="${a}"] select`);r.forEach(function(t){if(e===t)return;let i=t.querySelector(`option[value="${n}"]`);if(!i){i=new Option(s,o),t.options.add(i);return}i.textContent=s,i.value=o})}function dismissAddRelatedObjectPopup(n,s,o){const a=removePopupIndex(n.name),i=document.getElementById(a);if(i){const t=i.nodeName.toUpperCase();t==="SELECT"?(i.options[i.options.length]=new Option(o,s,!0,!0),updateRelatedSelectsOptions(i,n,null,o,s)):t==="INPUT"&&(i.classList.contains("vManyToManyRawIdAdminField")&&i.value?i.value+=","+s:i.value=s),e(i).trigger("change")}else{const e=a+"_to",t=new Option(o,s);SelectBox.add_to_cache(e,t),SelectBox.redisplay(e)}const r=t.indexOf(n);r>-1&&t.splice(r,1),n.close()}function dismissChangeRelatedObjectPopup(n,s,o,i){const a=removePopupIndex(n.name.replace(/^edit_/,"")),l=interpolate("#%s, #%s_from, #%s_to",[a,a,a]),r=e(l);r.find("option").each(function(){this.value===s&&(this.textContent=o,this.value=i)}).trigger("change"),updateRelatedSelectsOptions(r[0],n,s,o,i),r.next().find(".select2-selection__rendered").each(function(){this.lastChild.textContent=o,this.title=o});const c=t.indexOf(n);c>-1&&t.splice(c,1),n.close()}function dismissDeleteRelatedObjectPopup(n,s){const o=removePopupIndex(n.name.replace(/^delete_/,"")),a=interpolate("#%s, #%s_from, #%s_to",[o,o,o]),r=e(a);r.find("option").each(function(){this.value===s&&e(this).remove()}).trigger("change");const i=t.indexOf(n);i>-1&&t.splice(i,1),n.close()}window.showRelatedObjectLookupPopup=showRelatedObjectLookupPopup,window.dismissRelatedLookupPopup=dismissRelatedLookupPopup,window.showRelatedObjectPopup=showRelatedObjectPopup,window.updateRelatedObjectLinks=updateRelatedObjectLinks,window.dismissAddRelatedObjectPopup=dismissAddRelatedObjectPopup,window.dismissChangeRelatedObjectPopup=dismissChangeRelatedObjectPopup,window.dismissDeleteRelatedObjectPopup=dismissDeleteRelatedObjectPopup,window.dismissChildPopups=dismissChildPopups,window.showAddAnotherPopup=showRelatedObjectPopup,window.dismissAddAnotherPopup=dismissAddRelatedObjectPopup,window.addEventListener("unload",function(){window.dismissChildPopups()}),e(document).ready(function(){setPopupIndex(),e("a[data-popup-opener]").on("click",function(t){t.preventDefault(),opener.dismissRelatedLookupPopup(window,e(this).data("popup-opener"))}),e("body").on("click",'.related-widget-wrapper-link[data-popup="yes"]',function(t){if(t.preventDefault(),this.href){const t=e.Event("django:show-related",{href:this.href});e(this).trigger(t),t.isDefaultPrevented()||showRelatedObjectPopup(this)}}),e("body").on("change",".related-widget-wrapper select",function(){const n=e.Event("django:update-related");e(this).trigger(n),n.isDefaultPrevented()||updateRelatedObjectLinks(this)}),e(".related-widget-wrapper select").trigger("change"),e("body").on("click",".related-lookup",function(t){t.preventDefault();const n=e.Event("django:lookup-related");e(this).trigger(n),n.isDefaultPrevented()||showRelatedObjectLookupPopup(this)})})}