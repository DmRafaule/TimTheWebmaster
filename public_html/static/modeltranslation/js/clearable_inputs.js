var $,jQuery,django;(function(){"use strict";(jQuery||$||django.jQuery)(function(e){e(".clearable-input").each(function(){var t=e(this).children().last();e(this).find("input, select, textarea").not(t).change(function(){typeof t.prop=="undefined"?t.removeAttr("checked"):t.prop("checked",!1)})})})})()