import { adLoad } from './admanager.js';

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", adLoad);
} else {
	adLoad()
}