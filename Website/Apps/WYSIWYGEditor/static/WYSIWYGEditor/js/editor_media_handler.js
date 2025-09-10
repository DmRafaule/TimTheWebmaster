export function updateImagesForServer(){
	var scope = document.querySelector('#editor')
	var images = scope.querySelectorAll('img.image')
    var counter = 0
	images.forEach( (image, indx) => {
        if (!image.classList.contains('do-not-change')){
            image.dataset.src = `{% get_media_prefix %}{{images.${counter}.file}}`
            image.alt = `{{images.${counter}.text}}`
            counter += 1
        }
	})
} 

export function updateDownloadablesForServer(){
	var scope = document.querySelector('#editor')
    // WIll not select those downloadables links and videos which is saved via input
	var downloadables = scope.querySelectorAll('a.ref-downloadable:not(.do_not_updateDownloadablesForServer),video.my-video:not(.do_not_updateDownloadablesForServer)')
	downloadables.forEach( (down, indx) => {
        if (down.classList.contains('ref-downloadable')){
            down.setAttribute('href', `{% get_media_prefix %}{{downloadables.${indx}.file}}`)
        }
        else{
            down.dataset.src = `{% get_media_prefix %}{{downloadables.${indx}.file}}`
            down.dataset.text = `{{downloadables.${indx}.text}}`
        }
	})
}

function onReady(){
    // Callback function to execute when mutations are observed
	function  WaitMediaToAppear(mutationList, observer) {
		for (const mutation of mutationList) {
			if (mutation.addedNodes.length > 0){ 
				updateImagesForServer()
                updateDownloadablesForServer()
			}
		}
	};

	const observed = document.querySelector("#editor");
	const config = { childList: true,  subtree: true};
	const observer = new MutationObserver(WaitMediaToAppear);
	observer.observe(observed, config);
 
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}
