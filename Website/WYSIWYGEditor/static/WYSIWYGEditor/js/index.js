import './editor_media_handler.js';
import './editor_resize.js';
import './editor_upload.js';
import './quill-engine.js';
import './quill_images.js';
import './quill_blocks.js';
import './quill_videos.js';
import './quill_codeblock.js';
import './quill_abbr.js';
import './quill_links.js';
import './quill_table.js';
import './quill_headers.js'
import { regenerateAllHeaderIDs } from './quill_headers.js';
import './quill.js';
import './on_page_translation.js';
import 'htmx.org';

// Из-за того, что при отправке запроса через htmx контент копируется с самого начала, делаю 
// это на чистом JS, но не на HTMX
function getContent(){
    regenerateAllHeaderIDs()
    var content = document.querySelector('.ql-editor').innerHTML;
    return content;
}

window.getContent = getContent