(function($, Chart) {
'use strict';

var colors = [
  'rgba(179,0,0,0.3)',
  'rgba(204,153,0,0.3)',
  'rgba(0,153,51,0.3)',
  'rgba(51,51,255,0.3)',
  'rgba(153,0,204,0.3)',
];

/**
 * ==================================================================
 * Stats
 * ==================================================================
 */
$.ajax({
  url: '/game/listening/stats/',
  success: function(data) {
    var datasets = [];
    for (var i = 0; i < 5; i++) {
      datasets.push({
        label: 'Level ' + (i + 1),
        fill: false,
        borderColor: colors[i],
        backgroundColor: colors[i],
        data: data[i + 1],
      });
    }
    var ctx = document.getElementById("listening-chart").getContext('2d');
    var scatterChart = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: datasets,
      },
      options: {
        scales: {
          xAxes: [{
            type: 'time',
            position: 'bottom',
            time: {
              unit: 'day',
              displayFormats: {
                day: 'MMM DD YYYY',
              },
            },
          }]
        },
        responsive: false,
      }
    });
  },
});

$.ajax({
  url: '/game/transcription/stats/',
  success: function(data) {
    var datasets = [];
    for (var i = 0; i < 5; i++) {
      datasets.push({
        label: 'Level ' + (i + 1),
        fill: false,
        borderColor: colors[i],
        backgroundColor: colors[i],
        data: data[i + 1],
      });
    }
    var ctx = document.getElementById("transcription-chart").getContext('2d');
    var scatterChart = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: datasets,
      },
      options: {
        scales: {
          xAxes: [{
            type: 'time',
            position: 'bottom',
            time: {
              unit: 'day',
              displayFormats: {
                day: 'MMM DD YYYY',
              },
            },
          }]
        },
        responsive: false,
      }
    });
  },
});

})(jQuery, Chart);
