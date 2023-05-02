$(function() {
    let input = document.getElementById("inputTag");
    let imageName = document.getElementById("audioName")
    input.addEventListener("change", ()=>{
        let inputImage = document.querySelector("input[type=file]").files[0];
        imageName.innerText = inputImage.name;
    });
});

function downloadFile(filename) {
    event.preventDefault();
    var fileUrl = filename;
    console.log(filename)
    var xhr = new XMLHttpRequest();
    xhr.open('GET', fileUrl, true);
    xhr.responseType = 'blob';

    xhr.onload = function () {
        if (xhr.status === 200) {
            var blob = xhr.response;
            var downloadLink = document.createElement('a');
            downloadLink.href = window.URL.createObjectURL(blob);
            downloadLink.download = filename; // Specify the desired file name
            downloadLink.style.display = 'none';
            document.body.appendChild(downloadLink);

            downloadLink.addEventListener('click', function () {
                checkDownloadCompletion(fileUrl);
                document.body.removeChild(link);
            });
            downloadLink.click();

        }
    };
    xhr.send();
}

function runPythonFile(fileUrl) {
    $.ajax({
      url: '/updateFile',
      type: 'GET',
      data: 
      {
        file: fileUrl
      },
      dataType: 'text',
      success: function(response) {
        console.log('Python file executed successfully. Output:', response);
      },
      error: function(xhr, status, error) {
        console.error('Error executing Python file. Status:', xhr.status);
      }
    });
}

function checkDownloadCompletion(fileUrl) {
    fetch(fileUrl)
        .then(function(response) {
            if (response.ok) {
                console.log('Download completed');
                runPythonFile(fileUrl)
            } else {
                console.log('Download failed');
            }
        })
        .catch(function(error) {
            console.log('Download failed');
        });
}