var file_upload = document.getElementById('file_upload');
var submit_button = document.getElementById('submit_button');

var result_img = document.getElementById('result_img');

file_upload.onchange = function () {
  if (file_upload.value == '') {
    submit_button.disabled = true;
  }
  else {
    submit_button.disabled = false;
  }
}

if (result_img.getAttribute('src') == '') {
  result_img.style.display = 'none';
}