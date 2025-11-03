document.querySelectorAll('.carousel').forEach( (carousel) => {
	const slides = carousel.querySelectorAll('.slide');
	const buttons_container = document.querySelector(`#${carousel.dataset.buttonsId}`)
	const sliderButtons = buttons_container.querySelectorAll('.slider-button');
	const prevButton = buttons_container.querySelector('.prev');
	const nextButton = buttons_container.querySelector('.next');

	const disableButtons = (prevButton, nextButton, index) => {
		const lastSlideIndex = slides.length - 1;
		const firstSlideIndex = 0;

		if (index === lastSlideIndex) {
			nextButton.setAttribute('aria-disabled', true);
			nextButton.setAttribute('aria-label', 'no next slide available');
		} else if (index === firstSlideIndex) {
			prevButton.setAttribute('aria-disabled', true);
			prevButton.setAttribute('aria-label', 'no previous slide available');
		} else {
			nextButton.removeAttribute('aria-disabled');
			prevButton.removeAttribute('aria-disabled');
			nextButton.setAttribute('aria-label', 'next slide');
			prevButton.setAttribute('aria-label', 'previous slide');
		}
	}

	const controlSlider = (e) => {
		let currentIndex = 0;
		slides.forEach((slide, index) => {
			const hiddenAttribute = slide.getAttribute('aria-hidden');
			if (hiddenAttribute === 'false') currentIndex = index
		});
		var slideToActivate = null
		if (e.target.classList.contains('next')){
			slideToActivate = slides[currentIndex + 1]
		}
		else{
			if (e.target.classList.contains('prev')){
				slideToActivate = slides[currentIndex - 1]
			}
		}
		if (slideToActivate !== undefined) {
			// hide current slide
			slides[currentIndex].setAttribute('aria-hidden', true);
			slides[currentIndex].removeAttribute('tabindex');
			
			// disable buttons if needed
			const activateIndex = [...slides].indexOf(slideToActivate);
			disableButtons(prevButton, nextButton, activateIndex);
			
			// set active slide
			slideToActivate.setAttribute('aria-hidden', false);
			slideToActivate.setAttribute('tabindex', 0);
			slideToActivate.focus()
		} 
	}

	sliderButtons.forEach((button) => {
		button.addEventListener('click', controlSlider)
	});

})
