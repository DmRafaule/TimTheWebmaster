const number=5;var offset=0;function LoadPosts(e=!0,t="basic"){$.ajax({type:"GET",url:"load_post_preview/",data:{number,offset,category:category_name,is_recent:e,mode:t,for_who:""},mode:"same-origin",success:function(e){var t=$("#page");t.append(e),offset=offset+number},error:function(){}})}$(document).ready(function(){var e=$("#toViews"),s=e.data("view"),o=e.data("who"),i=$("#onSort").data("sort");const t=new IntersectionObserver((e)=>{for(const t of e)if(t.isIntersecting){var n=$("#toViews"),s=n.data("view"),o=n.data("who"),i=$("#onSort").data("sort");LoadPosts(i,s,o)}}),n=document.querySelector("#scroll-sentinel");t.observe(n)})