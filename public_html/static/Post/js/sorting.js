function UpdatePosts(e=!0,t="basic"){var s=$(".post_preview").length;$.ajax({type:"GET",url:"load_post_preview/",data:{number:s,offset:0,category:category_name,is_recent:e,mode:t,for_who:""},mode:"same-origin",success:function(e){var t,s,n=$("#page");n.text(""),n.append(e);for(s=n.find(".post_preview"),t=0;t<s.length;t++)$(s[t]).addClass("loader")},error:function(){}})}function onSort(){var s,o,t=$("#onSort"),n=$("#toViews"),e=t.data("sort"),e=!e;t.data("sort",e),s=n.data("view"),o=n.data("who"),UpdatePosts(e,s,o)}function onView(e,t=""){var n=$("#onSort").data("sort"),s=$("#toViews");s.data("view",e),UpdatePosts(n,e,t)}$(document).ready(function(){$("#onSort").on("click",function(){onSort(),$(this).toggleClass("rotate_X")}),$("#onBasicView").on("click",function(){onView("basic"),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")}),$("#onSimpleView").on("click",function(){onView("simple"),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")}),$("#onMinimalView").on("click",function(){onView("minimal"),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")}),$("#onRawView").on("click",function(){onView("raw"),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")}),$("#onNotExtendedView").on("click",function(){var e=$("#toViews").data("who");onView("basic",e),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")}),$("#onExtendedView").on("click",function(){var e=$("#toViews").data("who");onView("extended",e),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")}),$("#onListView").on("click",function(){var e=$("#toViews").data("who");onView("list",e),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")}),$("#onGridView").on("click",function(){var e=$("#toViews").data("who");onView("grid",e),$("#toViews").children().each(function(){$(this).removeClass("selected_view")}),$(this).toggleClass("selected_view")})})