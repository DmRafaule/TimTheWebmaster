export function adLoad() {
	let onAdUploaded = new CustomEvent('onAdUploaded')

	function pushAd(ad_block_id, render_to_id, type){
		if (render_to_id){
			render_to_id = `_${render_to_id}`
		}else{
			render_to_id = ''
		}
		window.yaContextCb.push(() => {
			Ya.Context.AdvManager.render({
				"blockId": ad_block_id,
				"renderTo": `ad_block_${ad_block_id}${render_to_id}`,
				"type": type,
				"onRender": (data) => { 
					var ad_marker = document.querySelector(`#ad_block_element_marker_${ad_block_id}${render_to_id}`)
					if (ad_marker){
						ad_marker.remove()
					}
					var ad_block = document.querySelector(`#ad_block_${ad_block_id}${render_to_id}`).parentElement
					if (ad_block){
						ad_block.classList.add('ad_block_no_background')
					}
				}
			})
		})
	}

	function onNodeAppear(ad_block){
		var ad_block_id = ad_block.dataset.adId
		var ad_block_page_id = ad_block.dataset.adUnificator
		var ad_block_type = ad_block.dataset.adType
		pushAd(ad_block_id,ad_block_page_id, ad_block_type)
	}

	// Возможно, в будущем, я захочу что-нибудь сделать с рекламными блоками, когда они появляются на экране
	function WaitAdToUpload(adBlock){
		var options = {
			  threshold: 0,
			};
		var adBlock_observer = new IntersectionObserver((entries, observer) => {
		  // Loop through the entries
		  for (const entry of entries) {
			// Check if the entry is intersecting the viewport
			if (entry.isIntersecting) {

			}
		  }
		}, options);
		adBlock_observer.observe(adBlock);
	}


	// Callback function to execute when mutations are observed
	function  WaitAdToAppear(mutationList, observer) {
		  for (const mutation of mutationList) {
			mutation.addedNodes.forEach(node => { 
				if (node.nodeType === 1){
					if (node.classList.contains("ad_block") || node.querySelector('.ad_block')){
						document.dispatchEvent(onAdUploaded)
						var ad_block = node.querySelector('.ad_block_element')
						onNodeAppear(ad_block)
					}
				}
			})
		  }
		};

	const observedElement = document.querySelector("body");
	const config = { childList: true, subtree: true};
	const observer = new MutationObserver(WaitAdToAppear);
	observer.observe(observedElement, config);

	const adBlocks = document.querySelectorAll(".ad_block_element");
	adBlocks.forEach( (adBlock) => {
		onNodeAppear(adBlock)
	})

}