/**
 * Vocabulary game module
 */
angular.module('VocabularyWordSelectApp', ['ngRoute', 'ngAnimate', 'ngSanitize'])

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

.directive('audios', function($sce) {
  return {
    restrict: 'A',
    scope: { code:'=' },
    replace: true,
    template: '<audio ng-src="{{url}}" controls loop autoplay></audio>',
    link: function (scope) {
      scope.$watch('src', function (newVal, oldVal) {
        if (newVal !== undefined) {
          scope.url = $sce.trustAsResourceUrl(newVal);
        }
      });
    }
  };
})

.filter('timeFilter', function() {
  return function(input) {
    return (input / 1000).toFixed(1) + 's';
  };
})

/**
 * Select package and store it to VocabularyGameFactory
 */
.controller('PackageSelectController', function($scope, $http, VocabularyGameFactory) {
  $scope.packages = null;
  var url = '/game/vocabulary/packages/';
  $http.get(url)
    .then(function(response) {
      $scope.packages = response.data.result;
    });
  $scope.selectPackage = VocabularyGameFactory.selectPackage;
})

/**
 * Download and set problems
 */
.controller('InitializeController', function($scope, $http, VocabularyGameFactory) {
  $scope.package = VocabularyGameFactory.getSelectedPackage();
  if ($scope.package === null) return;
  $scope.problems = null;
  $scope.title = $scope.package.title;
  var problemUrl = '/game/vocabulary/packages/' + $scope.package.id + '/problems/';
  $http.get(problemUrl)
    .then(function(response) {
      $scope.problems = response.data.result;
      VocabularyGameFactory.setProblems($scope.problems);
    });
})

/**
 * Start game, repeat each problems and store user score to VocabularyGameFactory
 */
.controller('GameController', function($scope, $http, $timeout, $interval, $location, $animate, VocabularyGameFactory) {

  $scope.package = VocabularyGameFactory.getSelectedPackage();
  if ($scope.package === null) return;
  $scope.problems = VocabularyGameFactory.getProblems();
  $scope.started = false;
  $scope.cleared = false;
  $scope.title = $scope.package.title;

  $scope.initializeGame = function() {
    $scope.started = true;
    $scope.problemIndex = 0;
    $scope.form = {};
    $scope.score = [];
    $scope.progress = 0;
    for (var i = 0; i < $scope.problems.length; i++) {
      $scope.score.push({
        id: $scope.problems[i].id,
        problem_text: $scope.problems[i].problem_text,
      });
    }
    $scope.nextProblem();
  };

  var startTime, endTime, intervalId;

  $scope.nextProblem = function() {
    if ($scope.problemIndex >= $scope.problems.length) {
      $scope.finishGame();
      return;
    }
    $scope.diffUserInput = '__';
    $scope.diffUserInputClass = "alert alert-info";
    $scope.form.userInput = '';
    $scope.audio_url = $scope.problems[$scope.problemIndex].url;
    console.log($scope.audio_url);
    $scope.cleared = false;
    $scope.timer = '0s';
    startTime = new Date().getTime();
    intevalId = $interval(function() {
      $scope.timer = Math.round((new Date().getTime() - startTime) / 1000) + 's';
    }, 1000);
  };

  $scope.updateGameState = function() {
    var answer = $scope.problems[$scope.problemIndex].problem_text;
    var input = VocabularyGameFactory.trimSpace($scope.form.userInput);
    /**
     * If the user doesn't input any characters, then show the problem.
     * Otherwise, show the diff of the correct answer and user input.
     * If the user input is the correct answer, then finish this problem.
     */
    if (input === '') {
      $scope.diffUserInput = '__';
    } else {
      if (input === answer) {
        $scope.diffUserInput = answer;
        $scope.solvedProblem();
      } else {
        result = VocabularyGameFactory.diff(answer, input);
        $scope.diffUserInput = result[1];
        $scope.diffUserInputClass = (result[0] ? 'alert alert-info' : 'alert alert-danger');
      }
    }
  };

  $scope.solvedProblem = function() {
    $scope.cleared = true;
    $scope.diffUserInputClass = 'alert alert-success game-cleared';
    endTime = new Date().getTime();
    $scope.score[$scope.problemIndex].responseTimeMs = endTime - startTime;
    $scope.problemIndex++;
    $scope.progress = Math.round($scope.problemIndex / $scope.problems.length * 100);
    $interval.cancel(intervalId);
    $timeout($scope.nextProblem, 1000);
  };

  $scope.finishGame = function() {
    VocabularyGameFactory.setScore($scope.score);
    $location.path('/result');
  };

  /**
   * Start game!
   */
  $scope.initializeGame();
})

.controller('ResultController', function($scope, $http, VocabularyGameFactory) {
  $scope.score = VocabularyGameFactory.getScore();
  if ($scope.score === null) return;
  $http.post('/game/vocabulary/result/store/', {
    score: $scope.score,
  })
  .then(function(response) {
  });
});
