$(document).ready(function(){var t=$("h2, h3, h4, h5, h6"),e=[];t.each(function(){let o=$(this).text(),s="#ref-"+o;s=s.replace(/[^#a-zA-Z0-9а-яА-Я]/g,"-").toLowerCase();let t=this.nodeName.toLowerCase(),n="padder-5";t=="h2"?n="padder-5":t=="h3"?n="padder-10":t=="h4"?n="padder-15":t=="h5"?n="padder-20":t=="h6"&&(n="padder-25"),e.push({text:o,ref:s,tag_name:t,padding:n}),$(this).attr("id",s.replace("#",""))}),$.ajax({type:"POST",url:"/"+language_code+"/load_table_of_content/",data:{titles:JSON.stringify(e)},headers:{"X-CSRFToken":csrftoken},mode:"same-origin",success:function(e){var t,n,s=$("h1");$(e).insertAfter(s),t=document.querySelectorAll(".up_button"),t.forEach(e=>{e.addEventListener("click",function(){pushUpButton(this)})}),n=document.querySelectorAll(".table_of_content_text"),n.forEach(e=>{e.addEventListener("click",function(){var t=$(e).attr("href"),n=100;jumpTo(t,n)})})}})});function jumpTo(e,t){var n=$(e).offset();n.top-=t,window.scrollTo(n)}function pushUpButton(e){e.classList.add("icon_button_pressed"),e.addEventListener("animationend",t=>{e.classList.remove("icon_button_pressed")})}