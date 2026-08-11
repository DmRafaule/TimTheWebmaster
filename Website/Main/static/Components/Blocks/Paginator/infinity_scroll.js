// To use infinity load you need to be attached to specific event
export function WaitSetinelToInteract(sentinel, options = {}){
	const onInfinityLoad = new CustomEvent("onInfinityLoad", {detail: {sentinel: sentinel, id: sentinel.id}});
	const observer = new IntersectionObserver((entries, observer) => {
	for (const entry of entries) {
		if (entry.isIntersecting) {
			sentinel.dispatchEvent(onInfinityLoad)
		}
	}
	}, options);
	observer.observe(sentinel);
}

function onReady(){



	// Callback function to execute when mutations are observed
	function  WaitSentinelToAppear(mutationList, observer) {
		  for (const mutation of mutationList) {
			if (mutation.addedNodes.length > 0){
				for (var i = 0; i < mutation.addedNodes.length; i++){
					// Check if node type is ELEMENT_NODE
					if (mutation.addedNodes[i].nodeType == 1){
						var sentinel = mutation.addedNodes[i].querySelector('.scroll-sentinel')
						// Check if inserted node has .scroll-sentinel
						if (sentinel){
							WaitSetinelToInteract(sentinel)
						}
					}
				}
			}
		  }
		};

	// Observe only those elements that I have explicitly assign
	// This observe those elements that gonna have new children via ajax or
	// Other technologies
	const observedElements = document.querySelectorAll(".toObserve");
	// This observer have to observe only those elements that have new children
	const config = { childList: true, subtree: true, };
	// Set up callback
	const observer = new MutationObserver(WaitSentinelToAppear);
	// Start observing the target node for configured mutations
	observedElements.forEach( (el) => {
		observer.observe(el, config);
	})
	document.querySelectorAll('.scroll-sentinel').forEach( (sent) => {
		WaitSetinelToInteract(sent)
	})
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}

