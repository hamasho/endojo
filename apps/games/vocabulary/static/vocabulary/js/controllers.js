/**
 * ==================================================================
 * Package select controller.
 * ==================================================================
 */
function PackageSelectController($scope, $http, VocabularyGame) {
  var that = this;
  this.packages = [];
  $http.get('/game/vocabulary/packages/')
    .then(function(response) {
      that.packages = response.data.result;
    });
  this.selectPackage = VocabularyGame.setSelectedPackage;
}

/**
 * ==================================================================
 * Word select controller.
 * ==================================================================
 */
function WordSelectController($scope, $http, $window, VocabularyGame) {
  this.package = VocabularyGame.getSelectedPackage();
  if ( ! this.package) return;
  this.knownWords = [];
  this.unknownWords = [];
  this.event = [];
  this.unselectedWords = [];
  var that = this;

  $http.get('/game/vocabulary/packages/' + this.package.id + '/words/')
    .then(function(response) {
      that.unselectedWords = response.data.result;
    });
  this.setWordAsKnown = function() {
    var word = that.unselectedWords.shift();
    that.knownWords.unshift(word);
    that.event.unshift('known');
  };
  this.setWordAsUnknown = function() {
    var word = that.unselectedWords.shift();
    that.unknownWords.unshift(word);
    that.event.unshift('unknown');
  };
  this.undoSelection = function() {
    if ( ! that.event.length) return;
    if (that.event.shift() === 'known') {
      var knownWord = that.knownWords.shift();
      that.unselectedWords.unshift(knownWord);
    } else {
      var unknownWord = that.unknownWords.shift();
      that.unselectedWords.unshift(unknownWord);
    }
  };
  this.storeUnknownWords = function() {
    $http.post('/game/vocabulary/words/unknown/', {
      words: that.unknownWords,
    }).then(function(response) { });
  };

  /**
   * Set key down event
   */
  angular.element($window).on('keydown', function(e) {
    if (e.keyCode === 37)
      $scope.$apply(function() {
        that.setWordAsKnown();
        e.preventDefault();
      });
    else if (e.keyCode === 39)
      $scope.$apply(function() {
        that.setWordAsUnknown();
        e.preventDefault();
      });
    else if (e.keyCode === 40)
      $scope.$apply(function() {
        that.undoSelection();
        e.preventDefault();
      });
  });
}

/**
 * ==================================================================
 * Initialize controller.
 * ==================================================================
 */
function InitController($http, $timeout, VocabularyGameFactory) {
  this.words = [];
  this.state1Words = [];
  var that = this;
  $http.get('/game/vocabulary/words/learning/')
    .then(function(response) {
      that.words = response.data.result.slice(0);
      for (var i = 0; i < that.words.length; i++) {
        if (that.words[i].state === 1) {
          that.state1Words.push(that.words[i]);
        }
      }
      VocabularyGameFactory.setWords(that.words);
      console.log(that.state1Words);
    });

  this.update = function(idx) {
    var word = this.state1Words[idx];
    if (word.input === word.word_text) {
      word.correct = true;
      $timeout(function() { word.input = ''; }, 500);
    }
  };
}

/**
 * ==================================================================
 * Main controller class for Vocabulary Game.
 * ==================================================================
 *
 * First, init() method is called.
 * Each time user inputs a character, update(input) method is invoked.
 * If there is no word remaining, finish() is called.
 *
 * a `word` object has the following properties:
 * word = {
 *   id: 1,
 *   word_text: 'some',
 *   meaning: <translation string in user's language>
 * }
 */
function VocabularyGameController($timeout, $location, VocabularyGameFactory) {
  this.$timeout = $timeout;
  this.$location = $location;
  this.gameService = VocabularyGameFactory;

  this.words = this.gameService.getWords();
  if ( ! this.words) {
    this.$location.path('/select');
    return;
  }
  this.wordQueue = this.gameService.setWordQueue(this.words);
  this.progress = 0;
  this.nAnswered = 0;
  this.nAllWords = this.wordQueue.length;
  this.failed = false;
  this.answeredWords = [];
  this.failedWords = [];
  this.next();
}

/**
 * Pick up a word from this.wordQueue, set to this.currentWord
 * and remove the picked word from word queue.
 */
VocabularyGameController.prototype.next = function() {
  if ( ! this.wordQueue.length) {
    this.finish();
    return;
  }
  var previousWord = this.currentWord;
  this.currentWord = this.wordQueue[0];
  this.input = '';
  this.isRightAnswer = false;
  this.displayedHtml = this.currentWord.meaning;
  this.displayClass = 'alert-display';
};

VocabularyGameController.prototype.update = function() {
  var word_text = this.currentWord.word_text;
  var input = this.gameService.trimSpace(this.input);
  if (input === '') {
    this.displayClass = 'alert-display';
  } else if (input === word_text) {
    this.giveRightAnswer();
  } else {
    var result = this.gameService.diff(word_text, input);
    this.displayClass = result[0] ? 'alert-display' : 'alert-display-danger';
  }
};

VocabularyGameController.prototype.giveUp = function() {
  this.displayedHtml = this.currentWord.word_text + '&nbsp;/&nbsp;' +
    this.currentWord.meaning;
  this.displayClass = 'alert-display-danger';
  this.failedWords.push(this.currentWord);
  this.failed = true;
  this.nAnswered++;
  this.progress = Math.round(this.nAnswered / this.nAllWords * 100);
  this.wordQueue.shift();
};

VocabularyGameController.prototype.continue = function() {
  this.failed = false;
  this.next();
};

VocabularyGameController.prototype.giveRightAnswer = function() {
  this.displayedHtml = this.currentWord.word_text + '&nbsp;/&nbsp;' +
    this.currentWord.meaning;
  this.displayClass = 'alert-display-success';
  this.isRightAnswer = true;
  this.nAnswered++;
  this.progress = Math.round(this.nAnswered / this.nAllWords * 100);
  if (this.wordQueue.length)
    this.wordQueue.shift();
  if (this.gameService.noRemainingWord(this.wordQueue, this.currentWord)) {
    this.answeredWords.push(this.currentWord);
  }
  var that = this;
  this.$timeout(function() { that.next(); }, 1000);
};

VocabularyGameController.prototype.finish = function() {
  this.gameService.setAnsweredWords(this.answeredWords);
  this.gameService.setFailedWords(this.failedWords);
  this.$location.path('/result');
};

/**
 * ==================================================================
 * Result store controller.
 * ==================================================================
 */
function ResultStoreController($http, $timeout, VocabularyGame) {
  this.words = VocabularyGame.getWords();
  this.answeredWords = VocabularyGame.getAnsweredWords();
  this.failedWords = VocabularyGame.getFailedWords();
  var result = this.answeredWords.concat(this.failedWords);
  if (this.answeredWords === null) return;
  $http.post('/game/vocabulary/result/store/', {
    result: result,
  })
  .then(function(response) { });

  this.update = function(idx) {
    var word = this.failed[idx];
    if (word.input === word.word_text) {
      word.correct = true;
      $timeout(function() { word.input = ''; }, 500);
    }
  };
}
