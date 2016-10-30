/* globals angular: false */
/* globals GameFactory, timeFilter: false */
/* globals autofocusDirective, audioDirective: false */
/* globals PackageSelectController: false */
/* globals WordSelectController: false */
/* globals InitController: false */
/* globals ListeningGameController: false */
/* globals ResultStoreController: false */

'use strict';
/**
 * Listening game module
 */
angular.module('ListeningGameApp', ['ui.router', 'ngAnimate', 'ngSanitize'])

.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

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

.factory('GameFactory', GameFactory)

.directive('autofocus', ['$timeout', autofocusDirective])
.directive('audios', ['$sce', audioDirective])

.filter('timeFilter', [timeFilter])

.controller('PackageSelectController', [
  '$http',
  'GameFactory',
  PackageSelectController
])
.controller('InitController', [
  '$http',
  'GameFactory',
  InitController
])
.controller('GameController', [
  '$http',
  '$timeout',
  '$interval',
  '$location',
  'GameFactory',
  ListeningGameController
])
.controller('ResultStoreController', [
  '$http',
  'GameFactory',
  ResultStoreController
]);