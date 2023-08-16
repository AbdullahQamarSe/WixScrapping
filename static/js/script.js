function hideDiv() {
    document.getElementById("content_div").style.display = "none";
    document.getElementById("loader_div").style.display = "flex";
  }
  window.onload = function() {
    console.log('Load window')
    try {
      var downloadLink = document.getElementById('csv_link');
      downloadLink.click();
    } catch (error) {
      
    }
             
          };