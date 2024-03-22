"use strict";{const e={monthsOfYear:[gettext("January"),gettext("February"),gettext("March"),gettext("April"),gettext("May"),gettext("June"),gettext("July"),gettext("August"),gettext("September"),gettext("October"),gettext("November"),gettext("December")],monthsOfYearAbbrev:[pgettext("abbrev. month January","Jan"),pgettext("abbrev. month February","Feb"),pgettext("abbrev. month March","Mar"),pgettext("abbrev. month April","Apr"),pgettext("abbrev. month May","May"),pgettext("abbrev. month June","Jun"),pgettext("abbrev. month July","Jul"),pgettext("abbrev. month August","Aug"),pgettext("abbrev. month September","Sep"),pgettext("abbrev. month October","Oct"),pgettext("abbrev. month November","Nov"),pgettext("abbrev. month December","Dec")],daysOfWeek:[pgettext("one letter Sunday","S"),pgettext("one letter Monday","M"),pgettext("one letter Tuesday","T"),pgettext("one letter Wednesday","W"),pgettext("one letter Thursday","T"),pgettext("one letter Friday","F"),pgettext("one letter Saturday","S")],firstDayOfWeek:parseInt(get_format("FIRST_DAY_OF_WEEK")),isLeapYear:function(e){return e%4===0&&e%100!==0||e%400===0},getDaysInMonth:function(t,n){let s;return t===1||t===3||t===5||t===7||t===8||t===10||t===12?s=31:t===4||t===6||t===9||t===11?s=30:t===2&&e.isLeapYear(n)?s=29:s=28,s},draw:function(t,n,s,o,i){const h=new Date,y=h.getDate(),b=h.getMonth()+1,g=h.getFullYear();let c="",f=!1;typeof i!="undefined"&&(f=i.getUTCFullYear()===n&&i.getUTCMonth()+1===t),t=parseInt(t),n=parseInt(n);const m=document.getElementById(s);removeChildren(m);const d=document.createElement("table");quickElement("caption",d,e.monthsOfYear[t-1]+" "+n);const u=quickElement("tbody",d);let a=quickElement("tr",u);for(let t=0;t<7;t++)quickElement("th",a,e.daysOfWeek[(t+e.firstDayOfWeek)%7]);const p=new Date(n,t-1,1-e.firstDayOfWeek).getDay(),v=e.getDaysInMonth(t,n);let l;a=quickElement("tr",u);for(let e=0;e<p;e++)l=quickElement("td",a," "),l.className="nonday";function j(e,t){function n(n){n.preventDefault(),o(e,t,this.textContent)}return n}let r=1;for(let e=p;r<=v;e++){e%7===0&&r!==1&&(a=quickElement("tr",u)),r===y&&t===b&&n===g?c="today":c="",f&&r===i.getUTCDate()&&(c!==""&&(c+=" "),c+="selected");const s=quickElement("td",a,"","class",c),o=quickElement("a",s,r,"href","#");o.addEventListener("click",j(n,t)),r++}for(;a.childNodes.length<7;)l=quickElement("td",a," "),l.className="nonday";m.appendChild(d)}};function Calendar(e,t,n){this.div_id=e,this.callback=t,this.today=new Date,this.currentMonth=this.today.getMonth()+1,this.currentYear=this.today.getFullYear(),typeof n!="undefined"&&(this.selected=n)}Calendar.prototype={drawCurrent:function(){e.draw(this.currentMonth,this.currentYear,this.div_id,this.callback,this.selected)},drawDate:function(e,t,n){this.currentMonth=e,this.currentYear=t,n&&(this.selected=n),this.drawCurrent()},drawPreviousMonth:function(){this.currentMonth===1?(this.currentMonth=12,this.currentYear--):this.currentMonth--,this.drawCurrent()},drawNextMonth:function(){this.currentMonth===12?(this.currentMonth=1,this.currentYear++):this.currentMonth++,this.drawCurrent()},drawPreviousYear:function(){this.currentYear--,this.drawCurrent()},drawNextYear:function(){this.currentYear++,this.drawCurrent()}},window.Calendar=Calendar,window.CalendarNamespace=e}