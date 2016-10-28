/**
 * ==================================================================
 * Package select controller.
 * ==================================================================
 */
function PackageSelectController($scope, $http, VocabularyGameFactory) {
  var that = this;
  this.packages = [];
  $http.get('/game/vocabulary/packages/')
    .then(function(response) {
      that.packages = response.data.result;
    });
  this.selectedPackage = VocabularyGameFactory.setSelectedPackage;
}

/**
 * ==================================================================
 * Initialize controller class for Vocabulary Game.
 * ==================================================================
 */
function InitController($http, VocabularyGameFactory) {
  this.words = [];
  this.state1Words = [];
  $http.get('/game/vocabulary/words/learning/')
    .then(function(response) {
      this.words = response.data.result;
      for (var i = 0; i < this.words.length; i++) {
        if (this.words[i].state === 1) {
          this.state1Words.push(this.words[i]);
        }
      }
      VocabularyGameFactory.setWords(this.words);
    });
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
  this.init();
}

VocabularyGameController.prototype.init = function() {
  this.words = this.gameService.getWords();
  this.wordQueue = this.gameService.setWordQueue(this.words);
  this.allCount = this.wordQueue.length;
  this.answeredWords = [];
  this.failedWords = [];
  this.next();
};

VocabularyGameController.prototype.next = function() {
  this.isRightAnswer = false;
  this.nextWord();
  if ( ! this.wordQueue.length) this.finish();
};

VocabularyGameController.prototype.update = function(input) {
  if (this.currentWord.word_text === input) {
    var that = this;
    this.input = '';
    this.isRightAnswer = true;
    this.$timeout(function() { that.next(); }, 1000);
  }
};

VocabularyGameController.prototype.finish = function() {
  VocabularyGameFactory.setAnsweredWords(this.answeredWords);
  VocabularyGameFactory.setFailedWords(this.failedWords);
  console.log(this.answeredWords);
  console.log(this.failedWords);
  this.$location.path('/result');
};

/**
 * Pick up a word from this.wordQueue, set to this.currentWord
 * and remove the picked word from word queue.
 */
VocabularyGameController.prototype.nextWord = function() {
  if ( ! this.wordQueue.length) return;
  var previousWord = this.currentWord;
  this.currentWord = this.wordQueue.shift();
  if (this.wordQueue.indexOf(previousWord) >= 0) {
    this.answeredWords.push(previousWord);
  }
  this.displayedText = this.currentWord.meaning;
};

/**
 * Compare a word with user input.
 * If the word start with the input string, return 'alert-success'.
 * Otherwise, 'alert-info'.
 */
VocabularyGameController.prototype.matchClass = function(input) {
  if (this.isRightAnswer)
    return 'alert-success';
  else if ( ! input && this.currentWord.word_text.startsWith(input))
    return 'alert-info';
  else
    return 'alert-danger';
};

/**
 * Set current word as failed and remove the word from word queue.
 */
VocabularyGameController.prototype.giveup = function() {
  this.failedWords.push(this.currentWord);
  this.wordQueue = this.gameService.removeWords(this.currentWord, this.wordQueue);
  this.next();
};
