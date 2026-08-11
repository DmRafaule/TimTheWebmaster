import '../../../../Main/static/Components/Containers/Dropdown/dropdown.js';
import '../../../../Main/static/Components/Blocks/Paginator/paginator.js';
import '../../../../Main/static/Components/Blocks/Paginator/infinity_scroll.js';
import '../../../../Main/static/Components/Blocks/Paginator/pagiscroll.js';
import {mediaLoad} from '../../../../Main/static/Components/Base/media_loader.js'

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mediaLoad);
} else {
	mediaLoad()
}