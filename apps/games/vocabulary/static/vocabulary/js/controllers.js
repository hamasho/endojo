/**
 * ==================================================================
 * Main controller for Vocabulary game.
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
function VocabularyGameController($timeout, VocabularyGameFactory) {
  this.gameService = VocabularyGameFactory;
  this.$timeout = $timeout;
  this.init();
}

VocabularyGameController.prototype.init = function() {
  this.words = this.gameService.getWords();
  var problems = this.words.concat(this.words).concat(this.words);
  this.wordQueue = this.gameService.shuffle(problems);
  this.wordDisplay = Array(6).fill(null);
  this.setWord();
};

VocabularyGameController.prototype.update = function(input) {
  // Check if input text matches with one of displayed word,
  var idx = this.wordDisplay.map(function(word) {
    return word ? word.word_text : null;
  }).indexOf(input);
  if (idx >= 0) {
    var that = this;
    this.input = '';
    this.$timeout(function() {
      that.wordDisplay[idx] = null;
      if ( ! that.wordQueue.length) that.finish();
      that.setWord();
    }, 500);
  }
};

VocabularyGameController.prototype.finish = function() {
  VocabularyGameFactory.setFailedWord(this.score);
  this.$location.path('/result');
};

/**
 * Pick up a word from this.wordQueue and set to this.wordDisplay.
 * There must be no duplicated words in display.
 * If the first word in this.wordQueue already exists in this.wordDisplay,
 * the next word is tried to put in display, and so forth.
 * If all words in word queue are already exist in display, do nothing.
 * The picked up word is removed from this.wordQueue.
 */
VocabularyGameController.prototype.setWord = function() {
  if ( ! this.wordQueue.length) return;
  for (var i = 0; i < this.wordQueue.length; i++) {
    if (this.wordDisplay.indexOf(this.wordQueue[i]) >= 0) continue;
    var idx = this.wordDisplay.indexOf(null);
    if (this.wordDisplay.indexOf(null) >= 0) {
      this.wordDisplay[idx] = this.wordQueue[i];
      this.wordQueue.splice(i, 1);
      i--;
    }
  }
};

/**
 * Compare a word with user input.
 * If the word start with the input string, return 'alert-success'.
 * Otherwise, 'alert-info'.
 */
VocabularyGameController.prototype.matchClass = function(word, input) {
  if ( ! word || ! input)
    return 'alert-info vocabulary-word-match';
  else if (word.word_text.startsWith(input))
    return 'alert-success vocabulary-word-match';
  else
    return 'alert-info vocabulary-word-match';
};
