function readFile(file) {
    var rawFile = new XMLHttpRequest();
    var result = ""
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
      if(rawFile.readyState === 4)  {
        if(rawFile.status === 200 || rawFile.status == 0) {
          result = rawFile.responseText;
         }
      }
    }
    rawFile.send(null);
    return result
}

function createIcon(path){
  let icon = document.createElement('img')
  icon.classList.add('icon')
  icon.classList.add('dynamic_image')
  icon.setAttribute('width', 32)
  icon.setAttribute('height', 32)
  icon.setAttribute('src', path)
  return icon;
}

// Return all elements between start_query_selector and end_query_selector 
function getRangeDomElements(start_query_selector, end_query_selector){
  var element = document.querySelector(start_query_selector)
  var elements = []
  // Get all stylesheets files 
  while (element.nextElementSibling.id != end_query_selector.slice(1)){
    element = element.nextElementSibling
    elements.push(element)
  }
  return elements
}

function getSubstringBetween(content, startstring, endstring){
	var strings = []
  	var start = 0
	var end = String(content).indexOf(endstring, start)
	while (end != -1){
		var query = String(content).substring(start, end).replaceAll('\n','').replaceAll(' ', '').split(',')
		start = String(content).indexOf(startstring, start) + startstring.length
		end = String(content).indexOf(endstring, start)
		strings.push(query)
	}
	return strings
}

function checkStylesheets(document_part, stylesheets) {
    var stylesheets_in_use = []
    // Check all stylesheets files
    stylesheets.forEach( (stylesheet) => {
        var content = readFile(stylesheet.getAttribute('href')).replaceAll('\r', '')
        // Remove all comments
        var start_com = 0
        var end_com = String(content).indexOf('*/', start_com)
        while (end_com != -1){
            start_com = String(content).indexOf('/*', start_com)
            var comment = String(content).substring(start_com, end_com + 2)
            content = String(content).replace(comment, '')
            start_com = end_com + 2
            end_com = String(content).indexOf('*/', start_com)
        }

        // Retrieve all possible queries
        getSubstringBetween(content, '}', '{').forEach((query)=>{
            if (document_part.querySelector(query)){
                stylesheets_in_use.push(stylesheet)
            }
        })
    })
    return [...new Set(stylesheets_in_use)]
}