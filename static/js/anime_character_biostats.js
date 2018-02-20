var character_data;
var chart_dataF = [];
var chart_dataM = []; //, female_character_data, male_character_data;
var chart_data = [];
var chart_dataA = [];

var bmi_data = [];
var bmi_dataF = [];
var bmi_dataM = [];
var bmi_dataA = [];

var currently_selected_data = [];

var character_name_labels = [];

var indices = [];
var indicesF = [];
var indicesM = [];
var indicesA = [];


var heightWeightPoints = [];
var heightWeightPointsF = [];
var heightWeightPointsM = [];
var heightWeightPointsA = [];

var imperialHeightWeightPoints = [];
var imperialHeightWeightPointsF = [];
var imperialHeightWeightPointsM = [];
var imperialHeightWeightPointsA = [];

var isMetric = true;

var white = "rgba(255,255,255,0.5)";
var highlightWhite = "rgba(255, 255, 255, 0.3)";

$(document).ready(function() {
  character_data = $("#data").data("list");

  character_data = character_data.filter(function(character_data) {
    return (character_data["weight"] != null && character_data["height"] != null);
  }).map(function(current, index) {
    current["bmi"] = computeMetricBMI(parseInt(current["height"]), parseInt(current["weight"]));
    return current;
  })

  character_data = character_data.sort(function(a, b) {
    if (a["bmi"] != null && b["bmi"] != null) {
      return a["bmi"] - b["bmi"];
    }
    return 0;
  })

  // female_character_data = character_data.filter(function(character) {
  //   if (character["gender"] != null) {
  //     return (character["gender"].toLowerCase() == "female")
  //   }
  //   return false
  // })
  // male_character_data = character_data.filter(function(character) {
  //   if (character["gender"] != null) {
  //     return (character["gender"].toLowerCase() == "male")
  //   }
  //   return false;
  // })

  var femaleCount = 0;
  var maleCount = 0;
  var count = 0;
  var allCount = 0;
  for (i in character_data) {
    var data = character_data[i];
    var height = parseInt(data['height']);
    var weight = parseInt(data['weight']);
    var gender = data['gender'];
    if (!isNaN(height) && !isNaN(weight)) {
      var toInclude = false;
      if (gender == null) {
        indices.push(parseInt(count));
        heightWeightPoints.push([height, weight]);
        imperialHeightWeightPoints.push([cmToIn(height), kgTolb(weight)]);
        chart_data.push(data);
        bmi_data.push([count, data['bmi']]);
        //character_name_labels.push([parseInt(count), data["name"]]);
        count++;
        toInclude = true;
      } else if (gender.toLowerCase() == "female") {
        indicesF.push(parseInt(count));
        heightWeightPointsF.push([height, weight]);
        imperialHeightWeightPointsF.push([cmToIn(height), kgTolb(weight)]);
        chart_dataF.push(data);
        bmi_dataF.push([count, data['bmi']]);
        //character_name_labels.push([parseInt(count), data["name"]]);
        //femaleCount++;
        count++;
        toInclude = true;
      } else if (gender.toLowerCase() == "male") {
        indicesM.push(parseInt(count));
        heightWeightPointsM.push([height, weight]);
        imperialHeightWeightPointsM.push([cmToIn(height), kgTolb(weight)]);
        chart_dataM.push(data);
        bmi_dataM.push([count, data['bmi']]);
        //character_name_labels.push([parseInt(count), data["name"]]);
        count++;
        toInclude = true;
      }

      // if (toInclude) {
      //   indicesA.push(parseInt(allCount));
      //   heightWeightPointsA.push([height, weight]);
      //   imperialHeightWeightPointsA.push([cmToIn(height), kgTolb(weight)]);
      //   chart_dataA.push(data);
      //   bmi_dataA.push([allCount, data['bmi']]);
      //   //character_name_labels.push([parseInt(count), data["name"]]);
      //   allCount++;
      // }
    }
  }


  indicesA = indices.concat(indicesF, indicesM);
  chart_dataA = chart_data.concat(chart_dataF, chart_dataM);
  console.log(chart_dataA);
  heightWeightPointsA = heightWeightPoints.concat(heightWeightPointsF, heightWeightPointsM);
  imperialHeightWeightPointsA = imperialHeightWeightPoints.concat(imperialHeightWeightPointsF, imperialHeightWeightPointsM);

  plotHeightWeight([{ data: heightWeightPoints, color: 'yellow', label: 'undefined' },
    { data: heightWeightPointsF, color: 'red', label: 'female' },
    { data: heightWeightPointsM, color: 'blue', label: 'male' }
  ], "Height (cm)", "Weight (cm)");

  setupToolTip("#height_weight");

  console.log(bmi_data);

  plotBMI([{ data: bmi_data, color: 'yellow', label: 'undefined', highlightColor: highlightWhite },
    { data: bmi_dataF, color: 'red', label: 'female', highlightColor: highlightWhite },
    { data: bmi_dataM, color: 'blue', label: 'male', highlightColor: highlightWhite }
  ]);

});




$("#switchUnits").click(function() {
  if (isMetric) {
    isMetric = false;
    plotHeightWeight([{ data: imperialHeightWeightPoints, color: 'yellow', label: 'undefined' },
      { data: imperialHeightWeightPointsF, color: 'red', label: 'female' },
      { data: imperialHeightWeightPointsM, color: 'blue', label: 'male' }
    ], "Height (in)", "Weight (lb)");
    $(this).html('Switch to metric units');
  } else {
    isMetric = true;
    plotHeightWeight([{ data: heightWeightPoints, color: 'yellow', label: 'undefined' },
      { data: heightWeightPointsF, color: 'red', label: 'female' },
      { data: heightWeightPointsM, color: 'blue', label: 'male' }
    ], "Height (cm)", "Weight (kg)");
    $(this).html('Switch to imperial units');
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

function nearestTenth(number) {
  return number.toFixed(2);
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
      barWidth: 0.5
    },
    axisLabels: {
      show: true
    },
    xaxes: [{
      axisLabelColour: white,
      axisLabel: "Character",
    }],
    yaxes: [{
      axisLabelColour: white,
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
      position: "nw"
    },
    grid: {
      hoverable: true,
      borderWidth: 2,
      autoHighlight: true
    }
  };
  let plot = $.plot($("#bmi_chart"), data, options);
  console.log(plot);

  setupToolTip("#bmi_chart");
}


function plotHeightWeight(data, xlabel, ylabel) {
  $.plot($("#height_weight"), data, {
    series: {
      points: {
        radius: 3,
        show: true,
        fill: false
      }
    },
    legend: {
      position: "nw"
    },
    grid: {
      hoverable: true,
      clickable: true
    },
    axisLabels: {
      show: true
    },
    xaxes: [{
      axisLabelColour: white,
      axisLabel: xlabel,
    }],
    yaxes: [{
      axisLabelColour: white,
      axisLabel: ylabel,
    }],
    xaxis: {
      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 12,
      axisLabelPadding: 5,
    },
    yaxis: {
      axisLabelUseCanvas: true,
      axisLabelFontSizePixels: 12,
      axisLabelPadding: 5,
    }
  });
  $('.yaxisLabel').css('color', 'red');
}


function setupToolTip(element) {
  $("<div id='tooltip'></div>").css({
    position: "absolute",
    display: "none",
    border: "1px solid #00F",
    "border-radius": "2px",
    padding: "10px",
    "background-color": "#fee",
    opacity: 0.80
  }).appendTo("body");

  $(element).bind("plothover", function(event, pos, item) {
    //console.log("hover!");
    if (item) {
      var index = item.dataIndex;
      var data;
      var heightWeight;
      console.log(item.series.color);
      if (item.series.color == 'blue') { // male
        data = chart_dataM[index];
        if (isMetric) {
          heightWeight = heightWeightPointsM[index];
        } else {
          heightWeight = imperialHeightWeightPointsM[index];
        }
      } else if (item.series.color == 'red') {
        data = chart_dataF[index];
        if (isMetric) {
          heightWeight = heightWeightPointsF[index];
        } else {
          heightWeight = imperialHeightWeightPointsF[index];
        }
      } else {
        console.log(chart_dataM[index]);
        data = chart_data[index];
        if (isMetric) {
          heightWeight = heightWeightPoints[index];
        } else {
          heightWeight = imperialHeightWeightPoints[index];
        }
      }
      if (isMetric) {
        units = ['cm', 'kg'];
      } else {
        units = ['in', 'lb'];
      }

      $("#tooltip").html("Character: " + data["name"].replace("_", " ") +
          "<br>Gender: " + data["gender"] +
          "<br>Age: " + ((data["age"]) ? data["age"] : "Not found") +
          "<br>Source: " + data["title"] +
          "<br>Height: " + heightWeight[0] + " " + units[0] +
          "<br>Weight: " + heightWeight[1] + " " + units[1] +
          "<br>BMI: " + nearestTenth(data["bmi"]))
        .css({ top: item.pageY + 20, left: item.pageX - 50 })
        .fadeIn(200);

    }

  });
  $("#placeholder").bind("plotclick", function(event, pos, item) {
    if (item) {
      //$("#clickdata").text(" - click point " + item.dataIndex + " in " + item.series.label);
      plot.highlight(item.series, item.datapoint);
    }
  });

}