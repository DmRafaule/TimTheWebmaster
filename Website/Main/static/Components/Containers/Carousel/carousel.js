const slides = document.querySelectorAll('.slide');
const sliderButtons = document.querySelectorAll('.slider-button');
const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');

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

// ---------------------------------
// Lazy Load Images ----------------
// ---------------------------------
// to do: only load the first three or so images when the carousel gets into the viewport. then at every right click load another image - if the urser isnt going to get to all the images whats the point in loading them
const lazySlideImages = document.querySelectorAll('.slide.lazy-img');

const imageObs = new IntersectionObserver((entries, observe) => {
	entries.forEach((entry) => {
		if(entry.isIntersecting) {
			const image = entry.target;
			image.classList.remove('lazy-img');
			imageObs.unobserve(image);
		}
	})
});

lazySlideImages.forEach((slideImage) => {
	imageObs.observe(slideImage);
})


// to do
// make it draggable
