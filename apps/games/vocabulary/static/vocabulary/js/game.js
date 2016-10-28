/**
 * Vocabulary game module
 */
angular.module('VocabularyGameApp', ['ngRoute', 'ngAnimate', 'ngSanitize'])

.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

/**
 * Router
 */
.config(function($routeProvider) {
  $routeProvider.when('/words', {
    templateUrl: 'packages/words/select/',
  });
  $routeProvider.when('/start', {
    templateUrl: 'start/',
  });
  $routeProvider.when('/main', {
    templateUrl: 'main/',
  });
  $routeProvider.when('/result', {
    templateUrl: 'result/',
  });
  $routeProvider.otherwise({
    templateUrl: 'packages/select/',
  });
})

.factory('VocabularyGameFactory', VocabularyGameFactory)

.directive('autofocus', ['$timeout', function($timeout) {
  return {
    restrict: 'A',
    link : function($scope, $element) {
      $timeout(function() {
        $element[0].focus();
      });
    }
  };
}])

.controller('PackageSelectController', ['$scope', '$http', 'VocabularyGameFactory', PackageSelectController])

/**
 * Select unknown words
 */
.controller('WordSelectController', function($scope, $http, $window, VocabularyGameFactory) {
  var package = VocabularyGameFactory.getSelectedPackage();
  $scope.knownWords = [];
  $scope.unknownWords = [];
  $http.get('/game/vocabulary/packages/' + package.id + '/words/')
    .then(function(response) {
      $scope.unselectedWords = response.data.result;
    });

  $scope.setWordAsKnown = function() {
    var word = $scope.unselectedWords.shift();
    $scope.knownWords.unshift(word);
  };
  $scope.setWordAsUnknown = function() {
    var word = $scope.unselectedWords.shift();
    $scope.unknownWords.unshift(word);
  };

  angular.element($window).on('keydown', function(e) {
    if (e.keyCode === 37) {        // left arrow
      $scope.$apply(function() {
        $scope.setWordAsKnown();
      });
    } else if (e.keyCode === 39) { // right arrow
      $scope.$apply(function() {
        $scope.setWordAsUnknown();
      });
    } else if (e.keyCode === 40) { // down arrow
    }
  });

  $scope.storeUnknownWords = function() {
    $http.post('/game/vocabulary/words/unknown/', {
      words: $scope.unknownWords,
    })
    .then(function(response) {
    });
  };
})

.controller('InitController', ['$http', 'VocabularyGameFactory', InitController])

/**
 * Start game, repeat each problems and store user score
 */
.controller('VocabularyGameController', ['$timeout', '$location', 'VocabularyGameFactory', VocabularyGameController])

.controller('ResultController', function($scope, $http, ListeningGameFactory) {
  $scope.score = ListeningGameFactory.getScore();
  if ($scope.score === null) return;
  $http.post('/game/listening/result/store/', {
    score: $scope.score,
  })
  .then(function(response) {
  });
});
