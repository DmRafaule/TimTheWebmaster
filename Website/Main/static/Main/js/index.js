import './htmx.js';
import '../../Components/Containers/Swap/swap.js'
import '../../Components/Containers/Sidebar/sidebar.js'
import '../../Components/Feedbacks/Toaster/toaster.js'
import '../../Components/Feedbacks/Loader/loader.js';
import '../../Components/Containers/Modal/modal.js';
import {tooltipInit} from '../../Components/Feedbacks/Tooltip/tooltip.js'

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", tooltipInit);
} else {
	tooltipInit()
}
