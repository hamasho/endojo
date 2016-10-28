/**
 * Vocabulary game's factory
 */
var VocabularyGameFactory = function($http, $sce) {

  var packages = null;
  var selectedPackage = null;
  var words = null;
  var gameScore = null;
  var answeredWords = null;
  var failedWords = null;

  return {
    setSelectedPackage: function(package) { selectedPackage = package; },
    getSelectedPackage: function() { return selectedPackage; },
    setWords: function(ws) { words = ws; },
    getWords: function() { return words; },
    setAnsweredWords: function(words) { answeredWords = words; },
    getAnsweredWords: function() { return answeredWords; },
    setFailedWords: function(words) { failedWords = words; },
    getFailedWords: function() { return failedWords; },

    setWordQueue: function(words) {
      return words.concat(words).concat(words);
    },
    removeWords: function(word, queue) {
      queue = queue.slice(0); // copy value
      var idx;
      while ((idx = queue.indexOf(word)) >= 0) {
        queue.splice(idx, 1);
      }
      return queue;
    },
  };
};
