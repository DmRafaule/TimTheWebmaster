import { LoadPosts } from "./pagiscroll.js"

// To be used in pagiscroll
export function update_time_filters(){
    var this_time = document.querySelector('input[name="thisTime"]:checked');
    if (!this_time)
        this_time = ''
    else
        this_time = this_time.value
    var week_day = []
    document.querySelectorAll('.week_day.selected_order').forEach((el)=>{
        week_day.push(el.dataset.time)
    })
    var month_day = []
    document.querySelectorAll('.month_day.selected_order').forEach((el)=>{
        month_day.push(el.dataset.time)
    })
    var month = []
    document.querySelectorAll('.month.selected_order').forEach((el)=>{
        month.push(el.dataset.time)
    })
    var year = []
    document.querySelectorAll('.year.selected_order').forEach((el)=>{
        year.push(el.dataset.time)
    })
    return [this_time, week_day, month_day, month, year]
}

function onSort(){
	var metaContainer = document.querySelector("#meta-data")
	var isRecent = metaContainer.dataset.sort
	if (isRecent == 'true')
		isRecent = false
	else
		isRecent = true
	metaContainer.dataset.sort = isRecent
	LoadPosts(1, true)
}

function onReady(){
	// Set up buttons effects for filtering by tim
	// Ordering and filtering by date
	var order_btns = document.querySelectorAll('.week_day,.month_day,.month,.year')
	order_btns.forEach( btn => {
		btn.addEventListener('click', (event) => {
			btn.classList.toggle('selected_order')
		})
	})
	var this_time_btns = document.querySelectorAll('input[name="thisTime"]')
	this_time_btns.forEach( btn => {
		btn.addEventListener('click', (event) => {
			var order_btns = document.querySelectorAll('.week_day,.month_day,.month,.year')
			order_btns.forEach( btn => {
				btn.classList.remove('selected_order')
			})
		})
	})

	document.addEventListener('onSort', (event) => {
		onSort()
		event.detail.button.classList.toggle('rotate_X')
	})
}

if (document.readyState === "loading") {
	// Loading hasn't finished yet
	document.addEventListener("DOMContentLoaded", onReady);
} else {
	onReady()
}