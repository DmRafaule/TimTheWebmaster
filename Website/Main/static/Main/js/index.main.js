import "../../Components/Containers/Tabs/tabs.js"
import {MiniMasonry} from "../../Components/Containers/Masonry/masonry.js"
import {mediaLoad} from '../../Components/Base/media_loader.js'
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var msnry = new MiniMasonry( {
    container: '.masonry',
    gutter: 5,
    basewidth: 400
});
msnry.layout()

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mediaLoad);
} else {
	mediaLoad()
}