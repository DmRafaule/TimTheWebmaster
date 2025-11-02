import "../../Components/Containers/Carousel/carousel.js"
import {initTabs} from "../../Components/Containers/Tabs/tabs_v2.js"
import {mediaLoad} from '../../Components/Base/media_loader.js'
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function toFixHeight(){
    document.querySelectorAll('.resize-block').forEach( (button) => {
        button.addEventListener('click', (event)=>{
            var refElementId = button.dataset.refElementId
            var height = document.querySelector(`#${refElementId}`).getBoundingClientRect().height + "px"
            var refSelectorId = button.dataset.refSelectorId
            var selector = document.querySelector(`#${refSelectorId}`)
            selector.style.height = height
        })
    })
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mediaLoad);
    document.addEventListener("DOMContentLoaded", initTabs);
    toFixHeight()
} else {
	mediaLoad()
	initTabs()
    toFixHeight()
}