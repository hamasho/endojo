'use strict';

/**
 * ==================================================================
 * Package select controller
 * ==================================================================
 */
function PackageSelectController($scope, $http, GameService) {
  this.packages = [];
  this.filteredPackages = [];
  this.currentPage = 1;
  this.numPerPage = 10;
  this.maxSize = 10;
  this.selectPackage = GameService.setSelectedPackage;

  var that = this;
  var setFilteredPackages = function() {
    var start = (that.currentPage - 1) * that.numPerPage;
    var end = start + that.numPerPage;
    that.filteredPackages = that.packages.slice(start, end);
  };

  $http.get('/game/listening/packages/')
    .then(function(response) {
      that.packages = response.data.packages;
      setFilteredPackages();
    });

  $scope.$watch('psc.currentPage + psc.numPerPage', setFilteredPackages);
}

/**
 * ==================================================================
 * Init controller
 * ==================================================================
 */
function InitController($http, $location, GameService) {
  this.package = GameService.getSelectedPackage();
  if (this.package === null) {
    $location.path('/select');
    return;
  }
  this.problems = [];
  var that = this;
  $http.get('/game/listening/packages/' + this.package.id + '/problems')
    .then(function(response) {
      that.problems = response.data.problems;
      GameService.setProblems(that.problems);
    });
}

/**
 * ==================================================================
 * Game controller
 * ==================================================================
 */
function ListeningGameController($http, $timeout, $interval, $location, GameService) {
  this.$http = $http;
  this.$timeout = $timeout;
  this.$interval = $interval;
  this.$location = $location;
  this.gameService = GameService;

  this.package = this.gameService.getSelectedPackage();
  if (this.package === null) {
    $location.path('/select');
    return;
  }
  this.problems = GameService.getProblems();
  this.currentProblemIndex = 0;
  this.score = [];
  this.progress = 0;
  this.failed = false;
  this.timer = '0s';
  this.next();
}

ListeningGameController.prototype.next = function() {
  if (this.currentProblemIndex >= this.problems.length) {
    this.finish();
    return;
  }
  this.currentProblem = this.problems[this.currentProblemIndex];
  this.input = '';
  this.displayedHtml = this.currentProblem.problem_text.replace(/[a-zA-Z0-9]/g, '_');
  this.displayClass = "alert-display";
  this.isRightAnswer = false;
  this.startTime = new Date().getTime();
  var that = this;
  this.intervalId = this.$interval(function() {
    var currentTime = new Date().getTime();
    that.timer = Math.round((currentTime - that.startTime) / 1000) + 's';
  }, 1000);
};

ListeningGameController.prototype.update = function() {
  var answer_text = this.currentProblem.problem_text;
  var input = this.gameService.trimSpace(this.input);
  if (input === '') {
    this.displayedHtml = answer_text.replace(/[a-zA-Z0-9]/g, '_');
    this.displayClass = 'alert-display';
  } else if (input === answer_text) {
    this.giveRightAnswer();
  } else {
    var result = this.gameService.diff(answer_text, input);
    this.displayedHtml = result[1];
    this.displayClass = result[0] ? 'alert-display' : 'alert-display-danger';
  }
};

ListeningGameController.prototype.giveUp = function() {
  this.displayedHtml = this.currentProblem.problem_text;
  this.displayClass = 'alert-display-danger';
  this.score.push({
    id: this.currentProblem.id,
    problem_text: this.currentProblem.problem_text,
    complete: false,
  });
  this.currentProblemIndex++;
  this.progress = Math.round(this.currentProblemIndex / this.problems.length * 100);
  this.$interval.cancel(this.intervalId);
  this.failed = true;
};

ListeningGameController.prototype.continue = function() {
  this.failed = false;
  this.next();
};

ListeningGameController.prototype.giveRightAnswer = function() {
  this.displayedHtml = this.currentProblem.problem_text;
  this.isRightAnswer = true;
  this.displayClass = 'alert-display-success';
  this.score.push({
    id: this.currentProblem.id,
    problem_text: this.currentProblem.problem_text,
    responseTimeMs: (new Date().getTime()) - this.startTime,
    complete: true,
  });
  this.currentProblemIndex++;
  this.progress = Math.round(this.currentProblemIndex / this.problems.length * 100);
  this.$interval.cancel(this.intervalId);
  this.$timeout(this.next.bind(this), 1000);
};

ListeningGameController.prototype.finish = function() {
  this.gameService.setScore(this.score);
  this.$location.path('/result');
};

/**
 * ==================================================================
 * Result store controller
 * ==================================================================
 */
function ResultStoreController($http, $location, GameService) {
  this.score = GameService.getScore();
  if (this.score === null) {
    $location.path('/select');
    return;
  }
  $http.post('/game/listening/result/store/', {
    score: this.score,
    package: GameService.getSelectedPackage(),
  }).then(function(response) {});
}
