import './htmx.js';
import '../../../../Main/static/Components/Containers/Dropdown/dropdown.js';
import '../../../../Main/static/Components/Base/ImagePreviewer/image_previewer.js';
import "../../../../Main/static/Components/Blocks/Codeblock/microlight.js";
import "../../../../Main/static/Components/Containers/Tabs/tabs.js";
import {mediaLoad} from '../../../../Main/static/Components/Base/media_loader.js'

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mediaLoad);
} else {
	mediaLoad()
}