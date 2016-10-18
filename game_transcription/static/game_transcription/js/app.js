angular.module('TranscriptionGameApp', ['ngRoute'])

.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

.config(function($routeProvider) {
  $routeProvider.when('/start', {
    templateUrl: '/game/transcription/start/',
  });

  $routeProvider.otherwise({
    templateUrl: 'packages/select/',
  });
})

.factory('gameFactory', function($http) {
  var selectedPackage = null;
  var problems = null;
  var gameScore = null;

  return {
    setPackage: function(package) {
      selectedPackage = package;
    },
    getPackage: function() {
      return selectedPackage;
    },
    setProblems: function(package) {
      $http.get('/game/transcription/packages/' + package.id + '/problems/')
        .then(function(response) {
          problems = response.data.result;
        });
    },
    getProblems: function() {
      return problems;
    },
    diff: function(str1, str2) {
      var diffs = JsDiff.diffChars(str1, str2);
      var result = '';
      for (var i = 0; i < diffs.length; i++) {
        if (( ! diffs[i].added) && ( ! diffs[i].removed)) {
          result += diffs[i].value;
        } else if (diffs[i].removed) {
          result += diffs[i].value.replace(/[a-zA-Z0-9'\.\?\!]/g, '_');
        }
      }
      return result;
    },
    setScore: function(score) {
      gameScore = score;
    },
    getScore: function() {
      return gameScore;
    },
  };
})

.controller('GameController', function($scope, $http, $timeout, gameFactory) {
  var url = 'http://localhost:8000/game/transcription/';

  $scope.packages = [];
  $scope.gamePreStart = true;

  $scope.setPackage = gameFactory.setPackage;
  $scope.getPackage = gameFactory.getPackage;
  $scope.setProblems = gameFactory.setProblems;
  $scope.getProblems = gameFactory.getProblems;
  $scope.setScore = gameFactory.setScore;
  $scope.getScore = gameFactory.getScore;

  $http.get(url + 'packages/')
    .then(function(response) {
      $scope.packages = response.data.result;
    });

  $scope.gameStarted = false;

  var startTime, endTime;

  $scope.initializeGame = function() {
    $scope.gamePreStart = false;
    $scope.gameStarted = true;
    $scope.gameIndex = 0;
    $scope.problems = $scope.getProblems();
    $scope.form = {};
    $scope.startGame();
    $scope.score = [];
    for (var i = 0; i < $scope.problems.length; i++) {
      $scope.score.push({
        id: $scope.problems[i].id,
        question_text: $scope.problems[i].question_text,
      });
    }
  };

  $scope.startGame = function() {
    if ($scope.gameIndex >= $scope.problems.length) {
      $scope.finishGame();
      return;
    }
    $scope.diffUserInput = $scope.problems[$scope.gameIndex].question_text;
    $scope.form.userInput = '';
    $scope.diffUserInputClass = "";
    startTime = new Date().getTime();
  };

  $scope.updateGameState = function() {
    var answer = $scope.problems[$scope.gameIndex].question_text;
    var input = $scope.form.userInput;
    if (input === '') {
      $scope.diffUserInput = answer;
    } else {
      if (input === answer) {
        $scope.diffUserInput = answer;
        $scope.clearGame();
      } else {
        $scope.diffUserInput = gameFactory.diff(answer, input);
      }
    }
  };

  $scope.clearGame = function() {
    $scope.form.userInput = '';
    $scope.diffUserInputClass = 'game-cleared';
    endTime = new Date().getTime();
    $scope.score[$scope.gameIndex].clearTime = endTime - startTime;
    $scope.gameIndex++;
    $timeout($scope.startGame, 1000);
  };

  $scope.finishGame = function() {
    gameFactory.setScore($scope.score);
    $scope.gameStarted = false;
    $scope.gameCleared = true;
  };
});
