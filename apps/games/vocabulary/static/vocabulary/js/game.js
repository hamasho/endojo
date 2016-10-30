/**
 * Vocabulary game module
 */
angular.module('VocabularyGameApp', ['ui.router', 'ngAnimate', 'ngSanitize'])

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

.factory('VocabularyGameFactory', VocabularyGameFactory)

.directive('autofocus', ['$timeout', autofocusDirective])

.controller('PackageSelectController', ['$scope', '$http', 'VocabularyGameFactory', PackageSelectController])
.controller('WordSelectController', ['$scope', '$http', '$window', 'VocabularyGameFactory', WordSelectController])
.controller('InitController', ['$http', '$timeout', 'VocabularyGameFactory', InitController])
.controller('VocabularyGameController', ['$timeout', '$location', 'VocabularyGameFactory', VocabularyGameController])
.controller('ResultStoreController', ['$http', '$timeout', 'VocabularyGameFactory', ResultStoreController]);
