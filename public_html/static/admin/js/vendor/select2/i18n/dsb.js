/*! Select2 4.0.13 | https://github.com/select2/select2/blob/master/LICENSE.md */!function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var e=jQuery.fn.select2.amd;e.define("select2/i18n/dsb",[],function(){var t=["znamuško","znamušce","znamuška","znamuškow"],n=["zapisk","zapiska","zapiski","zapiskow"],e=function(e,t){return 1===e?t[0]:2===e?t[1]:e>2&&e<=4?t[2]:e>=5?t[3]:void 0};return{errorLoading:function(){return"Wuslědki njejsu se dali zacytaś."},inputTooLong:function(n){var s=n.input.length-n.maximum;return"Pšosym lašuj "+s+" "+e(s,t)},inputTooShort:function(n){var s=n.minimum-n.input.length;return"Pšosym zapódaj nanejmjenjej "+s+" "+e(s,t)},loadingMore:function(){return"Dalšne wuslědki se zacytaju…"},maximumSelected:function(t){return"Móžoš jano "+t.maximum+" "+e(t.maximum,n)+"wubraś."},noResults:function(){return"Žedne wuslědki namakane"},searching:function(){return"Pyta se…"},removeAllItems:function(){return"Remove all items"}}}),e.define,e.require}()