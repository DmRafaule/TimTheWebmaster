/*! Select2 4.0.13 | https://github.com/select2/select2/blob/master/LICENSE.md */!function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var e=jQuery.fn.select2.amd;e.define("select2/i18n/ru",[],function(){function e(e,t,n,s){return e%10<5&&e%10>0&&e%100<5||e%100>20?e%10>1?n:t:s}return{errorLoading:function(){return"Невозможно загрузить результаты"},inputTooLong:function(t){var n=t.input.length-t.maximum,s="Пожалуйста, введите на "+n+" символ";return s+=e(n,"","a","ов"),s+=" меньше"},inputTooShort:function(t){var n=t.minimum-t.input.length,s="Пожалуйста, введите ещё хотя бы "+n+" символ";return s+=e(n,"","a","ов")},loadingMore:function(){return"Загрузка данных…"},maximumSelected:function(t){var n="Вы можете выбрать не более "+t.maximum+" элемент";return n+=e(t.maximum,"","a","ов")},noResults:function(){return"Совпадений не найдено"},searching:function(){return"Поиск…"},removeAllItems:function(){return"Удалить все элементы"}}}),e.define,e.require}()