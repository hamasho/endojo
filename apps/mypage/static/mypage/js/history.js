(function(angular, Chart) {
'use strict';

/**
 * Main controller
 */
function HistoryController($http) {
  var that = this;
  $http.get('/mypage/histories/')
    .then(function(response) {
      that.histories = response.data.histories;
    });
}

/**
 * Vocabulary game module
 */
angular.module('HistoryApp', [])

.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

.controller('HistoryController', [
  '$http',
  HistoryController
]);

})(angular, Chart);
