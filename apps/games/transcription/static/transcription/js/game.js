/**
 * Transcription game module
 */
angular.module('TranscriptionGameApp', ['ui.router', 'ngAnimate', 'ngSanitize'])

.config(['$interpolateProvider', function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
}])

/**
 * Router
 */
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise('select');

  $stateProvider.state('start', {
    url: '/start',
    templateUrl: 'start/',
  })
  .state('main', {
    url: '/main',
    templateUrl: 'main/',
  })
  .state('result', {
    url: '/result',
    templateUrl: 'result/',
  })
  .state('select', {
    url: '/select',
    templateUrl: 'packages/select/',
  });
}])

.directive('autofocus', ['$timeout', autofocusDirective])

.filter('timeFilter', [timeFilter])

.factory('TranscriptionGameFactory', TranscriptionGameFactory)

.controller('PackageSelectController', ['$http', 'TranscriptionGameFactory', PackageSelectController])
.controller('InitController', ['$http', 'TranscriptionGameFactory', InitController])
.controller('GameController', ['$http', '$timeout', '$interval', '$location', 'TranscriptionGameFactory', GameController])
.controller('ResultStoreController', ['$http', 'TranscriptionGameFactory', ResultStoreController]);
