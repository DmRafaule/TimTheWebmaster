// When the user clicks on the button, open the modal
export function openModal(modal){
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
export function closeModal(modal) {
  modal.style.display = "none";
}

export function initModals(){
  // Get the modal
  document.querySelectorAll(".modal-window").forEach( (modal) =>{
    // Get the buttons that opens the modal, it will be always outside the modal
    var btns = document.querySelectorAll(`#${modal.dataset.btnId}`);
    // Get the <span> element that closes the modal, it will be always inside the modal
    var close_btn = modal.querySelector(`#${modal.dataset.btnCloseId}`);

    btns.forEach((btn)=>{
      btn.addEventListener('click', (ev) => {
        openModal(modal)
      })
    })


    if (close_btn)
      close_btn.addEventListener('click', (ev) => {
        closeModal(modal)
      })

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener('click', (event) => {
      if (event.target == modal) {
        closeModal(modal)
      }
    })
  })
}