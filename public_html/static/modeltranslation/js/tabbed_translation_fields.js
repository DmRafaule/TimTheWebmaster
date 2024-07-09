var google,django,gettext;(function(){var e=window.jQuery||$||django.jQuery;e.expr[":"].parents=function(t,n,s){return e(t).parents(s[3]).length<1},e(function(e){var t,s,o,i,a,l=function(){return document.querySelector("#jazzmin-theme, #jazzy-navbar, #jazzy-tabs, #jazzy-actions")?"jazzmin":"default"},d={default:{mainHeader:()=>e("#content").find("h1"),tabContainer:t=>e(t).closest(".form-row"),tabUlClass:"",tabLiClass:"",tabAClass:"",tabErrorClass:"ui-tab-has-errors"},jazzmin:{mainHeader:()=>e("#content-main").find(".card-title:first"),tabContainer:t=>e(t).closest(".form-group"),tabUlClass:"nav nav-tabs",tabLiClass:"nav-item",tabAClass:"nav-link",tabErrorClass:"ui-tab-has-errors"}};const n=d[l()];o=function(t){this.el=t.el,this.cls=t.cls,this.id="",this.origFieldname="",this.lang="",this.groupId="",this.init=function(){var t=this.cls.substring(o.cssPrefix.length,this.cls.length).split("-");this.origFieldname=t[0],this.lang=t[1],this.id=e(this.el).attr("id"),this.groupId=this.buildGroupId()},this.buildGroupId=function(){var e=this.id.split("-"),t="id_"+this.origFieldname;return e.length===3?t=e[0]+"-"+e[1]+"-"+t:e.length===4?t=e[0]+"-"+e[1]+"-"+e[2]+"-"+t:e.length===5&&e[3]!="__prefix__"?t=e[0]+"-"+e[1]+"-"+e[2]+"-"+e[3]+"-"+this.origFieldname:e.length===6?t=e[0]+"-"+e[1]+"-"+e[2]+"-"+e[3]+"-"+e[4]+"-"+this.origFieldname:e.length===7&&(t=e[0]+"-"+e[1]+"-"+e[2]+"-"+e[3]+"-"+e[4]+"-"+e[5]+"-"+this.origFieldname),t},this.init()},o.cssPrefix="mt-field-",s=function(t){this.$fields=t.$fields,this.groupedTranslations={},this.init=function(){this.$fields=this.$fields.add("fieldset.collapse-closed .mt"),this.groupedTranslations=this.getGroupedTranslations()},this.getGroupedTranslations=function(){var t=this,n=o.cssPrefix;return this.$fields.each(function(s,i){e.each(e(i).attr("class").split(" "),function(e,s){if(s.substring(0,n.length)===n){var a=new o({el:i,cls:s});t.groupedTranslations[a.groupId]||(t.groupedTranslations[a.groupId]={}),t.groupedTranslations[a.groupId][a.lang]=i}})}),this.groupedTranslations},this.init()};function r(t){var s=[];return e.each(t,function(t,o){if(t.includes("__prefix__"))return;var a,i=e("<div></div>"),r=e(`<ul class='${n.tabUlClass}'></ul>`),c=0;i.append(r),e.each(o,function(t,s){var l,u,o=n.tabContainer(s),m=e("label",o),d=o.find("label"),h="tab_"+e(s).attr("id");d.html()&&d.html(d.html().replace(/ \[.+\]/,"")),a||(a={insert:o.prev().length?"after":o.next().length?"prepend":"append",el:o.prev().length?o.prev():o.parent()}),o.find("script").remove(),u=e('<div id="'+h+'"></div>').append(o),l=e(`<li class='${n.tabLiClass} `+(m.hasClass("required")?"required":"")+"'"+`><a class="${n.tabAClass}" href="#`+h+'">'+t.replace("_","-")+"</a></li>"),r.append(l),i.append(u),o.hasClass("errors")&&(c=r.find("li").length-1,l.addClass(n.tabErrorClass))}),a.el[a.insert](i),i.tabs({active:c}),s.push(i)}),s}function u(){e(".mt").parents(".inline-group").not(".tabular").find(".add-row a").click(function(){var o=new s({$fields:e(this).parent().prev().prev().find(".mt").add(e(this).parent().prev(".djn-items").children(".djn-item").last().find(".mt"))}),n=r(o.groupedTranslations);t.update(n),t.activateTab(n)})}a=function(t){this.id=t.id,this.$id=null,this.$table=null,this.translationColumns=[],this.requiredColumns=[],this.init=function(){this.$id=e("#"+this.id),this.$table=e(this.$id).find("table")},this.getAllGroupedTranslations=function(){var e=new s({$fields:this.$table.find(".mt").filter("input, textarea, select")});return this.initTable(),e.groupedTranslations},this.getGroupedTranslations=function(e){var t=new s({$fields:e});return t.groupedTranslations},this.initTable=function(){var t=this,n=new s({$fields:this.$table.find(".mt").filter("input, textarea, select")});this.translationColumns=this.getTranslationColumns(n.groupedTranslations),this.$table.find("th").each(function(n){e.inArray(n+1,t.translationColumns)!==-1&&e(this).hide(),e(this).html()&&e.inArray(n+1,t.translationColumns)===-1&&e(this).html(e(this).html().replace(/ \[.+\]/,""))})},this.getTranslationColumns=function(t){var n=[];return e.each(t,function(t,s){var o=0;e.each(s,function(t,s){var i=e(s).closest("td").prevAll().length;o>0&&e.inArray(i,n)===-1&&n.push(i),o+=1})}),n},this.getRequiredColumns=function(){var t=[];return this.$table.find("th.required").each(function(){t.push(e(this).index()+1)}),t},this.init()};function h(n){n.$table.find(".add-row a").click(function(){var s=c(n.getGroupedTranslations(e(this).parent().parent().prev().prev().find(".mt")));t.update(s),t.activateTab(s)})}function c(t){var s=[];return e.each(t,function(t,o){if(t.includes("__prefix__"))return;var a,i=e("<td></td>"),r=e("<ul></ul>"),c=0;i.append(r),e.each(o,function(t,s){var l,d,u,o=e(s).closest("td"),h="tab_"+e(s).attr("id");a||(a={insert:o.prev().length?"after":o.next().length?"prepend":"append",el:o.prev().length?o.prev():o.parent()}),d=e('<div id="'+h+'"></div>').append(o),l={},e.each(o[0].attributes,function(e,t){l[t.nodeName]=t.nodeValue}),o.replaceWith(function(){return e("<div />",l).append(e(this).contents())}),u=e("<li"+(e(s).hasClass("mt-default")?' class="required"':"")+'><a href="#'+h+'">'+t.replace("_","-")+"</a></li>"),r.append(u),i.append(d),o.hasClass("errors")&&(c=r.find("li").length-1,tab.addClass(n.tabErrorClass))}),a.el[a.insert](i),i.tabs({active:c}),s.push(i)}),s}t={languages:[],$select:e("<select id='modeltranslation-main-switch' class='modeltranslation-switch'>"),init:function(t,s){var o=this;e.each(t,function(t,n){e.each(n,function(t){e.inArray(t,o.languages)<0&&o.languages.push(t)})}),e.each(this.languages,function(t,n){o.$select.append(e('<option value="'+t+'">'+n.replace("_","-")+"</option>"))}),this.update(s),n.mainHeader().append("&nbsp;").append(o.$select)},update:function(t){var n=this;this.$select.change(function(){e.each(t,function(e,t){t.tabs("option","active",parseInt(n.$select.val(),10))})})},activateTab:function(t){var n=this;e.each(t,function(e,t){t.tabs("option","active",parseInt(n.$select.val(),10))})}},e("body").hasClass("change-form")&&(i=new s({$fields:e(".mt").filter("input, textarea, select, iframe, div").filter(":parents(.tabular)").filter(":parents(.empty-form)")}),t.init(i.groupedTranslations,r(i.groupedTranslations)),e(document).ready(function(){u()}),e("div.inline-group > div.tabular").each(function(){var n=new a({id:e(this).parent().attr("id")});t.update(c(n.getAllGroupedTranslations())),e(document).ready(function(){e(window).on("load",function(){h(n)})})}))})})()