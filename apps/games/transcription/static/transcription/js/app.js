/**
 * Transcription game module
 *
 */
angular.module('TranscriptionGameApp', ['ngRoute', 'ngSanitize'])

.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

.config(function($routeProvider) {
  $routeProvider.when('/start', {
    templateUrl: 'start/',
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
 * Start game, repeat each problems and store user score to GameFactory
 */
.controller('GameController', function($scope, $http, $timeout, $location, GameFactory) {

  $scope.problems = null;
  $scope.started = false;
  $scope.getPackage = GameFactory.getSelectedPackage;

  var problemUrl = '/game/transcription/packages/' + $scope.getPackage().id + '/problems/';
  $http.get(problemUrl)
    .then(function(response) {
      $scope.problems = response.data.result;
    });

  $scope.initializeGame = function() {
    $scope.started = true;
    $scope.problemIndex = 0;
    $scope.form = {};
    $scope.score = [];
    for (var i = 0; i < $scope.problems.length; i++) {
      $scope.score.push({
        id: $scope.problems[i].id,
        question_text: $scope.problems[i].question_text,
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
    $scope.diffUserInput = $scope.problems[$scope.problemIndex].question_text;
    $scope.diffUserInputClass = "";
    $scope.form.userInput = '';
    startTime = new Date().getTime();
  };

  $scope.updateGameState = function() {
    var answer = $scope.problems[$scope.problemIndex].question_text;
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
        $scope.diffUserInput = GameFactory.diff(answer, input);
      }
    }
  };

  $scope.solvedProblem = function() {
    $scope.diffUserInputClass = 'game-cleared';
    endTime = new Date().getTime();
    $scope.score[$scope.problemIndex].clearTime = endTime - startTime;
    $scope.problemIndex++;
    $timeout($scope.nextProblem, 1000);
  };

  $scope.finishGame = function() {
    GameFactory.setScore($scope.score);
    $location.path('/result');
  };
})

.controller('ResultController', function($scope, GameFactory) {
  $scope.score = GameFactory.getScore();
});
