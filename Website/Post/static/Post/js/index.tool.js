import './htmx.js';
import '../../../../Main/static/Components/Containers/Dropdown/dropdown.js';
import '../../../../Main/static/Components/Base/ImagePreviewer/image_previewer.js';
import microlight from "../../../../Main/static/Components/Blocks/Codeblock/microlight.js";
import "../../../../Main/static/Components/Containers/Tabs/tabs.js";
import {mediaLoad} from '../../../../Main/static/Components/Base/media_loader.js'
import "../../../../Main/static/Components/Containers/Carousel/carousel.js"

if (document.readyState === "loading") {
    window.microlight = microlight
    document.addEventListener("DOMContentLoaded", mediaLoad);
} else {
    window.microlight = microlight
	mediaLoad()
}