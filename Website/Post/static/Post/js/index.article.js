import './htmx.js';
import '../../../../Main/static/Components/Containers/Dropdown/dropdown.js';
import '../../../../Main/static/Components/Base/ImagePreviewer/image_previewer.js'
import "../../../../Main/static/Components/Blocks/Codeblock/microlight.js";
import "../../../../Main/static/Components/Containers/Tabs/tabs.js";
import {mediaLoad} from '../../../../Main/static/Components/Base/media_loader.js'
import {initLinkGather} from '../../../../Main/static/Components/Base/link_gather.js'; 
import {initTableOfContent} from '../../../../Main/static/Components/Containers/TableOfContent/table_of_content.js'

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mediaLoad);
    document.addEventListener("DOMContentLoaded", initLinkGather);
    document.addEventListener("DOMContentLoaded", initTableOfContent);
} else {
	mediaLoad()
    initLinkGather()
    initTableOfContent()
}