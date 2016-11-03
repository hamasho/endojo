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
 * Home
 * ==================================================================
 */
$.ajax({
  url: '/mypage/score/',
  success: function(data) {
    var userDatasets = [{
      label: 'User Score',
      fill: false,
      borderColor: colors[0],
      backgroundColor: colors[0],
      data: [data.user_score],
    }];
    var userCtx = document.getElementById("user-score-chart").getContext('2d');
    var userScatterChart = new Chart(userCtx, {
      type: 'horizontalBar',
      data: {
        labels: ['User Score'],
        datasets: userDatasets,
      },
      options: {
        legend: {
          display: false,
        },
        scales: {
          xAxes: [{
            position: 'bottom',
            ticks: {
              min: 0,
            },
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

    var datasets = [{
      label: 'Each Game\'s Score',
      fill: false,
      borderColor: colors[2],
      backgroundColor: colors[2],
      data: [
        data.vocabulary_score,
        data.listening_score,
        data.transcription_score,
      ],
    }];
    var allCtx = document.getElementById("score-chart").getContext('2d');
    var allScatterChart = new Chart(allCtx, {
      type: 'horizontalBar',
      data: {
        labels: ['Vocabulary', 'Listening', 'Transcription'],
        datasets: datasets,
      },
      options: {
        legend: {
          display: false,
        },
        scales: {
          xAxes: [{
            position: 'bottom',
            ticks: {
              min: 0,
            },
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
  }
});

})(jQuery, Chart);
