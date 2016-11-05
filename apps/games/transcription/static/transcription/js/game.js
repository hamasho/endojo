/* globals angular: false */
/* globals GameFactory, autofocusDirective, timeFilter: false */
/* globals PackageSelectController: false */
/* globals WordSelectController: false */
/* globals InitController: false */
/* globals TranscriptionGameController: false */
/* globals ResultStoreController: false */
'use strict';

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

.factory('GameFactory', GameFactory)

.controller('PackageSelectController', [
    '$http',
    'GameFactory',
    PackageSelectController
])
.controller('InitController', [
    '$http',
    '$location',
    'GameFactory',
    InitController
])
.controller('GameController', [
    '$http',
    '$timeout',
    '$interval',
    '$location',
    'GameFactory',
    TranscriptionGameController
])
.controller('ResultStoreController', [
    '$http',
    '$location',
    'GameFactory',
    ResultStoreController
]);
