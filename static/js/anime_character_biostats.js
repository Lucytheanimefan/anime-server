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

  plotBMI([{ data: bmi_data, color: 'yellow', label: 'undefined' },
    { data: bmi_dataF, color: 'red', label: 'female' },
    { data: bmi_dataM, color: 'blue', label: 'male' }
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
    border: "1px solid #fdd",
    padding: "2px",
    "background-color": "#fee",
    opacity: 0.80
  }).appendTo("body");

  $(element).bind("plothover", function(event, pos, item) {
    //console.log("hover!");
    if (item) {
      //console.log(item);
      var index = item.dataIndex;
      var data;
      var heightWeight;
      console.log(item.series.color);
      if (item.series.color == 'blue') { // male
        //var index = indicesM[item.dataIndex];
        data = chart_dataM[index];
        if (isMetric) {
          heightWeight = heightWeightPointsM[index];
        } else {
          heightWeight = imperialHeightWeightPointsM[index];
        }
      } else if (item.series.color == 'red') {
        //var index = indicesF[item.dataIndex];
        data = chart_dataF[index];
        if (isMetric) {
          heightWeight = heightWeightPointsF[index];
        } else {
          heightWeight = imperialHeightWeightPointsF[index];
        }
      } else {
        //var index = indices[item.dataIndex];
        console.log(chart_dataM[index]);
        data = chart_data[index];
        if (isMetric) {
          heightWeight = heightWeightPoints[index];
        } else {
          heightWeight = imperialHeightWeightPoints[index];
        }
      }
      console.log(index);
      console.log(data);
      //console.log(chart_dataA[index]);
      //let data = chart_data[index];

      // var index = indicesA[item.dataIndex];
      // var data = chart_dataA[index];
      // var heightWeight;
      // var units;
      if (isMetric) {
        //heightWeight = heightWeightPointsA[index];
        units = ['cm', 'kg'];
      } else {
        //heightWeight = imperialHeightWeightPointsA[index];
        units = ['in', 'lb'];
      }
      // console.log(index);
      // console.log(data);
      //console.log(item);

      $("#tooltip").html("Character: " + data["name"] +
          "<br>Gender: " + data["gender"] +
          "<br>Age: " + ((data["age"]) ? data["age"] : "Not found") +
          "<br>Source: " + data["title"] +
          "<br>Height: " + heightWeight[0] + " " + units[0] +
          "<br>Weight: " + heightWeight[1] + " " + units[1] +
          "<br>BMI: " + data["bmi"])
        .css({ top: item.pageY + 5, left: item.pageX + 5 })
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