var character_data;

var chart_data = [];

var bmi_data = [];

var currently_selected_data = [];

var character_name_labels = [];

var indices = [];
var heightWeightPoints = [];
var imperialHeightWeightPoints = [];

var isMetric = true;

$(document).ready(function() {
  character_data = $("#data").data("list");



  console.log(character_data);



  var count = 0;
  for (i in character_data) {
    var data = character_data[i];
    if (data["height"] != null && data["weight"] != null) {
      var height = parseInt(data['height']);
      var weight = parseInt(data['weight']);
      if (!isNaN(height) && !isNaN(weight)) {
        indices.push(parseInt(count));
        heightWeightPoints.push([height, weight]);
        imperialHeightWeightPoints.push([cmToIn(height), kgTolb(weight)]);
        chart_data.push(data);
        bmi_data.push([parseInt(computeMetricBMI(height, weight))]);
        character_name_labels.push([parseInt(count), data["name"]]);
        count++;
      }
    }
  }

  plotHeightWeight({ data: heightWeightPoints }, "Height (cm)", "Weight (cm)");
  setupToolTip("#height_weight");

  // Sort the bmi data
  bmi_data.sort(function(a, b) { return a - b });
  bmi_data = bmi_data.map(function(current, index, arr) {
    return [index, current];
  })
  console.log(bmi_data);
  plotBMI(bmi_data);

});


$("#switchUnits").click(function() {
  if (isMetric) {
    isMetric = false;
    plotHeightWeight({ data: imperialHeightWeightPoints }, "Height (in)", "Weight (lb)");
  } else {
    isMetric = true;
    plotHeightWeight({ data: heightWeightPoints }, "Height (cm)", "Weight (cm)");
  }
})

function computeMetricBMI(height, weight) {
  return weight / (height * height * 0.0001);
}

function kgTolb(kg) {
  return Math.round(kg * 2.20462);
}

function cmToIn(cm) {
  return Math.round(cm * 0.393701);
}

function plotBMI(data) {
  let ticks = character_name_labels;
  console.log(ticks);
  let options = {
    series: {
      bars: {
        show: true,
      },
      color: "#058DC7"
    },
    bars: {
      align: "center",
      barWidth: 0.1
    },
    axisLabels: {
      show: true
    },
    xaxes: [{
      axisLabelColour: "#058DC7",
      axisLabel: "Character",
    }],
    yaxes: [{
      axisLabelColour: "#058DC7",
      position: 'left',
      axisLabel: "BMI",
    }],
    xaxis: {
      axisLabel: "Character",
      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 12,
      axisLabelFontFamily: 'Verdana, Arial',
      axisLabelPadding: 10
    },
    yaxis: {
      axisLabel: "BMI",
      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 12,
      axisLabelFontFamily: 'Verdana, Arial',
      axisLabelPadding: 3
    },
    legend: {
      noColumns: 0,
      labelBoxBorderColor: "#000000",
      position: "nw"
    },
    grid: {
      hoverable: true,
      borderWidth: 2,
    }
  };
  $.plot($("#bmi_chart"), [data], options);
  setupToolTip("#bmi_chart");
}


function plotHeightWeight(data, xlabel, ylabel) {
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
    grid: {
      hoverable: true,
      clickable: true
    },
    axisLabels: {
      show: true
    },
    xaxes: [{
      axisLabelColour: "#058DC7",
      axisLabel: xlabel,
    }],
    yaxes: [{
      axisLabelColour: "#058DC7",
      position: 'left',
      axisLabel: ylabel,
    }],
    xaxis: {

      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 12,
      axisLabelPadding: 5,
      //color: "#058DC7"
    },
    yaxis: {

      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 12,
      axisLabelPadding: 5,
      //color: "#058DC7",

    }
  });
  $('.yaxisLabel').css('color', 'red');
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
    //console.log("hover!");
    if (item) {
      let index = indices[item.dataIndex];
      let data = chart_data[index];
      var heightWeight;
      if (isMetric) {
        heightWeight = heightWeightPoints[index];
      } else {
        heightWeight = imperialHeightWeightPoints[index];
      }
      //console.log(pos);
      $("#tooltip").html("Character: " + data["name"] +
          "<br>Gender: " + data["gender"] +
          "<br>Age: " + ((data["age"]) ? data["age"] : "Not found") +
          "<br>Source: " + data["title"] +
          "<br>Height: " + heightWeight[0] +
          "<br>Weight: " + heightWeight[1] +
          "<br>BMI: " + bmi_data[index][1])
        .css({ top: item.pageY + 5, left: item.pageX + 5 })
        .fadeIn(200);

    }
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