/**
 * HTML autofocus attribute doesn't work.
 * So replace the default with the following directive.
 */
function autofocusDirective($timeout) {
  return {
    restrict: 'A',
    link : function($scope, $element) {
      $timeout(function() {
        $element[0].focus();
      });
    }
  };
}

/**
 * Enable dynamic audio source.
 */
function audioDirective($sce) {
  return {
    restrict: 'A',
    scope: { code:'=' },
    replace: true,
    template: '<audio ng-src="{{url}}" controls loop autoplay></audio>',
    link: function (scope) {
      scope.$watch('src', function (newVal, oldVal) {
        if (newVal !== undefined) {
          scope.url = $sce.trustAsResourceUrl(newVal);
        }
      });
    }
  };
}
