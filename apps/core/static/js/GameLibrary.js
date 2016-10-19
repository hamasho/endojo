/**
 * Factory to serve functionalities for game
 */
var GameFactory = function($http, $sce) {

  var packages = null;
  var selectedPackage = null;
  var gameScore = null;

  return {
    selectPackage: function(package) {
      selectedPackage = package;
    },
    getSelectedPackage: function() {
      return selectedPackage;
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
      var result = '';
      for (var i = 0; i < diffs.length; i++) {
        if (( ! diffs[i].added) && ( ! diffs[i].removed)) {
          result += '<span class="answer-correct-part">' + diffs[i].value + '</span>';
        } else if (diffs[i].removed) {
          result += '<span class="answer-blank-part">' +
            diffs[i].value.replace(/[a-zA-Z0-9'\.\?\!]/g, '_') + '</span>';
        } else if (diffs[i].added) {
          result += '<span class="answer-incorrect-part">' + diffs[i].value + '</span>';
        }
      }
      return $sce.trustAsHtml(result);
    },
    /**
     * Trim spaces at beginning and end of sentence.
     * Also compress continuous spaces.
     */
    trimSpace: function(str) {
      return str.replace(/^ */, '').replace(/ *$/, '').replace(/ +/g, ' ');
    },

  };

};
