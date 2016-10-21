var datasets = [];
var colors = [
  'rgba(179,0,0,0.3)',
  'rgba(204,153,0,0.3)',
  'rgba(0,153,51,0.3)',
  'rgba(51,51,255,0.3)',
  'rgba(153,0,204,0.3)',
];

$.ajax({
  url: '/game/transcription/stats',
  success: function(data) {
    for (var i = 0; i < 5; i++) {
      datasets.push({
        label: 'Level ' + (i + 1),
        fill: false,
        borderColor: colors[i],
        backgroundColor: colors[i],
        data: data[i + 1],
      });
    }
    var ctx = document.getElementById("myChart").getContext('2d');
    var scatterChart = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: datasets,
      },
      options: {
        scales: {
          xAxes: [{
            type: 'linear',
            position: 'bottom'
          }]
        },
        responsive: false,
      }
    });
  },
});

/*
   var datasets = [{
   label: 'Level 1',
   fill: false,
   borderColor: 'rgba(255,0,0,0.3)',
   backgroundColor: 'rgba(255,0,0,0.3)',
   data: [
   { x: 0, y: Math.random() * 10, },
   { x: 1, y: Math.random() * 10, },
   { x: 2, y: Math.random() * 10, },
   { x: 3, y: Math.random() * 10, },
   { x: 4, y: Math.random() * 10, },
   { x: 5, y: Math.random() * 10, },
   { x: 6, y: Math.random() * 10, },
   { x: 7, y: Math.random() * 10, }
   ],
   }, {
   label: 'Level 2',
   fill: false,
   borderColor: 'rgba(0,255,0,0.3)',
   backgroundColor: 'rgba(0,255,0,0.3)',
   data: [
   { x: 0, y: Math.random() * 10, },
   { x: 1, y: Math.random() * 10, },
   { x: 2, y: Math.random() * 10, },
   { x: 3, y: Math.random() * 10, },
   { x: 4, y: Math.random() * 10, },
   { x: 5, y: Math.random() * 10, },
   { x: 6, y: Math.random() * 10, },
   { x: 7, y: Math.random() * 10, }
   ],
   }, {
   label: 'Level 3',
   fill: false,
   borderColor: 'rgba(0,0,255,0.3)',
   backgroundColor: 'rgba(0,0,255,0.3)',
   data: [
   { x: 0, y: Math.random() * 10, },
   { x: 1, y: Math.random() * 10, },
   { x: 2, y: Math.random() * 10, },
   { x: 3, y: Math.random() * 10, },
   { x: 7, y: Math.random() * 10, }
   ],
   }, {
   label: 'Level 4',
   fill: false,
   borderColor: 'rgba(0,0,255,0.3)',
   backgroundColor: 'rgba(0,0,255,0.3)',
   data: [
   ],
   },
   ];

   var ctx = document.getElementById("myChart").getContext('2d');
   var scatterChart = new Chart(ctx, {
   type: 'line',
   data: {
   datasets: datasets,
   },
   options: {
   scales: {
   xAxes: [{
   type: 'linear',
   position: 'bottom'
   }]
   },
   responsive: false,
   }
   });
   */
