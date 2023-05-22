$(function() {
    let input = document.getElementById("inputTag");
    let imageName = document.getElementById("audioName")
    input.addEventListener("change", ()=>{
        let inputImage = document.querySelector("input[type=file]").files[0];
        imageName.innerText = inputImage.name;
    });
});