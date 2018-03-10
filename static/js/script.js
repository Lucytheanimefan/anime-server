var spinner;

function check_job_status(status_url) {
  //console.log("Status url: " + status_url)
  $.getJSON(status_url, function(data) {
    startLoadSpinner();
    $("#results").html("<h2>Loading...this could take a long time so maybe go do something else first</h2>");
    switch (data.status) {
      case "finished":
        stopLoadSpinner();
        console.log(data.result)
        $("#results").html(data.result);
        break;
      case "failed":
        stopLoadSpinner();
        console.log("Job failed: " + data.message);
        alert("Error loading data");
        break;
      default:
        // queued/started/deferred - every 5 seconds
        setTimeout(function() {
          check_job_status(status_url);
        }, 5000);
    }
  });
}

function startLoadSpinner() {
  // var opts = {
  //   lines: 13, // The number of lines to draw
  //   length: 38, // The length of each line
  //   width: 17, // The line thickness
  //   radius: 45, // The radius of the inner circle
  //   scale: 1, // Scales overall size of the spinner
  //   corners: 1, // Corner roundness (0..1)
  //   color: '#ffffff', // CSS color or array of colors
  //   fadeColor: 'transparent', // CSS color or array of colors
  //   opacity: 0.25, // Opacity of the lines
  //   rotate: 0, // The rotation offset
  //   direction: 1, // 1: clockwise, -1: counterclockwise
  //   speed: 1, // Rounds per second
  //   trail: 60, // Afterglow percentage
  //   fps: 20, // Frames per second when using setTimeout() as a fallback in IE 9
  //   zIndex: 2e9, // The z-index (defaults to 2000000000)
  //   className: 'spinner', // The CSS class to assign to the spinner
  //   top: '50%', // Top position relative to parent
  //   left: '50%', // Left position relative to parent
  //   shadow: null, // Box-shadow for the lines
  //   position: 'absolute' // Element positioning
  // };

  // var target = document.getElementById('loading-spinner');
  // spinner = new Spinner(opts).spin(target);

}

function stopLoadSpinner(){
  // spinner.stop();
}