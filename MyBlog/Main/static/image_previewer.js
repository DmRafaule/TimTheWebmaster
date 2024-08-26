var drag = false

// Insert exit button on page
function addExit(img){
    var exit_btn_img = document.createElement('img')
    exit_btn_img.src = `${PATH}close_white.svg`
    exit_btn_img.classList.add('icon')
    exit_btn_img.classList.add('button')
    exit_btn_img.classList.add('dynamic_image')
    exit_btn_img.classList.add('squered_button')
    exit_btn_img.classList.add('loader')
    var exit_btn = document.createElement('div')
    exit_btn.classList.add('header_button')
    exit_btn.addEventListener('click',()=>{
        outImage(img)
        exit_btn.remove()
    })
    exit_btn.insertAdjacentElement('afterbegin',exit_btn_img)
    var header_btns = document.querySelectorAll('.header_button') 
    var last_header_btn = header_btns[header_btns.length - 1]
    last_header_btn.insertAdjacentElement('afterend',exit_btn)
}

function zoomIn( e ){
    var targ = document.querySelector('.image_zoomable');
    const transform = getComputedStyle(targ).getPropertyValue('transform')
    targ.style.transform = `${transform} scale(1.5)`
}

function zoomOut( e ){
    var targ = document.querySelector('.image_zoomable');
    const transform = getComputedStyle(targ).getPropertyValue('transform')
    targ.style.transform = `${transform} scale(0.5)`
}

// Insert zoom buttons on page
function addZoom(){
    var zoom_container = document.createElement('div')
    zoom_container.id = 'zoom_buttons'
    zoom_container.classList.add('column')
    zoom_container.classList.add('flex-nowrap')
    zoom_container.classList.add('mid_gap')
    zoom_container.classList.add('marger_mid')
    zoom_container.classList.add('is_fixed')
    zoom_container.classList.add('b-l')
    zoom_container.classList.add('zIndPl3')
    zoom_container.classList.add('padder')

    var zoom_in_img = document.createElement('img')
    zoom_in_img.src = `${PATH}zoom_in.svg`
    zoom_in_img.classList.add('icon')
    zoom_in_img.classList.add('button')
    zoom_in_img.classList.add('dynamic_image')
    zoom_in_img.classList.add('squered_button')
    zoom_in_img.classList.add('bg-main')
    zoom_in_img.classList.add('loader')
    var zoom_in = document.createElement('div')
    zoom_in.addEventListener('click', zoomIn)
    zoom_in.insertAdjacentElement('afterbegin',zoom_in_img)

    zoom_out = zoom_in.cloneNode(true)
    zoom_out.children[0].src = `${PATH}zoom_out.svg`
    zoom_out.addEventListener('click', zoomOut)

    zoom_container.insertAdjacentElement('afterbegin',zoom_out)
    zoom_container.insertAdjacentElement('afterbegin',zoom_in)

    var main = document.querySelector('#main') 
    main.insertAdjacentElement('afterbegin',zoom_container)
}

function startDrag( e ){
    // determine event object
    if (!e) {
        var e = window.event;
    }

    // IE uses srcElement, others use target
    var targ = e.target ? e.target : e.srcElement;
    if (!targ.classList.contains('image')) {
        return false
    };
    // check if it is mobile touch
    if (e.type == 'touchstart') {var e = e.touches[0]}
    // calculate event X, Y coordinates
    offsetX = e.clientX;
    offsetY = e.clientY;

    let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
    let vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
    
    // assign default values for top and left properties
    if (!targ.style.left) {
        targ.style.left = `${vw/2}px`
    };
    if (!targ.style.top) {
        targ.style.top = `${vh/2}px`
    };

    // calculate integer values for top and left 
    // properties
    coordX = parseInt(targ.style.left);
    coordY = parseInt(targ.style.top);
    drag = true;


    return false
}

function dragging(e) {
    if (!drag) {return};
    if (!e) { var e= window.event};
    // check if it is mobile touch
    if (e.type == 'touchmove') { e = e.touches[0]}
    var targ=e.target?e.target:e.srcElement;
    // move div element
    var targ = e.target ? e.target : e.srcElement;
    if (targ.classList.contains('image')) {
        targ.style.left=coordX+e.clientX-offsetX+'px';
        targ.style.top=coordY+e.clientY-offsetY+'px';
    };
    return false;
}

function stopDrag( e ){
    drag = false;
}

function toggleImage(img){
    img.classList.toggle('is_fixed')
    img.classList.toggle('image_zoomable')
    img.classList.toggle('m-m')
    img.classList.toggle('zIndPl2')
    img.classList.toggle('image_dragable')
}

function removeOverlay(){
    var dark_overlay = document.querySelector('#overlay')
    dark_overlay.remove()
}


function addOverlay(img){
    var dark_overlay = document.createElement('div')
    dark_overlay.id = 'overlay'
    dark_overlay.classList.add('is_fixed')
    dark_overlay.classList.add('full_width')
    dark_overlay.classList.add('full_height')
    dark_overlay.classList.add('opacity-075')
    dark_overlay.classList.add('bg-black')
    dark_overlay.classList.add('zIndPl2')
    dark_overlay.addEventListener('click', (event) => {
        outImage(img)
    })
    var main = document.getElementById('main')
    main.insertAdjacentElement('afterbegin',dark_overlay)
}

// To open image previewer
function onImage(event){
    toggleImage(this)
    addOverlay(this)
    addExit(this)
    addZoom()
}

// To close image previewer
function outImage(img){
    img.style.transform = ''
    img.style.left = ''
    img.style.top = ''
    // Put image back
    toggleImage(img)
    img.addEventListener('click', onImage, {once: true})
    // Remove overlay
    removeOverlay()
    // Remove close button
    var header_btns = document.querySelectorAll('.header_button') 
    var last_header_btn = header_btns[header_btns.length - 1]
    last_header_btn.remove()
    // Remove zoom buttons
    document.querySelector('#zoom_buttons').remove()

}

function onNewImages(event){
    var images = document.querySelectorAll('.image')
    images.forEach( (img) => {
        img.addEventListener('click', onImage,{once: true})
    })
}

function onReady(){
    document.addEventListener('onMediaUploaded', onNewImages)
    var images = document.querySelectorAll('.image')
    images.forEach( (img) => {
        img.addEventListener('click', onImage,{once: true})
    })
    if (IS_MOBILE){
        document.ontouchstart = startDrag
        document.ontouchmove = dragging
        document.ontouchend = stopDrag
    }
    else{
        document.onmousedown = startDrag;
        document.onmouseup = stopDrag;
        document.onmousemove = dragging;
    }
}

if (document.readyState === "loading") {
    // Loading hasn't finished yet
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
      onReady()
  }