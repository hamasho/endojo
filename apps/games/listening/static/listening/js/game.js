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

.factory('ListeningGameFactory', ListeningGameFactory)

.directive('autofocus', ['$timeout', autofocusDirective])
.directive('audios', ['$sce', audioDirective])

.filter('timeFilter', [timeFilter])

.controller('PackageSelectController', ['$http', 'ListeningGameFactory', PackageSelectController])
.controller('InitController', ['$http', 'ListeningGameFactory', InitController])
.controller('GameController', ['$http', '$timeout', '$interval', '$location', 'ListeningGameFactory', GameController])
.controller('ResultStoreController', ['$http', 'ListeningGameFactory', ResultStoreController]);
