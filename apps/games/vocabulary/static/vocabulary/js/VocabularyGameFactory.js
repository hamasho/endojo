/**
 * Vocabulary game's factory
 */
var VocabularyGameFactory = function($http, $sce) {

  var packages = null;
  var selectedPackage = null;
  var words = null;
  var gameScore = null;

  return {
    selectPackage: function(package) {
      selectedPackage = package;
    },
    getSelectedPackage: function() {
      return selectedPackage;
    },
    setWords: function(ws) {
      words = ws;
    },
    getWords: function() {
      return words;
    },
    setScore: function(score) {
      gameScore = score;
    },
    getScore: function() {
      return gameScore;
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
              diffs[i].value.replace(/[a-zA-Z0-9'\.\?\!]/g, '_') + '</span>';
          }
        } else if (diffs[i].added) {
          correct = false;
          result += '<span class="answer-incorrect-part">' + diffs[i].value + '</span>';
        }
      }
      return [correct, $sce.trustAsHtml(result)];
    },
    /**
     * Trim spaces at beginning and end of sentence.
     * Also compress continuous spaces.
     */
    trimSpace: function(str) {
      return str.replace(/^ */, '').replace(/ *$/, '').replace(/ +/g, ' ');
    },

    /**
     * Set selected word as known
     */
    setKnown: function() {
    },
    /**
     * Set selected word as unknown
     */
    setUnknown: function() {
    },

    shuffle: function(array) {
      // TODO: implement
      return array;
    },
  };
};
