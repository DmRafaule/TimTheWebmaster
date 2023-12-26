var canvas = document.getElementById("glslCanvas");
        var sandbox = new GlslCanvas(canvas);
        var texCounter = 0;
        var sandbox_content = "";
        var sandbox_title = "";
        var sandbox_author = "";
        var sandbox_thumbnail = ""; 
		canvas.setAttribute('width', window.innerWidth )

        function parseQuery (qstr) {
            var query = {};
            var a = qstr.split('&');
            for (var i in a) {
                var b = a[i].split('=');
                query[decodeURIComponent(b[0])] = decodeURIComponent(b[1]);
            }
            return query;
        }

        function load(url) {
            // Make the request and wait for the reply
            fetch(url)
                .then(function (response) {
                    // If we get a positive response...
                    if (response.status !== 200) {
                        console.log('Error getting shader. Status code: ' + response.status);
                        return;
                    }
                    // console.log(response);
                    return response.text();
                })
                .then(function(content) {
                    sandbox_content = content;
                    sandbox.load(content);

                    var title = addTitle();
                    var author = addAuthor();
                    if ( title === "unknown" && author === "unknown") {
                        document.getElementById("credits").style.visibility = "hidden";
                    } else {
                        document.getElementById("credits").style.visibility = "visible";
                    }

                    addMeta({
                                'title' : title + ' by ' + author,
                                'type' : 'website',
                                'url': window.location.href,
                                'image': sandbox_thumbnail
                            })                 
                })
        }

        if (window.location.hash !== '') {
            var hashes = location.hash.split('&');
            for (var i in hashes) {
                var ext = hashes[i].substr(hashes[i].lastIndexOf('.') + 1);
                var path = hashes[i];

                // Extract hash if is present
                if (path.search('#') === 0) {
                    path = path.substr(1);
                }

                if (ext === 'frag') {
                    load(path);
                }
                else if (ext === 'png' || ext === 'jpg' || ext === 'PNG' || ext === 'JPG') {
                    sandbox.setUniform("u_tex"+texCounter.toString(), path);
                    texCounter++;
                }
            }
        }
