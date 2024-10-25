// Images
class CustomImage extends Quill.import('formats/image'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('image')
        domNode.classList.add('dynamic_image')
        domNode.classList.add('image-bordered')
    }
}
Quill.register(CustomImage, true)