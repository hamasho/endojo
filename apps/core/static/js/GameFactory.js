/* globals JsDiff: false */
'use strict';

/**
 * Game factory
 *
 * This factory is used by all of Vocabulary, Listening and Transcription
 * games.
 */
var GameFactory = function($http, $sce) {

  var selectedPackage = null;
  var problems = null;
  var words = null;
  var answeredWords = null;
  var failedWords = null;
  var score = null;

  return {
    setSelectedPackage: function(p) { selectedPackage = p; },
    getSelectedPackage: function() { return selectedPackage; },
    setProblems: function(ps) { problems = ps; },
    getProblems: function() { return problems; },
    setWords: function(ws) { words = ws; },
    getWords: function() { return words; },
    setAnsweredWords: function(words) { answeredWords = words; },
    getAnsweredWords: function() { return answeredWords; },
    setFailedWords: function(words) { failedWords = words; },
    getFailedWords: function() { return failedWords; },
    setScore: function(s) { score = s; },
    getScore: function() { return score; },

    setWordQueue: function(words) {
      //return words.concat(words).concat(words);
      return words.slice(0);
    },
    /**
     * Trim spaces at beginning and end of sentence.
     * Also compress continuous spaces.
     */
    trimSpace: function(str) {
      return str.replace(/^ */, '').replace(/ *$/, '').replace(/ +/g, ' ');
    },
    /**
     * Calculate diff and return the result as HTML
     */
    diff: function(str1, str2) {
      var diffs = JsDiff.diffChars(str1, str2);
      var correct = true;
      var result = '';
      for (var i = 0; i < diffs.length; i++) {
        if (( ! diffs[i].added) && ( ! diffs[i].removed)) {
          result += '<span class="answer-correct-part">' + diffs[i].value + '</span>';
        } else if (diffs[i].removed) {
          if (diffs[i].value === ' ') {
            correct = false;
            result += '<span class="answer-incorrect-part">&nbsp;&nbsp;</span>';
          } else {
            correct = (i === diffs.length - 1 ? correct : false);
            result += '<span class="answer-blank-part">' +
              diffs[i].value.replace(/[a-zA-Z0-9]/g, '_') + '</span>';
          }
        } else if (diffs[i].added) {
          correct = false;
          result += '<span class="answer-incorrect-part">' + diffs[i].value + '</span>';
        }
      }
      return [correct, $sce.trustAsHtml(result)];
    },
    noRemainingWord: function(wordQueue, word) {
      for (var i = 0; i < wordQueue.length; i++) {
        if (wordQueue[i].id === word.id) {
          return false;
        }
      }
      return true;
    },
  };
};
