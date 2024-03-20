/*!
 * jQuery JavaScript Library v3.6.0
 * https://jquery.com/
 *
 * Includes Sizzle.js
 * https://sizzlejs.com/
 *
 * Copyright OpenJS Foundation and other contributors
 * Released under the MIT license
 * https://jquery.org/license
 *
 * Date: 2021-03-02T17:08Z
 */(function(e,t){"use strict";typeof module=="object"&&typeof module.exports=="object"?module.exports=e.document?t(e,!0):function(e){if(!e.document)throw new Error("jQuery requires a window with a document");return t(e)}:t(e)})(typeof window!="undefined"?window:this,function(e,t){/*!
 * Sizzle CSS Selector Engine v2.3.6
 * https://sizzlejs.com/
 *
 * Copyright JS Foundation and other contributors
 * Released under the MIT license
 * https://js.foundation/
 *
 * Date: 2021-02-16
 */"use strict";v=[],oe=Object.getPrototypeOf,b=v.slice,ae=v.flat?function(e){return v.flat.call(e)}:function(e){return v.concat.apply([],e)},J=v.push,I=v.indexOf,V={},he=V.toString,W=V.hasOwnProperty,fe=W.toString,yt=fe.call(Object),a={},o=function(t){return typeof t=="function"&&typeof t.nodeType!="number"&&typeof t.item!="function"},_=function(t){return t!=null&&t===t.window},i=e.document,jt={type:!0,src:!0,nonce:!0,noModule:!0};function gt(e,t,n){n=n||i;var s,a,o=n.createElement("script");if(o.text=e,t)for(s in jt)a=t[s]||t.getAttribute&&t.getAttribute(s),a&&o.setAttribute(s,a);n.head.appendChild(o).parentNode.removeChild(o)}function E(e){return e==null?e+"":typeof e=="object"||typeof e=="function"?V[he.call(e)]||"object":typeof e}var s,o,i,a,r,d,m,f,g,v,b,j,y,_,x,C,k,A,S,M,F,z,L,I,B,V,$,W,Y,Q,Z,J,oe,ae,he,fe,yt,jt,ft="3.6.0",n=function(e,t){return new n.fn.init(e,t)},xe,Ce,Ee,Ie,He,Re,et,tt,xt,Ct,Et,Ge,$e,Ae,ot,ue,pe,ge,_t,we,se,Ve,ee,at,rt,pt,vt,bt,wt,be,ve,me,te,Ye,ie,Le,De,ze;n.fn=n.prototype={jquery:ft,constructor:n,length:0,toArray:function(){return b.call(this)},get:function(e){return e==null?b.call(this):e<0?this[e+this.length]:this[e]},pushStack:function(e){var t=n.merge(this.constructor(),e);return t.prevObject=this,t},each:function(e){return n.each(this,e)},map:function(e){return this.pushStack(n.map(this,function(t,n){return e.call(t,n,t)}))},slice:function(){return this.pushStack(b.apply(this,arguments))},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},even:function(){return this.pushStack(n.grep(this,function(e,t){return(t+1)%2}))},odd:function(){return this.pushStack(n.grep(this,function(e,t){return t%2}))},eq:function(e){var n=this.length,t=+e+(e<0?n:0);return this.pushStack(t>=0&&t<n?[this[t]]:[])},end:function(){return this.prevObject||this.constructor()},push:J,sort:v.sort,splice:v.splice},n.extend=n.fn.extend=function(){var t,i,a,r,c,l,e=arguments[0]||{},s=1,u=arguments.length,d=!1;for(typeof e=="boolean"&&(d=e,e=arguments[s]||{},s++),typeof e!="object"&&!o(e)&&(e={}),s===u&&(e=this,s--);s<u;s++)if((l=arguments[s])!=null)for(i in l){if(t=l[i],i==="__proto__"||e===t)continue;d&&t&&(n.isPlainObject(t)||(r=Array.isArray(t)))?(a=e[i],r&&!Array.isArray(a)?c=[]:!r&&!n.isPlainObject(a)?c={}:c=a,r=!1,e[i]=n.extend(d,c,t)):t!==void 0&&(e[i]=t)}return e},n.extend({expando:"jQuery"+(ft+Math.random()).replace(/\D/g,""),isReady:!0,error:function(e){throw new Error(e)},noop:function(){},isPlainObject:function(e){var t,n;return!!e&&he.call(e)==="[object Object]"&&(t=oe(e),!t||(n=W.call(t,"constructor")&&t.constructor,typeof n=="function"&&fe.call(n)===yt))},isEmptyObject:function(e){var t;for(t in e)return!1;return!0},globalEval:function(e,t,n){gt(e,{nonce:t&&t.nonce},n)},each:function(e,t){var s,n=0;if(_e(e)){for(s=e.length;n<s;n++)if(t.call(e[n],n,e[n])===!1)break}else for(n in e)if(t.call(e[n],n,e[n])===!1)break;return e},makeArray:function(e,t){var s=t||[];return e!=null&&(_e(Object(e))?n.merge(s,typeof e=="string"?[e]:e):J.call(s,e)),s},inArray:function(e,t,n){return t==null?-1:I.call(t,e,n)},merge:function(e,t){for(var o=+t.length,n=0,s=e.length;n<o;n++)e[s++]=t[n];return e.length=s,e},grep:function(e,t,n){for(var o,i=[],s=0,a=e.length,r=!n;s<a;s++)o=!t(e[s],s),o!==r&&i.push(e[s]);return i},map:function(e,t,n){var o,a,s=0,i=[];if(_e(e))for(a=e.length;s<a;s++)o=t(e[s],s,n),o!=null&&i.push(o);else for(s in e)o=t(e[s],s,n),o!=null&&i.push(o);return ae(i)},guid:1,support:a}),typeof Symbol=="function"&&(n.fn[Symbol.iterator]=v[Symbol.iterator]),n.each("Boolean Number String Function Array Date RegExp Object Error Symbol".split(" "),function(e,t){V["[object "+t+"]"]=t.toLowerCase()});function _e(e){var t=!!e&&"length"in e&&e.length,n=E(e);return!o(e)&&!_(e)&&(n==="array"||t===0||typeof t=="number"&&t>0&&t-1 in e)}j=function(e){var t,n,i,r,c,l,v,b,j,x,C,E,k,F,T,z,U,ae,ce,a="sizzle"+1*new Date,u=e.document,m=0,ue=0,Z=S(),ne=S(),ee=S(),N=S(),q=function(e,t){return e===t&&(C=!0),0},Oe={}.hasOwnProperty,y=[],Ce=y.pop,xe=y.push,g=y.push,X=y.slice,O=function(e,t){for(var n=0,s=e.length;n<s;n++)if(e[n]===t)return n;return-1},K="checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",s=`[\\x20\\t\\r\\n\\f]`,_="(?:\\\\[\\da-fA-F]{1,6}"+s+`?|\\\\[^\\r\\n\\f]|[\\w-]|[^\0-\\x7f])+`,re="\\["+s+"*("+_+")(?:"+s+"*([*^$|!~]?=)"+s+`*(?:'((?:\\\\.|[^\\\\'])*)'|"((?:\\\\.|[^\\\\"])*)"|(`+_+"))|)"+s+"*\\]",W=":("+_+`)(?:\\((('((?:\\\\.|[^\\\\'])*)'|"((?:\\\\.|[^\\\\"])*)")|((?:\\\\.|[^\\\\()[\\]]|`+re+")*)|.*)\\)|)",le=new RegExp(s+"+","g"),P=new RegExp("^"+s+"+|((?:^|[^\\\\])(?:\\\\.)*)"+s+"+$","g"),_e=new RegExp("^"+s+"*,"+s+"*"),G=new RegExp("^"+s+"*([>+~]|"+s+")"+s+"*"),ye=new RegExp(s+"|>"),je=new RegExp(W),be=new RegExp("^"+_+"$"),D={ID:new RegExp("^#("+_+")"),CLASS:new RegExp("^\\.("+_+")"),TAG:new RegExp("^("+_+"|[*])"),ATTR:new RegExp("^"+re),PSEUDO:new RegExp("^"+W),CHILD:new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\("+s+"*(even|odd|(([+-]|)(\\d*)n|)"+s+"*(?:([+-]|)"+s+"*(\\d+)|))"+s+"*\\)|)","i"),bool:new RegExp("^(?:"+K+")$","i"),needsContext:new RegExp("^"+s+"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\("+s+"*((?:-\\d)?\\d*)"+s+"*\\)|)(?=[^-]|$)","i")},ve=/HTML$/i,ge=/^(?:input|select|textarea|button)$/i,pe=/^h\d$/i,A=/^[^{]+\{\s*\[native \w/,he=/^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,H=/[+~]/,f=new RegExp("\\\\[\\da-fA-F]{1,6}"+s+`?|\\\\([^\\r\\n\\f])`,"g"),p=function(e,t){var n="0x"+e.slice(1)-65536;return t?t:n<0?String.fromCharCode(n+65536):String.fromCharCode(n>>10|55296,n&1023|56320)},ie=/([\0-\x1f\x7f]|^-?\d)|^-$|[^\0-\x1f\x7f-\uFFFF\w-]/g,oe=function(e,t){return t?e==="\0"?"�":e.slice(0,-1)+"\\"+e.charCodeAt(e.length-1).toString(16)+" ":"\\"+e},se=function(){b()},de=R(function(e){return e.disabled===!0&&e.nodeName.toLowerCase()==="fieldset"},{dir:"parentNode",next:"legend"});try{g.apply(y=X.call(u.childNodes),u.childNodes),y[u.childNodes.length].nodeType}catch{g={apply:y.length?function(e,t){xe.apply(e,X.call(t))}:function(e,t){for(var n=e.length,s=0;e[n++]=t[s++];);e.length=n-1}}}function o(e,t,s,o){var c,d,u,f,p,v,j,m=t&&t.ownerDocument,h=t?t.nodeType:9;if(s=s||[],typeof e!="string"||!e||h!==1&&h!==9&&h!==11)return s;if(!o&&(b(t),t=t||n,l)){if(h!==11&&(v=he.exec(e)))if(c=v[1]){if(h===9)if(d=t.getElementById(c)){if(d.id===c)return s.push(d),s}else return s;else if(m&&(d=m.getElementById(c))&&k(t,d)&&d.id===c)return s.push(d),s}else if(v[2])return g.apply(s,t.getElementsByTagName(e)),s;else if((c=v[3])&&i.getElementsByClassName&&t.getElementsByClassName)return g.apply(s,t.getElementsByClassName(c)),s;if(i.qsa&&!N[e+" "]&&(!r||!r.test(e))&&(h!==1||t.nodeName.toLowerCase()!=="object")){if(j=e,m=t,h===1&&(ye.test(e)||G.test(e))){for(m=H.test(e)&&Y(t.parentNode)||t,(m!==t||!i.scope)&&((u=t.getAttribute("id"))?u=u.replace(ie,oe):t.setAttribute("id",u=a)),f=E(e),p=f.length;p--;)f[p]=(u?"#"+u:":scope")+" "+L(f[p]);j=f.join(",")}try{return g.apply(s,m.querySelectorAll(j)),s}catch{N(e,!0)}finally{u===a&&t.removeAttribute("id")}}}return ce(e.replace(P,"$1"),t,s,o)}function S(){var n=[];function e(s,o){return n.push(s+" ")>t.cacheLength&&delete e[n.shift()],e[s+" "]=o}return e}function h(e){return e[a]=!0,e}function d(e){var t=n.createElement("fieldset");try{return!!e(t)}catch{return!1}finally{t.parentNode&&t.parentNode.removeChild(t),t=null}}function I(e,n){for(var s=e.split("|"),o=s.length;o--;)t.attrHandle[s[o]]=n}function J(e,t){var n=t&&e,s=n&&e.nodeType===1&&t.nodeType===1&&e.sourceIndex-t.sourceIndex;if(s)return s;if(n)for(;n=n.nextSibling;)if(n===t)return-1;return e?1:-1}function me(e){return function(t){var n=t.nodeName.toLowerCase();return n==="input"&&t.type===e}}function fe(e){return function(t){var n=t.nodeName.toLowerCase();return(n==="input"||n==="button")&&t.type===e}}function Q(e){return function(t){return"form"in t?t.parentNode&&t.disabled===!1?"label"in t?"label"in t.parentNode?t.parentNode.disabled===e:t.disabled===e:t.isDisabled===e||t.isDisabled!==!e&&de(t)===e:t.disabled===e:"label"in t&&t.disabled===e}}function w(e){return h(function(t){return t=+t,h(function(n,s){for(var o,i=e([],n.length,t),a=i.length;a--;)n[o=i[a]]&&(n[o]=!(s[o]=n[o]))})})}function Y(e){return e&&typeof e.getElementsByTagName!="undefined"&&e}i=o.support={},ae=o.isXML=function(e){var n=e&&e.namespaceURI,t=e&&(e.ownerDocument||e).documentElement;return!ve.test(n||t&&t.nodeName||"HTML")},b=o.setDocument=function(e){var o,m,h=e?e.ownerDocument||e:u;return h==n||h.nodeType!==9||!h.documentElement?n:(n=h,c=n.documentElement,l=!ae(n),u!=n&&(o=n.defaultView)&&o.top!==o&&(o.addEventListener?o.addEventListener("unload",se,!1):o.attachEvent&&o.attachEvent("onunload",se)),i.scope=d(function(e){return c.appendChild(e).appendChild(n.createElement("div")),typeof e.querySelectorAll!="undefined"&&!e.querySelectorAll(":scope fieldset div").length}),i.attributes=d(function(e){return e.className="i",!e.getAttribute("className")}),i.getElementsByTagName=d(function(e){return e.appendChild(n.createComment("")),!e.getElementsByTagName("*").length}),i.getElementsByClassName=A.test(n.getElementsByClassName),i.getById=d(function(e){return c.appendChild(e).id=a,!n.getElementsByName||!n.getElementsByName(a).length}),i.getById?(t.filter.ID=function(e){var t=e.replace(f,p);return function(e){return e.getAttribute("id")===t}},t.find.ID=function(e,t){if(typeof t.getElementById!="undefined"&&l){var n=t.getElementById(e);return n?[n]:[]}}):(t.filter.ID=function(e){var t=e.replace(f,p);return function(e){var n=typeof e.getAttributeNode!="undefined"&&e.getAttributeNode("id");return n&&n.value===t}},t.find.ID=function(e,t){if(typeof t.getElementById!="undefined"&&l){var n,o,i,s=t.getElementById(e);if(s){if(n=s.getAttributeNode("id"),n&&n.value===e)return[s];for(i=t.getElementsByName(e),o=0;s=i[o++];)if(n=s.getAttributeNode("id"),n&&n.value===e)return[s]}return[]}}),t.find.TAG=i.getElementsByTagName?function(e,t){if(typeof t.getElementsByTagName!="undefined")return t.getElementsByTagName(e);if(i.qsa)return t.querySelectorAll(e)}:function(e,t){var n,s=[],i=0,o=t.getElementsByTagName(e);if(e==="*"){for(;n=o[i++];)n.nodeType===1&&s.push(n);return s}return o},t.find.CLASS=i.getElementsByClassName&&function(e,t){if(typeof t.getElementsByClassName!="undefined"&&l)return t.getElementsByClassName(e)},j=[],r=[],(i.qsa=A.test(n.querySelectorAll))&&(d(function(e){var t;c.appendChild(e).innerHTML="<a id='"+a+"'></a><select id='"+a+`-
`):t)),s};var At=/\[\]$/,nt=/\r?\n/g,Mt=/^(?:submit|button|image|reset|file)$/i,Ft=/^(?:input|select|textarea|keygen)/i;function de(e,t,s,o){var i;if(Array.isArray(t))n.each(t,function(t,n){s||At.test(e)?o(e,n):de(e+"["+(typeof n=="object"&&n!=null?t:"")+"]",n,s,o)});else if(!s&&E(t)==="object")for(i in t)de(e+"["+i+"]",t[i],s,o);else o(e,t)}n.param=function(e,t){var s,i=[],a=function(e,t){var n=o(t)?t():t;i[i.length]=encodeURIComponent(e)+"="+encodeURIComponent(n??"")};if(e==null)return"";if(Array.isArray(e)||e.jquery&&!n.isPlainObject(e))n.each(e,function(){a(this.name,this.value)});else for(s in e)de(s,e[s],t,a);return i.join("&")},n.fn.extend({serialize:function(){return n.param(this.serializeArray())},serializeArray:function(){return this.map(function(){var e=n.prop(this,"elements");return e?n.makeArray(e):this}).filter(function(){var e=this.type;return this.name&&!n(this).is(":disabled")&&Ft.test(this.nodeName)&&!Mt.test(e)&&(this.checked||!S.test(e))}).map(function(e,t){var s=n(this).val();return s==null?null:Array.isArray(s)?n.map(s,function(e){return{name:t.name,value:e.replace(nt,`
`)}}):{name:t.name,value:s.replace(nt,`
`)}}).get()}});var zt=/%20/g,Dt=/#.*$/,Nt=/([?&])_=[^&]*/,Lt=/^(.*?):[ \t]*([^\r\n]*)$/mg,Rt=/^(?:about|app|app-storage|.+-extension|file|res|widget):$/,Pt=/^(?:GET|HEAD)$/,Ht=/^\/\//,ht={},le={},ct="*/".concat("*"),ce=i.createElement("a");ce.href=A.href;function st(e){return function(t,n){typeof t!="string"&&(n=t,t="*");var s,i=0,a=t.toLowerCase().match(m)||[];if(o(n))for(;s=a[i++];)s[0]==="+"?(s=s.slice(1)||"*",(e[s]=e[s]||[]).unshift(n)):(e[s]=e[s]||[]).push(n)}}function Ze(e,t,s,o){var i={},r=e===le;function a(c){var l;return i[c]=!0,n.each(e[c]||[],function(e,n){var c=n(t,s,o);if(typeof c=="string"&&!r&&!i[c])return t.dataTypes.unshift(c),a(c),!1;if(r)return!(l=c)}),l}return a(t.dataTypes[0])||!i["*"]&&a("*")}function re(e,t){var s,o,i=n.ajaxSettings.flatOptions||{};for(s in t)t[s]!==void 0&&((i[s]?e:o||(o={}))[s]=t[s]);return o&&n.extend(!0,e,o),e}function qt(e,t,n){for(var o,i,a,r,c=e.contents,s=e.dataTypes;s[0]==="*";)s.shift(),a===void 0&&(a=e.mimeType||t.getResponseHeader("Content-Type"));if(a)for(o in c)if(c[o]&&c[o].test(a)){s.unshift(o);break}if(s[0]in n)i=s[0];else{for(o in n){if(!s[0]||e.converters[o+" "+s[0]]){i=o;break}r||(r=o)}i=i||r}if(i)return i!==s[0]&&s.unshift(i),n[i]}function Yt(e,t,n,s){var o,i,a,c,l,r={},d=e.dataTypes.slice();if(d[1])for(i in e.converters)r[i.toLowerCase()]=e.converters[i];for(o=d.shift();o;)if(e.responseFields[o]&&(n[e.responseFields[o]]=t),!a&&s&&e.dataFilter&&(t=e.dataFilter(t,e.dataType)),a=o,o=d.shift(),o)if(o==="*")o=a;else if(a!=="*"&&a!==o){if(i=r[a+" "+o]||r["* "+o],!i)for(l in r)if(c=l.split(" "),c[1]===o&&(i=r[a+" "+c[0]]||r["* "+c[0]],i)){i===!0?i=r[l]:r[l]!==!0&&(o=c[0],d.unshift(c[1]));break}if(i!==!0)if(i&&e.throws)t=i(t);else try{t=i(t)}catch(e){return{state:"parsererror",error:i?e:"No conversion from "+a+" to "+o}}}return{state:"success",data:t}}return n.extend({active:0,lastModified:{},etag:{},ajaxSettings:{url:A.href,type:"GET",isLocal:Rt.test(A.protocol),global:!0,processData:!0,async:!0,contentType:"application/x-www-form-urlencoded; charset=UTF-8",accepts:{"*":ct,text:"text/plain",html:"text/html",xml:"application/xml, text/xml",json:"application/json, text/javascript"},contents:{xml:/\bxml\b/,html:/\bhtml/,json:/\bjson\b/},responseFields:{xml:"responseXML",text:"responseText",json:"responseJSON"},converters:{"* text":String,"text html":!0,"text json":JSON.parse,"text xml":n.parseXML},flatOptions:{url:!0,context:!0}},ajaxSetup:function(e,t){return t?re(re(e,n.ajaxSettings),t):re(n.ajaxSettings,e)},ajaxPrefilter:st(ht),ajaxTransport:st(le),ajax:function(t,s){typeof t=="object"&&(s=t,t=void 0),s=s||{};var r,c,d,u,h,f,g,b,_,w,o=n.ajaxSetup({},s),l=o.context||o,j=o.context&&(l.nodeType||l.jquery)?n(l):n.event,y=n.Deferred(),O=n.Callbacks("once memory"),p=o.statusCode||{},x={},C={},E="canceled",a={readyState:0,getResponseHeader:function(e){if(c){if(!h){h={};for(var t;t=Lt.exec(w);)h[t[1].toLowerCase()+" "]=(h[t[1].toLowerCase()+" "]||[]).concat(t[2])}t=h[e.toLowerCase()+" "]}return t==null?null:t.join(", ")},getAllResponseHeaders:function(){return c?w:null},setRequestHeader:function(e,t){return c==null&&(e=C[e.toLowerCase()]=C[e.toLowerCase()]||e,x[e]=t),this},overrideMimeType:function(e){return c==null&&(o.mimeType=e),this},statusCode:function(e){var t;if(e)if(c)a.always(e[a.status]);else for(t in e)p[t]=[p[t],e[t]];return this},abort:function(e){var t=e||E;return u&&u.abort(t),v(0,t),this}};if(y.promise(a),o.url=((t||o.url||A.href)+"").replace(Ht,A.protocol+"//"),o.type=s.method||s.type||o.method||o.type,o.dataTypes=(o.dataType||"*").toLowerCase().match(m)||[""],o.crossDomain==null){d=i.createElement("a");try{d.href=o.url,d.href=d.href,o.crossDomain=ce.protocol+"//"+ce.host!==d.protocol+"//"+d.host}catch{o.crossDomain=!0}}if(o.data&&o.processData&&typeof o.data!="string"&&(o.data=n.param(o.data,o.traditional)),Ze(ht,o,s,a),c)return a;f=n.event&&o.global,f&&n.active++===0&&n.event.trigger("ajaxStart"),o.type=o.type.toUpperCase(),o.hasContent=!Pt.test(o.type),r=o.url.replace(Dt,""),o.hasContent?o.data&&o.processData&&(o.contentType||"").indexOf("application/x-www-form-urlencoded")===0&&(o.data=o.data.replace(zt,"+")):(g=o.url.slice(r.length),o.data&&(o.processData||typeof o.data=="string")&&(r+=(te.test(r)?"&":"?")+o.data,delete o.data),o.cache===!1&&(r=r.replace(Nt,"$1"),g=(te.test(r)?"&":"?")+"_="+me.guid+++g),o.url=r+g),o.ifModified&&(n.lastModified[r]&&a.setRequestHeader("If-Modified-Since",n.lastModified[r]),n.etag[r]&&a.setRequestHeader("If-None-Match",n.etag[r])),(o.data&&o.hasContent&&o.contentType!==!1||s.contentType)&&a.setRequestHeader("Content-Type",o.contentType),a.setRequestHeader("Accept",o.dataTypes[0]&&o.accepts[o.dataTypes[0]]?o.accepts[o.dataTypes[0]]+(o.dataTypes[0]!=="*"?", "+ct+"; q=0.01":""):o.accepts["*"]);for(_ in o.headers)a.setRequestHeader(_,o.headers[_]);if(o.beforeSend&&(o.beforeSend.call(l,a,o)===!1||c))return a.abort();if(E="abort",O.add(o.complete),a.done(o.success),a.fail(o.error),u=Ze(le,o,s,a),u){if(a.readyState=1,f&&j.trigger("ajaxSend",[a,o]),c)return a;o.async&&o.timeout>0&&(b=e.setTimeout(function(){a.abort("timeout")},o.timeout));try{c=!1,u.send(x,v)}catch(e){if(c)throw e;v(-1,e)}}else v(-1,"No Transport");function v(t,s,i,d){var m,g,v,_,x,h=s;if(c)return;c=!0,b&&e.clearTimeout(b),u=void 0,w=d||"",a.readyState=t>0?4:0,m=t>=200&&t<300||t===304,i&&(g=qt(o,a,i)),!m&&n.inArray("script",o.dataTypes)>-1&&n.inArray("json",o.dataTypes)<0&&(o.converters["text script"]=function(){}),g=Yt(o,g,a,m),m?(o.ifModified&&(v=a.getResponseHeader("Last-Modified"),v&&(n.lastModified[r]=v),v=a.getResponseHeader("etag"),v&&(n.etag[r]=v)),t===204||o.type==="HEAD"?h="nocontent":t===304?h="notmodified":(h=g.state,x=g.data,_=g.error,m=!_)):(_=h,(t||!h)&&(h="error",t<0&&(t=0))),a.status=t,a.statusText=(s||h)+"",m?y.resolveWith(l,[x,h,a]):y.rejectWith(l,[a,h,_]),a.statusCode(p),p=void 0,f&&j.trigger(m?"ajaxSuccess":"ajaxError",[a,o,m?x:_]),O.fireWith(l,[a,h]),f&&(j.trigger("ajaxComplete",[a,o]),--n.active||n.event.trigger("ajaxStop"))}return a},getJSON:function(e,t,s){return n.get(e,t,s,"json")},getScript:function(e,t){return n.get(e,void 0,t,"script")}}),n.each(["get","post"],function(e,t){n[t]=function(e,s,i,a){return o(s)&&(a=a||i,i=s,s=void 0),n.ajax(n.extend({url:e,type:t,dataType:a,data:s,success:i},n.isPlainObject(e)&&e))}}),n.ajaxPrefilter(function(e){var t;for(t in e.headers)t.toLowerCase()==="content-type"&&(e.contentType=e.headers[t]||"")}),n._evalUrl=function(e,t,s){return n.ajax({url:e,type:"GET",dataType:"script",cache:!0,async:!1,global:!1,converters:{"text script":function(){}},dataFilter:function(e){n.globalEval(e,t,s)}})},n.fn.extend({wrapAll:function(e){var t;return this[0]&&(o(e)&&(e=e.call(this[0])),t=n(e,this[0].ownerDocument).eq(0).clone(!0),this[0].parentNode&&t.insertBefore(this[0]),t.map(function(){for(var e=this;e.firstElementChild;)e=e.firstElementChild;return e}).append(this)),this},wrapInner:function(e){return o(e)?this.each(function(t){n(this).wrapInner(e.call(this,t))}):this.each(function(){var t=n(this),s=t.contents();s.length?s.wrapAll(e):t.append(e)})},wrap:function(e){var t=o(e);return this.each(function(s){n(this).wrapAll(t?e.call(this,s):e)})},unwrap:function(e){return this.parent(e).not("body").each(function(){n(this).replaceWith(this.childNodes)}),this}}),n.expr.pseudos.hidden=function(e){return!n.expr.pseudos.visible(e)},n.expr.pseudos.visible=function(e){return!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length)},n.ajaxSettings.xhr=function(){try{return new e.XMLHttpRequest}catch{}},Ye={0:200,1223:204},F=n.ajaxSettings.xhr(),a.cors=!!F&&"withCredentials"in F,a.ajax=F=!!F,n.ajaxTransport(function(t){var n,s;if(a.cors||F&&!t.crossDomain)return{send:function(o,i){var r,a=t.xhr();if(a.open(t.type,t.url,t.async,t.username,t.password),t.xhrFields)for(r in t.xhrFields)a[r]=t.xhrFields[r];t.mimeType&&a.overrideMimeType&&a.overrideMimeType(t.mimeType),!t.crossDomain&&!o["X-Requested-With"]&&(o["X-Requested-With"]="XMLHttpRequest");for(r in o)a.setRequestHeader(r,o[r]);n=function(e){return function(){n&&(n=s=a.onload=a.onerror=a.onabort=a.ontimeout=a.onreadystatechange=null,e==="abort"?a.abort():e==="error"?typeof a.status!="number"?i(0,"error"):i(a.status,a.statusText):i(Ye[a.status]||a.status,a.statusText,(a.responseType||"text")!=="text"||typeof a.responseText!="string"?{binary:a.response}:{text:a.responseText},a.getAllResponseHeaders()))}},a.onload=n(),s=a.onerror=a.ontimeout=n("error"),a.onabort!==void 0?a.onabort=s:a.onreadystatechange=function(){a.readyState===4&&e.setTimeout(function(){n&&s()})},n=n("abort");try{a.send(t.hasContent&&t.data||null)}catch(e){if(n)throw e}},abort:function(){n&&n()}}}),n.ajaxPrefilter(function(e){e.crossDomain&&(e.contents.script=!1)}),n.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/\b(?:java|ecma)script\b/},converters:{"text script":function(e){return n.globalEval(e),e}}}),n.ajaxPrefilter("script",function(e){e.cache===void 0&&(e.cache=!1),e.crossDomain&&(e.type="GET")}),n.ajaxTransport("script",function(e){if(e.crossDomain||e.scriptAttrs){var t,s;return{send:function(o,a){s=n("<script>").attr(e.scriptAttrs||{}).prop({charset:e.scriptCharset,src:e.url}).on("load error",t=function(e){s.remove(),t=null,e&&a(e.type==="error"?404:200,e.type)}),i.head.appendChild(s[0])},abort:function(){t&&t()}}}}),ie=[],Z=/(=)\?(?=&|$)|\?\?/,n.ajaxSetup({jsonp:"callback",jsonpCallback:function(){var e=ie.pop()||n.expando+"_"+me.guid++;return this[e]=!0,e}}),n.ajaxPrefilter("json jsonp",function(t,s,i){var a,r,c,l=t.jsonp!==!1&&(Z.test(t.url)?"url":typeof t.data=="string"&&(t.contentType||"").indexOf("application/x-www-form-urlencoded")===0&&Z.test(t.data)&&"data");if(l||t.dataTypes[0]==="jsonp")return a=t.jsonpCallback=o(t.jsonpCallback)?t.jsonpCallback():t.jsonpCallback,l?t[l]=t[l].replace(Z,"$1"+a):t.jsonp!==!1&&(t.url+=(te.test(t.url)?"&":"?")+t.jsonp+"="+a),t.converters["script json"]=function(){return c||n.error(a+" was not called"),c[0]},t.dataTypes[0]="json",r=e[a],e[a]=function(){c=arguments},i.always(function(){r===void 0?n(e).removeProp(a):e[a]=r,t[a]&&(t.jsonpCallback=s.jsonpCallback,ie.push(a)),c&&o(r)&&r(c[0]),c=r=void 0}),"script"}),a.createHTMLDocument=function(){var e=i.implementation.createHTMLDocument("").body;return e.innerHTML="<form></form><form></form>",e.childNodes.length===2}(),n.parseHTML=function(e,t,s){if(typeof e!="string")return[];typeof t=="boolean"&&(s=t,t=!1);var o,r,c;return t||(a.createHTMLDocument?(t=i.implementation.createHTMLDocument(""),c=t.createElement("base"),c.href=i.location.href,t.head.appendChild(c)):t=i),o=Ee.exec(e),r=!s&&[],o?[t.createElement(o[1])]:(o=dt([e],t,r),r&&r.length&&n(r).remove(),n.merge([],o.childNodes))},n.fn.load=function(e,t,s){var i,c,l,a=this,r=e.indexOf(" ");return r>-1&&(i=w(e.slice(r)),e=e.slice(0,r)),o(t)?(s=t,t=void 0):t&&typeof t=="object"&&(c="POST"),a.length>0&&n.ajax({url:e,type:c||"GET",dataType:"html",data:t}).done(function(e){l=arguments,a.html(i?n("<div>").append(n.parseHTML(e)).find(i):e)}).always(s&&function(e,t){a.each(function(){s.apply(this,l||[e.responseText,t,e])})}),this},n.expr.pseudos.animated=function(e){return n.grep(n.timers,function(t){return e===t.elem}).length},n.offset={setOffset:function(e,t,s){var i,r,c,l,d,u,f,h=n.css(e,"position"),m=n(e),a={};h==="static"&&(e.style.position="relative"),i=m.offset(),l=n.css(e,"top"),u=n.css(e,"left"),f=(h==="absolute"||h==="fixed")&&(l+u).indexOf("auto")>-1,f?(r=m.position(),d=r.top,c=r.left):(d=parseFloat(l)||0,c=parseFloat(u)||0),o(t)&&(t=t.call(e,s,n.extend({},i))),t.top!=null&&(a.top=t.top-i.top+d),t.left!=null&&(a.left=t.left-i.left+c),"using"in t?t.using.call(e,a):m.css(a)}},n.fn.extend({offset:function(e){if(arguments.length)return e===void 0?this:this.each(function(t){n.offset.setOffset(this,e,t)});var s,o,t=this[0];if(!t)return;return t.getClientRects().length?(s=t.getBoundingClientRect(),o=t.ownerDocument.defaultView,{top:s.top+o.pageYOffset,left:s.left+o.pageXOffset}):{top:0,left:0}},position:function(){if(!this[0])return;var e,o,i,t=this[0],s={top:0,left:0};if(n.css(t,"position")==="fixed")o=t.getBoundingClientRect();else{for(o=this.offset(),i=t.ownerDocument,e=t.offsetParent||i.documentElement;e&&(e===i.body||e===i.documentElement)&&n.css(e,"position")==="static";)e=e.parentNode;e&&e!==t&&e.nodeType===1&&(s=n(e).offset(),s.top+=n.css(e,"borderTopWidth",!0),s.left+=n.css(e,"borderLeftWidth",!0))}return{top:o.top-s.top-n.css(t,"marginTop",!0),left:o.left-s.left-n.css(t,"marginLeft",!0)}},offsetParent:function(){return this.map(function(){for(var e=this.offsetParent;e&&n.css(e,"position")==="static";)e=e.offsetParent;return e||y})}}),n.each({scrollLeft:"pageXOffset",scrollTop:"pageYOffset"},function(e,t){var s="pageYOffset"===t;n.fn[e]=function(n){return g(this,function(e,n,o){var i;if(_(e)?i=e:e.nodeType===9&&(i=e.defaultView),o===void 0)return i?i[t]:e[n];i?i.scrollTo(s?i.pageXOffset:o,s?o:i.pageYOffset):e[n]=o},e,n,arguments.length)}}),n.each(["top","left"],function(e,t){n.cssHooks[t]=We(a.pixelPosition,function(e,s){if(s)return s=U(e,t),Q.test(s)?n(e).position()[t]+"px":s})}),n.each({Height:"height",Width:"width"},function(e,t){n.each({padding:"inner"+e,content:t,"":"outer"+e},function(s,o){n.fn[o]=function(i,a){var r=arguments.length&&(s||typeof i!="boolean"),c=s||(i===!0||a===!0?"margin":"border");return g(this,function(t,s,i){var a;return _(t)?o.indexOf("outer")===0?t["inner"+e]:t.document.documentElement["client"+e]:t.nodeType===9?(a=t.documentElement,Math.max(t.body["scroll"+e],a["scroll"+e],t.body["offset"+e],a["offset"+e],a["client"+e])):i===void 0?n.css(t,s,c):n.style(t,s,i,c)},t,r?i:void 0,r)}})}),n.each(["ajaxStart","ajaxStop","ajaxComplete","ajaxError","ajaxSuccess","ajaxSend"],function(e,t){n.fn[t]=function(e){return this.on(t,e)}}),n.fn.extend({bind:function(e,t,n){return this.on(e,null,t,n)},unbind:function(e,t){return this.off(e,null,t)},delegate:function(e,t,n,s){return this.on(t,e,n,s)},undelegate:function(e,t,n){return arguments.length===1?this.off(e,"**"):this.off(t,e||"**",n)},hover:function(e,t){return this.mouseenter(e).mouseleave(t||e)}}),n.each(("blur focus focusin focusout resize scroll click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup contextmenu").split(" "),function(e,t){n.fn[t]=function(e,n){return arguments.length>0?this.on(t,null,e,n):this.trigger(t)}}),Le=/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,n.proxy=function(e,t){var s,i,a;return typeof t=="string"&&(i=e[t],t=e,e=i),o(e)?(a=b.call(arguments,2),s=function(){return e.apply(t||this,a.concat(b.call(arguments)))},s.guid=e.guid=e.guid||n.guid++,s):void 0},n.holdReady=function(e){e?n.readyWait++:n.ready(!0)},n.isArray=Array.isArray,n.parseJSON=JSON.parse,n.nodeName=u,n.isFunction=o,n.isWindow=_,n.camelCase=p,n.type=E,n.now=Date.now,n.isNumeric=function(e){var t=n.type(e);return(t==="number"||t==="string")&&!isNaN(e-parseFloat(e))},n.trim=function(e){return e==null?"":(e+"").replace(Le,"")},typeof define=="function"&&define.amd&&define("jquery",[],function(){return n}),De=e.jQuery,ze=e.$,n.noConflict=function(t){return e.$===n&&(e.$=ze),t&&e.jQuery===n&&(e.jQuery=De),n},typeof t=="undefined"&&(e.jQuery=e.$=n),n})