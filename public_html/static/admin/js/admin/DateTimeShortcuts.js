"use strict";{const e={calendars:[],calendarInputs:[],clockInputs:[],clockHours:{default_:[[gettext_noop("Now"),-1],[gettext_noop("Midnight"),0],[gettext_noop("6 a.m."),6],[gettext_noop("Noon"),12],[gettext_noop("6 p.m."),18]]},dismissClockFunc:[],dismissCalendarFunc:[],calendarDivName1:"calendarbox",calendarDivName2:"calendarin",calendarLinkName:"calendarlink",clockDivName:"clockbox",clockLinkName:"clocklink",shortCutsClass:"datetimeshortcuts",timezoneWarningClass:"timezonewarning",timezoneOffset:0,init:function(){const t=document.body.dataset.adminUtcOffset;if(t){const n=(new Date).getTimezoneOffset()*-60;e.timezoneOffset=n-t}for(const t of document.getElementsByTagName("input"))t.type==="text"&&t.classList.contains("vTimeField")?(e.addClock(t),e.addTimezoneWarning(t)):t.type==="text"&&t.classList.contains("vDateField")&&(e.addCalendar(t),e.addTimezoneWarning(t))},now:function(){const e=document.body.dataset.adminUtcOffset;if(e){const t=new Date,n=t.getTimezoneOffset()*-60;return t.setTime(t.getTime()+1e3*(e-n)),t}return new Date},addTimezoneWarning:function(t){const i=e.timezoneWarningClass;let n=e.timezoneOffset/3600;if(!n)return;if(t.parentNode.querySelectorAll("."+i).length)return;let s;n>0?s=ngettext("Note: You are %s hour ahead of server time.","Note: You are %s hours ahead of server time.",n):(n*=-1,s=ngettext("Note: You are %s hour behind server time.","Note: You are %s hours behind server time.",n)),s=interpolate(s,[n]);const o=document.createElement("span");o.className=i,o.textContent=s,t.parentNode.appendChild(document.createElement("br")),t.parentNode.appendChild(o)},addClock:function(t){const n=e.clockInputs.length;e.clockInputs[n]=t,e.dismissClockFunc[n]=function(){return e.dismissClock(n),!0};const o=document.createElement("span");o.className=e.shortCutsClass,t.parentNode.insertBefore(o,t.nextSibling);const a=document.createElement("a");a.href="#",a.textContent=gettext("Now"),a.addEventListener("click",function(t){t.preventDefault(),e.handleClockQuicklink(n,-1)});const i=document.createElement("a");i.href="#",i.id=e.clockLinkName+n,i.addEventListener("click",function(t){t.preventDefault(),t.stopPropagation(),e.openClock(n)}),quickElement("span",i,"","class","clock-icon","title",gettext("Choose a Time")),o.appendChild(document.createTextNode(" ")),o.appendChild(a),o.appendChild(document.createTextNode(" | ")),o.appendChild(i);const s=document.createElement("div");s.style.display="none",s.style.position="absolute",s.className="clockbox module",s.id=e.clockDivName+n,document.body.appendChild(s),s.addEventListener("click",function(e){e.stopPropagation()}),quickElement("h2",s,gettext("Choose a time"));const r=quickElement("ul",s);r.className="timelist";const l=typeof e.clockHours[t.name]=="undefined"?"default_":t.name;e.clockHours[l].forEach(function(t){const s=quickElement("a",quickElement("li",r),gettext(t[0]),"href","#");s.addEventListener("click",function(s){s.preventDefault(),e.handleClockQuicklink(n,t[1])})});const c=quickElement("p",s);c.className="calendar-cancel";const d=quickElement("a",c,gettext("Cancel"),"href","#");d.addEventListener("click",function(t){t.preventDefault(),e.dismissClock(n)}),document.addEventListener("keyup",function(t){t.which===27&&(e.dismissClock(n),t.preventDefault())})},openClock:function(t){const n=document.getElementById(e.clockDivName+t),s=document.getElementById(e.clockLinkName+t);window.getComputedStyle(document.body).direction!=="rtl"?n.style.left=findPosX(s)+17+"px":n.style.left=findPosX(s)-110+"px",n.style.top=Math.max(0,findPosY(s)-30)+"px",n.style.display="block",document.addEventListener("click",e.dismissClockFunc[t])},dismissClock:function(t){document.getElementById(e.clockDivName+t).style.display="none",document.removeEventListener("click",e.dismissClockFunc[t])},handleClockQuicklink:function(t,n){let s;n===-1?s=e.now():s=new Date(1970,1,1,n,0,0,0),e.clockInputs[t].value=s.strftime(get_format("TIME_INPUT_FORMATS")[0]),e.clockInputs[t].focus(),e.dismissClock(t)},addCalendar:function(t){const n=e.calendars.length;e.calendarInputs[n]=t,e.dismissCalendarFunc[n]=function(){return e.dismissCalendar(n),!0};const o=document.createElement("span");o.className=e.shortCutsClass,t.parentNode.insertBefore(o,t.nextSibling);const c=document.createElement("a");c.href="#",c.appendChild(document.createTextNode(gettext("Today"))),c.addEventListener("click",function(t){t.preventDefault(),e.handleCalendarQuickLink(n,0)});const a=document.createElement("a");a.href="#",a.id=e.calendarLinkName+n,a.addEventListener("click",function(t){t.preventDefault(),t.stopPropagation(),e.openCalendar(n)}),quickElement("span",a,"","class","date-icon","title",gettext("Choose a Date")),o.appendChild(document.createTextNode(" ")),o.appendChild(c),o.appendChild(document.createTextNode(" | ")),o.appendChild(a);const s=document.createElement("div");s.style.display="none",s.style.position="absolute",s.className="calendarbox module",s.id=e.calendarDivName1+n,document.body.appendChild(s),s.addEventListener("click",function(e){e.stopPropagation()});const l=quickElement("div",s),d=quickElement("a",l,"<","href","#");d.className="calendarnav-previous",d.addEventListener("click",function(t){t.preventDefault(),e.drawPrev(n)});const u=quickElement("a",l,">","href","#");u.className="calendarnav-next",u.addEventListener("click",function(t){t.preventDefault(),e.drawNext(n)});const m=quickElement("div",s,"","id",e.calendarDivName2+n);m.className="calendar",e.calendars[n]=new Calendar(e.calendarDivName2+n,e.handleCalendarCallback(n)),e.calendars[n].drawCurrent();const i=quickElement("div",s);i.className="calendar-shortcuts";let r=quickElement("a",i,gettext("Yesterday"),"href","#");r.addEventListener("click",function(t){t.preventDefault(),e.handleCalendarQuickLink(n,-1)}),i.appendChild(document.createTextNode(" | ")),r=quickElement("a",i,gettext("Today"),"href","#"),r.addEventListener("click",function(t){t.preventDefault(),e.handleCalendarQuickLink(n,0)}),i.appendChild(document.createTextNode(" | ")),r=quickElement("a",i,gettext("Tomorrow"),"href","#"),r.addEventListener("click",function(t){t.preventDefault(),e.handleCalendarQuickLink(n,+1)});const h=quickElement("p",s);h.className="calendar-cancel";const f=quickElement("a",h,gettext("Cancel"),"href","#");f.addEventListener("click",function(t){t.preventDefault(),e.dismissCalendar(n)}),document.addEventListener("keyup",function(t){t.which===27&&(e.dismissCalendar(n),t.preventDefault())})},openCalendar:function(t){const n=document.getElementById(e.calendarDivName1+t),s=document.getElementById(e.calendarLinkName+t),o=e.calendarInputs[t];if(o.value){const a=get_format("DATE_INPUT_FORMATS")[0],n=o.value.strptime(a),i=n.getUTCFullYear(),s=n.getUTCMonth()+1,r=/\d{4}/;r.test(i.toString())&&s>=1&&s<=12&&e.calendars[t].drawDate(s,i,n)}window.getComputedStyle(document.body).direction!=="rtl"?n.style.left=findPosX(s)+17+"px":n.style.left=findPosX(s)-180+"px",n.style.top=Math.max(0,findPosY(s)-75)+"px",n.style.display="block",document.addEventListener("click",e.dismissCalendarFunc[t])},dismissCalendar:function(t){document.getElementById(e.calendarDivName1+t).style.display="none",document.removeEventListener("click",e.dismissCalendarFunc[t])},drawPrev:function(t){e.calendars[t].drawPreviousMonth()},drawNext:function(t){e.calendars[t].drawNextMonth()},handleCalendarCallback:function(t){const n=get_format("DATE_INPUT_FORMATS")[0];return function(s,o,i){e.calendarInputs[t].value=new Date(s,o-1,i).strftime(n),e.calendarInputs[t].focus(),document.getElementById(e.calendarDivName1+t).style.display="none"}},handleCalendarQuickLink:function(t,n){const s=e.now();s.setDate(s.getDate()+n),e.calendarInputs[t].value=s.strftime(get_format("DATE_INPUT_FORMATS")[0]),e.calendarInputs[t].focus(),e.dismissCalendar(t)}};window.addEventListener("load",e.init),window.DateTimeShortcuts=e}