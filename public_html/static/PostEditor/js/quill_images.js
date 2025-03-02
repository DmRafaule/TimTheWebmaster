class CustomImage extends Quill.import('formats/image'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('image')
        domNode.classList.add('dynamic_image')
        domNode.classList.add('image-bordered')
    }
}
Quill.register(CustomImage, true)

// Text under image
class TextUnderImage extends Quill.import('blots/block'){}
TextUnderImage.tagName = 'div'
TextUnderImage.blotName = "text-under-image"
TextUnderImage.className = "under_image"
Quill.register({'formats/text-under-image': TextUnderImage})