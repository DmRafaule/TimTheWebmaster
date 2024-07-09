"use strict";function quickElement(){const e=document.createElement(arguments[0]);if(arguments[2]){const t=document.createTextNode(arguments[2]);e.appendChild(t)}const t=arguments.length;for(let n=3;n<t;n+=2)e.setAttribute(arguments[n],arguments[n+1]);return arguments[1].appendChild(e),e}function removeChildren(e){for(;e.hasChildNodes();)e.removeChild(e.lastChild)}function findPosX(e){let t=0;if(e.offsetParent)for(;e.offsetParent;)t+=e.offsetLeft-e.scrollLeft,e=e.offsetParent;else e.x&&(t+=e.x);return t}function findPosY(e){let t=0;if(e.offsetParent)for(;e.offsetParent;)t+=e.offsetTop-e.scrollTop,e=e.offsetParent;else e.y&&(t+=e.y);return t}Date.prototype.getTwelveHours=function(){return this.getHours()%12||12},Date.prototype.getTwoDigitMonth=function(){return this.getMonth()<9?"0"+(this.getMonth()+1):this.getMonth()+1},Date.prototype.getTwoDigitDate=function(){return this.getDate()<10?"0"+this.getDate():this.getDate()},Date.prototype.getTwoDigitTwelveHour=function(){return this.getTwelveHours()<10?"0"+this.getTwelveHours():this.getTwelveHours()},Date.prototype.getTwoDigitHour=function(){return this.getHours()<10?"0"+this.getHours():this.getHours()},Date.prototype.getTwoDigitMinute=function(){return this.getMinutes()<10?"0"+this.getMinutes():this.getMinutes()},Date.prototype.getTwoDigitSecond=function(){return this.getSeconds()<10?"0"+this.getSeconds():this.getSeconds()},Date.prototype.getAbbrevMonthName=function(){return typeof window.CalendarNamespace=="undefined"?this.getTwoDigitMonth():window.CalendarNamespace.monthsOfYearAbbrev[this.getMonth()]},Date.prototype.getFullMonthName=function(){return typeof window.CalendarNamespace=="undefined"?this.getTwoDigitMonth():window.CalendarNamespace.monthsOfYear[this.getMonth()]},Date.prototype.strftime=function(e){const s={b:this.getAbbrevMonthName(),B:this.getFullMonthName(),c:this.toString(),d:this.getTwoDigitDate(),H:this.getTwoDigitHour(),I:this.getTwoDigitTwelveHour(),m:this.getTwoDigitMonth(),M:this.getTwoDigitMinute(),p:this.getHours()>=12?"PM":"AM",S:this.getTwoDigitSecond(),w:"0"+this.getDay(),x:this.toLocaleDateString(),X:this.toLocaleTimeString(),y:(""+this.getFullYear()).substr(2,4),Y:""+this.getFullYear(),"%":"%"};let n="",t=0;for(;t<e.length;)e.charAt(t)==="%"?(n=n+s[e.charAt(t+1)],++t):n=n+e.charAt(t),++t;return n},String.prototype.strptime=function(e){const o=e.split(/[.\-/]/),n=this.split(/[.\-/]/);let t=0,i,a,s;for(;t<o.length;){switch(o[t]){case"%d":i=n[t];break;case"%m":a=n[t]-1;break;case"%Y":s=n[t];break;case"%y":parseInt(n[t],10)>=69?s=n[t]:s=new Date(Date.UTC(n[t],0)).getUTCFullYear()+100;break}++t}return new Date(Date.UTC(s,a,i))}