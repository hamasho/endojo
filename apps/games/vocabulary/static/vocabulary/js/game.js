/* globals angular: false */
/* globals GameFactory, autofocusDirective: false */
/* globals PackageSelectController: false */
/* globals WordSelectController: false */
/* globals InitController: false */
/* globals VocabularyGameController: false */
/* globals ResultStoreController: false */
'use strict';

/**
 * Vocabulary game module
 */
angular.module('VocabularyGameApp', [
    'ngAnimate',
    'ngSanitize',
    'ui.router',
    'ui.bootstrap',
])

.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

/**
 * Router
 */
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise('select');

  $stateProvider.state('words', {
    url: '/words',
    templateUrl: 'packages/words/select/',
  });
  $stateProvider.state('start', {
    url: '/start',
    templateUrl: 'start/',
  });
  $stateProvider.state('main', {
    url: '/main',
    templateUrl: 'main/',
  });
  $stateProvider.state('result', {
    url: '/result',
    templateUrl: 'result/',
  });
  $stateProvider.state('select', {
    url: '/select',
    templateUrl: 'packages/select/',
  });
}])

.factory('GameFactory', ['$http', '$sce', GameFactory])

.directive('autofocus', ['$timeout', autofocusDirective])

.controller('PackageSelectController', [
    '$scope',
    '$http',
    '$location',
    'GameFactory',
    PackageSelectController
])
.controller('WordSelectController', [
    '$scope',
    '$location',
    '$http',
    '$window',
    '$document',
    'GameFactory',
    WordSelectController
])
.controller('InitController', [
    '$http',
    '$timeout',
    'GameFactory',
    InitController
])
.controller('VocabularyGameController', [
    '$timeout',
    '$location',
    'GameFactory',
    VocabularyGameController
])
.controller('ResultStoreController', [
    '$http',
    '$location',
    '$timeout',
    'GameFactory',
    ResultStoreController
]);
