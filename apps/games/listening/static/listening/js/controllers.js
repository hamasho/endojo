/**
 * ==================================================================
 * Package select controller
 * ==================================================================
 */
function PackageSelectController($http, ListeningGame) {
  this.packages = [];
  this.selectPackage = ListeningGame.setSelectedPackage;
  var that = this;
  $http.get('/game/listening/packages/')
    .then(function(response) {
      that.packages = response.data.packages;
    });
}

/**
 * ==================================================================
 * Init controller
 * ==================================================================
 */
function InitController($http, ListeningGame) {
  this.package = ListeningGame.getSelectedPackage();
  if (this.package === null) return;
  this.problems = [];
  var that = this;
  $http.get('/game/listening/packages/' + this.package.id + '/problems')
    .then(function(response) {
      that.problems = response.data.result;
      ListeningGame.setProblems(that.problems);
    });
}

/**
 * ==================================================================
 * Game controller
 * ==================================================================
 */
function GameController($http, $timeout, $interval, $location, ListeningGame) {
  this.$http = $http;
  this.$timeout = $timeout;
  this.$interval = $interval;
  this.$location = $location;
  this.gameService = ListeningGame;

  this.package = this.gameService.getSelectedPackage();
  if (this.package === null) return;
  this.problems = ListeningGame.getProblems();
  this.currentProblemIndex = 0;
  this.score = [];
  this.progress = 0;
  this.failed = false;
  this.timer = '0s';
  this.next();
}

GameController.prototype.next = function() {
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

GameController.prototype.update = function() {
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

GameController.prototype.giveUp = function() {
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

GameController.prototype.continue = function() {
  this.failed = false;
  this.next();
};

GameController.prototype.giveRightAnswer = function() {
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

GameController.prototype.finish = function() {
  this.gameService.setScore(this.score);
  this.$location.path('/result');
};

/**
 * ==================================================================
 * Result store controller
 * ==================================================================
 */
function ResultStoreController($http, ListeningGame) {
  this.score = ListeningGame.getScore();
  if (this.score === null) return;
  $http.post('/game/listening/result/store/', {
    score: this.score,
    package: ListeningGame.getSelectedPackage(),
  }).then(function(response) {});
}
