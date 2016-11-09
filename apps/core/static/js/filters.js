/**
 * Convert ms time to second.
 * 1980 => 2.0s
 * 3230 => 3.2s
 */
function timeFilter() {
  return function(input) {
    return (input / 1000).toFixed(1) + 's';
  };
}

/**
 * Trust resource URL
 */
function trustedFilter($sce) {
  return function(url) {
    return $sce.trustAsResourceUrl(url);
  };
}
