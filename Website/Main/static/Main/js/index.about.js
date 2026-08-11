import "../../Components/Containers/Carousel/carousel.js"
import {mediaLoad} from '../../Components/Base/media_loader.js'

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mediaLoad);
} else {
	mediaLoad()
}