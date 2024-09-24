
document.addEventListener('DOMContentLoaded', function(){
    // controls the number of images to upload
    const MAX_IMAGES = 4;
    const imageContainer = document.querySelector('.container.detail');

    // Function to handle file input change
    function handleFileInputChange(input, preview) {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e){
                preview.src = e.target.result;
                preview.style.display = "block";
            }
            reader.readAsDataURL(file);
        } else {
            preview.src = "";
            preview.style.display = "none";
        }
    }

    // for(let i = 1; i <= 4; i++){
    //     console.log(i);
    //     var imageInput = document.getElementById(`image_input_id${i}`);
    //     var imagePreview = document.getElementById(`image_preview_id${i}`);

    //     imageInput.addEventListener('change', function() {
    //         handleFileInputChange(imageInput, imagePreview);
    //     });

    // }

    // Attach event listener to the main image input and the 3 other image inputs
    // todo: look for a more efficient way to implement -- see for loop above
    const mainImageInput = document.getElementById('image_input_id');
    const mainImagePreview = document.getElementById('image_preview_id');

    mainImageInput.addEventListener('change', function() {
        handleFileInputChange(mainImageInput, mainImagePreview);
    });


    // Function to dynamically add image input
    function addImageInput(index) {
        const newItem = document.createElement('div');
        newItem.className = 'item';
        newItem.innerHTML = `
            <div class="item-img-box item-detail">
                <div style="display:flex; flex-direction:column; align-items: center; justify-content: center;">
                    <img src="{{estate.img${index}.url}}" id="image_preview_id_${index}"/>
                    <input type="file" id="image_input_id_${index}" name="img${index}" />
                </div>
            </div>
        `;
        imageContainer.appendChild(newItem);

        const imageInput = document.getElementById(`image_input_id_${index}`);
        const imagePreview = document.getElementById(`image_preview_id_${index}`);

        // Attach event listener to dynamically added input
        imageInput.addEventListener('change', function() {
            handleFileInputChange(imageInput, imagePreview);
        });
    }


    // // Attach event listener to the video input
    // const videoInput = document.getElementById('video_input_id');
    // const videoPreview = document.getElementById('video_preview_id');
    // videoInput.addEventListener('change', function() {
    //     handleFileInputChange(videoInput, videoPreview);
    // });

    // Dynamically add additional image inputs
    for (let i = 2; i <= MAX_IMAGES; i++) {
        addImageInput(i);
    }

});
