import { IS_MOBILE } from "../mobile_check.js"

var drag = false;
var offsetX = 0;
var offsetY = 0;
var coordX = 0;
var coordY = 0;

// Insert exit button on page
function addExit(img){
    var header_splitter = document.querySelector('#header-buttons-splitter') 
    var header_button_to_exit = header_splitter.previousElementSibling.lastElementChild.cloneNode(true)
    header_button_to_exit.classList.remove("ttw-button_swap_not_active")
    header_button_to_exit.classList.remove("ttw-sidebar_button_close")
    header_button_to_exit.classList.remove("ttw-button_swap_back")
    header_button_to_exit.addEventListener('click',()=>{
        outImage(img)
        header_button_to_exit.remove()
    })
    header_splitter.insertAdjacentElement('beforebegin', header_button_to_exit)
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
    zoom_container.classList.add('flex')
    zoom_container.classList.add('flex-col')
    zoom_container.classList.add('flex-nowrap')
    zoom_container.classList.add('gap-3')
    zoom_container.classList.add('m-2')
    zoom_container.classList.add('fixed')
    zoom_container.classList.add('bottom-0')
    zoom_container.classList.add('left-0')
    zoom_container.classList.add('p-2')
    zoom_container.classList.add('z-30')

    var zoom_in_img = document.createElement('img')
    zoom_in_img.src = `${PATH}zoom_in.svg`
    zoom_in_img.classList.add('ttw-button_squared')
    zoom_in_img.classList.add('bg-main')
    zoom_in_img.classList.add('loader')

    var zoom_in = document.createElement('div')
    zoom_in.classList.add('ttw-button')
    zoom_in.classList.add('ttw-button_action')
    zoom_in.classList.add('ttw-button_squared')
    zoom_in.addEventListener('click', zoomIn)
    zoom_in.insertAdjacentElement('afterbegin',zoom_in_img)

    var zoom_out = zoom_in.cloneNode(true)
    zoom_out.children[0].src = `${PATH}zoom_out.svg`
    zoom_out.addEventListener('click', zoomOut)

    zoom_container.insertAdjacentElement('afterbegin',zoom_out)
    zoom_container.insertAdjacentElement('afterbegin',zoom_in)

    var main = document.querySelector('main') 
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

function addImage(img){
    img.id = 'image_previewer_copy'
    img.classList.toggle('fixed')
    img.classList.toggle('image_zoomable')
    img.classList.toggle('image_dragable')
    img.classList.toggle('z-20')
    var main = document.querySelector('main')
    main.insertAdjacentElement('afterbegin',img)
}

function removeImage(img){
    document.querySelector('#image_previewer_copy').remove()
}

function removeOverlay(){
    var dark_overlay = document.querySelector('#overlay')
    dark_overlay.remove()
}


function addOverlay(img){
    var dark_overlay = document.createElement('div')
    dark_overlay.id = 'overlay'
    dark_overlay.classList.add('image_overlay')
    dark_overlay.addEventListener('click', (event) => {
        outImage(img)
    })
    var main = document.querySelector('main')
    main.insertAdjacentElement('afterbegin',dark_overlay)
}

// To open image previewer
function onImage(event){
    if (IS_MOBILE){
        document.ontouchstart = startDrag
        document.ontouchmove = dragging
        document.ontouchend = stopDrag
    }
    else{
        document.onmousedown = startDrag
        document.onmouseup = stopDrag
        document.onmousemove = dragging
    }
    var image_copy = this.cloneNode(true)
    addImage(image_copy)
    addOverlay(this)
    addExit(this)
    addZoom()
}

// To close image previewer
function outImage(img){
    if (IS_MOBILE){
        document.ontouchstart = (e)=>{}
        document.ontouchmove = (e)=>{}
        document.ontouchend = (e)=>{}
    }
    else{
        document.onmousedown = (e)=>{}
        document.onmouseup = (e)=>{}
        document.onmousemove = (e)=>{}
    }
    img.style.transform = ''
    img.style.left = ''
    img.style.top = ''
    removeImage(img)
    // Remove overlay
    removeOverlay()
    // Remove close button
    var header_splitter = document.querySelector('#header-buttons-splitter') 
    var header_button_to_exit = header_splitter.previousElementSibling
    header_button_to_exit.remove()
    // Remove zoom buttons
    document.querySelector('#zoom_buttons').remove()

}

function onNewImages(event){
    var images = document.querySelectorAll('.image')
    images.forEach( (img) => {
        img.addEventListener('click', onImage)
    })
}

function onReady(){
    document.addEventListener('onMediaUploaded', onNewImages)
    var images = document.querySelectorAll('.image')
    images.forEach( (img) => {
        img.addEventListener('click', onImage)
    })
}

if (document.readyState === "loading") {
    // Loading hasn't finished yet
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}