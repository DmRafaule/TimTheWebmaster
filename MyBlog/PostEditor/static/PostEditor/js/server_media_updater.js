
function updateCodeBlock(scope){
	scope.querySelectorAll('.ql-code-block-container').forEach( (el) => {
		el.querySelector('select.ql-ui').style.display = 'none'
	})
}

function updateImagesForServer(){
	var scope = document.querySelector('#editor')
	var images = scope.querySelectorAll('img.image')
	images.forEach( (image, indx) => {
		image.dataset.src = `{% get_media_prefix %}{{images.${indx}.file}}`
		image.alt = `{{images.${indx}.text}}`
	})
} 
function updateImagesForServerClearSRC(scope){
	var images = scope.querySelectorAll('img.image')
	images.forEach( (image, indx) => {
		image.src = PATH+'image-not-found.webp'
	})
} 

function updateDownloadablesForServer(){
	var scope = document.querySelector('#editor')
	var downloadables = scope.querySelectorAll('a.ref-downloadable,video.my-video')
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

function onReady() {
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