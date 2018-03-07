function check_job_status(status_url) {
  //console.log("Status url: " + status_url)
  $.getJSON(status_url, function(data) {
    console.log(data);
    switch (data.status) {
      case "finished":
          console.log(data.result)
          $("#results").html(data.result);
          break;
      case "failed":
          console.log("Job failed: " + data.message);
          alert("Error loading data");
          break;
      default:
        // queued/started/deferred - every 30 seconds
        setTimeout(function() {
          check_job_status(status_url);
        }, 30000);
    }
  });
}