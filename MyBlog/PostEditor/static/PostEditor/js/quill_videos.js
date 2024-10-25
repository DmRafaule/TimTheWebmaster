// Video
class CustomVideo extends Quill.import('formats/video'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('dynamic_image')
        domNode.controls = 'true'
        domNode.preload = 'metadata'
        let tooltip = new VideoTooltip(quill, domNode, 'video URL or #')
        tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
        tooltip.show()
    }
}
CustomVideo.tagName = 'video'
CustomVideo.className = 'my-video'
CustomVideo.blotName = 'my-video'
Quill.register(CustomVideo, true)