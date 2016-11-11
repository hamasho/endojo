(function($, Chart) {
'use strict';

var colors = [
  'rgba(179,0,0,0.3)',
  'rgba(204,153,0,0.3)',
  'rgba(0,153,51,0.3)',
  'rgba(51,51,255,0.3)',
  'rgba(153,0,204,0.3)',
  'rgba(255, 159, 64, 0.3)',
];

/**
 * ==================================================================
 * Stats
 * ==================================================================
 */
$.ajax({
  url: '/game/vocabulary/stats/',
  success: function(data) {
    var datasets = [];
    for (var i = 1; i <= 6; i++) {
      datasets.push({
        label: 'State ' + i,
        fill: false,
        borderColor: colors[i - 1],
        backgroundColor: colors[i - 1],
        data: data['state' + i],
      });
    }
    var ctx = document.getElementById("vocabulary-chart").getContext('2d');
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
          }],
        },
        responsive: false,
      }
    });
  },
});

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
