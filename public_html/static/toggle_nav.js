let menu_button=document.getElementById("menu_button"),header=document.getElementById("header"),header_height=header.getBoundingClientRect().height+"px";function toggleMenu(){var e=document.getElementById("nav");e.classList.toggle("active_nav"),e.style.top=header_height}menu_button.addEventListener("click",toggleMenu)