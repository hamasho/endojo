/**
 * Transcription game module
 *
 */
angular.module('TranscriptionGameApp', ['ngRoute', 'ngAnimate', 'ngSanitize'])

.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

.config(function($routeProvider) {
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

.factory('GameFactory', GameFactory)

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

/**
 * Select package and store it to GameFactory
 */
.controller('PackageSelectController', function($scope, $http, GameFactory) {
  $scope.packages = null;
  var url = '/game/transcription/packages/';
  $http.get(url)
    .then(function(response) {
      $scope.packages = response.data.result;
    });
  $scope.selectPackage = GameFactory.selectPackage;
})

/**
 * Download and set problems
 */
.controller('InitializeController', function($scope, $http, GameFactory) {
  $scope.package = GameFactory.getSelectedPackage();
  if ($scope.package === null) return;
  $scope.problems = null;
  $scope.title = $scope.package.title;
  var problemUrl = '/game/transcription/packages/' + $scope.package.id + '/problems/';
  $http.get(problemUrl)
    .then(function(response) {
      $scope.problems = response.data.result;
      GameFactory.setProblems($scope.problems);
    });
})

/**
 * Start game, repeat each problems and store user score to GameFactory
 */
.controller('GameController', function($scope, $http, $timeout, $location, $animate, GameFactory) {

  $scope.package = GameFactory.getSelectedPackage();
  if ($scope.package === null) return;
  $scope.problems = GameFactory.getProblems();
  $scope.started = false;
  $scope.cleared = false;
  $scope.title = $scope.package.title;

  $scope.initializeGame = function() {
    $scope.started = true;
    $scope.problemIndex = 0;
    $scope.form = {};
    $scope.score = [];
    for (var i = 0; i < $scope.problems.length; i++) {
      $scope.score.push({
        id: $scope.problems[i].id,
        problem_text: $scope.problems[i].problem_text,
      });
    }
    $scope.nextProblem();
  };

  var startTime, endTime;

  $scope.nextProblem = function() {
    if ($scope.problemIndex >= $scope.problems.length) {
      $scope.finishGame();
      return;
    }
    $scope.diffUserInput = $scope.problems[$scope.problemIndex].problem_text;
    $scope.diffUserInputClass = "alert alert-info";
    $scope.form.userInput = '';
    $scope.cleared = false;
    startTime = new Date().getTime();
  };

  $scope.updateGameState = function() {
    var answer = $scope.problems[$scope.problemIndex].problem_text;
    var input = GameFactory.trimSpace($scope.form.userInput);
    /**
     * If the user doesn't input any characters, then show the problem.
     * Otherwise, show the diff of the correct answer and user input.
     * If the user input is the correct answer, then finish this problem.
     */
    if (input === '') {
      $scope.diffUserInput = answer;
    } else {
      if (input === answer) {
        $scope.diffUserInput = answer;
        $scope.solvedProblem();
      } else {
        result = GameFactory.diff(answer, input);
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
    $timeout($scope.nextProblem, 1000);
  };

  $scope.finishGame = function() {
    GameFactory.setScore($scope.score);
    $location.path('/result');
  };

  /**
   * Start game!
   */
  $scope.initializeGame();
})

.controller('ResultController', function($scope, $http, GameFactory) {
  $scope.score = GameFactory.getScore();
  $http.post('/game/transcription/result/store/', {
    score: $scope.score,
  })
  .then(function(response) {
  });
});
