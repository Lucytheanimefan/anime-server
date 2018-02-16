$(document).ready(function() {
  var character_data = $("#data").data("list");

  console.log(character_data);

  var heightWeightPoints = [];
  for (i in character_data) {
    var data = character_data[i];
    if (data["height"] != null && data["weight"] != null) {
      var height = parseInt(data['height']);
      var weight = parseInt(data['weight']);
      if (!isNaN(height) && !isNaN(weight)) {
        console.log(height + "," + weight);
        heightWeightPoints.push([height, weight])
      }
    }
  }
  //console.log(heightWeightPoints);

  plotHeightWeight(heightWeightPoints);
  setupToolTip("#height_weight");

});

function plotHeightWeight(data) {
  $.plot($("#height_weight"), [data], {
    series: {
      points: {
        radius: 3,
        show: true,
        fill: true,
        fillColor: "#058DC7"
      },
      color: "#058DC7"
    },
    xaxis: {
      tickSize: 5,
      tickLength: 0,
      tickDecimals: 0,
      axisLabel: "Height (cm)",
      axisLabelUseCanvas: false,
      axisLabelFontSizePixels: 12,
      axisLabelPadding: 5,
      //color: "#058DC7"
    },
    yaxis: {
      axisLabel: "Weight (kg)",
      axisLabelUseCanvas: false,
      axisLabelFontSizePixels: 12,
      axisLabelPadding: 5,
      //color: "#058DC7"
    }
  });
  $('.yaxisLabel').css('color','red');
}


function setupToolTip(element) {
  $("<div id='tooltip'></div>").css({
    position: "absolute",
    display: "none",
    border: "1px solid #fdd",
    padding: "2px",
    "background-color": "#fee",
    opacity: 0.80
  }).appendTo("body");

  $(element).bind("plothover", function(event, pos, item) {
    console.log("hover!");
    console.log(item);
    // if ($("#enablePosition:checked").length > 0) {
    //   var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
    //   $("#hoverdata").text(str);
    // }
    // if ($("#enableTooltip:checked").length > 0) {
    //   if (item) {
    //     var x = item.datapoint[0].toFixed(2),
    //       y = item.datapoint[1].toFixed(2);
    //     $("#tooltip").html(item.series.label + " of " + x + " = " + y)
    //       .css({ top: item.pageY + 5, left: item.pageX + 5 })
    //       .fadeIn(200);
    //   } else {
    //     $("#tooltip").hide();
    //   }
    // }
  });
  $("#placeholder").bind("plotclick", function(event, pos, item) {
    if (item) {
      //$("#clickdata").text(" - click point " + item.dataIndex + " in " + item.series.label);
      plot.highlight(item.series, item.datapoint);
    }
  });

}