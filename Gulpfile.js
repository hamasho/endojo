var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');

gulp.task('styles', function() {
  gulp.src('apps/core/static/css/*.scss')
      .pipe(sass().on('error', sass.logError))
      .pipe(gulp.dest('apps/core/static/css/'));
});

gulp.task('minify-vocabulary', function() {
  gulp.src([
    'apps/core/static/components/angular/angular.js',
    'apps/core/static/components/angular-sanitize/angular-sanitize.js',
    'apps/core/static/components/angular-animate/angular-animate.js',
    'apps/core/static/components/angular-ui-router/release/angular-ui-router.js',
    'apps/core/static/components/angular-bootstrap/ui-bootstrap-tpls.js',
    'apps/core/static/components/jsdiff/diff.js',
    'apps/core/static/js/directives.js',
    'apps/core/static/js/GameFactory.js',
    'apps/games/vocabulary/static/vocabulary/js/controllers.js',
    'apps/games/vocabulary/static/vocabulary/js/game.js',
  ])
  .pipe(concat('concat.js'))
  .pipe(gulp.dest('apps/games/vocabulary/static/vocabulary/js/'))
  .pipe(rename('uglify.js'))
  .pipe(uglify({ mangle: false }))
  .pipe(gulp.dest('apps/games/vocabulary/static/vocabulary/js/'));
});

gulp.task('minify-listening', function() {
  gulp.src([
    'apps/core/static/components/angular/angular.js',
    'apps/core/static/components/angular-sanitize/angular-sanitize.js',
    'apps/core/static/components/angular-animate/angular-animate.js',
    'apps/core/static/components/angular-ui-router/release/angular-ui-router.js',
    'apps/core/static/components/angular-bootstrap/ui-bootstrap-tpls.js',
    'apps/core/static/components/jsdiff/diff.js',
    'apps/core/static/js/directives.js',
    'apps/core/static/js/filters.js',
    'apps/core/static/js/GameFactory.js',
    'apps/games/listening/static/listening/js/controllers.js',
    'apps/games/listening/static/listening/js/game.js',
  ])
  .pipe(concat('concat.js'))
  .pipe(gulp.dest('apps/games/listening/static/listening/js/'))
  .pipe(rename('uglify.js'))
  .pipe(uglify({ mangle: false }))
  .pipe(gulp.dest('apps/games/listening/static/listening/js/'));
});

gulp.task('minify-transcription', function() {
  gulp.src([
    'apps/core/static/components/angular/angular.js',
    'apps/core/static/components/angular-sanitize/angular-sanitize.js',
    'apps/core/static/components/angular-animate/angular-animate.js',
    'apps/core/static/components/angular-ui-router/release/angular-ui-router.js',
    'apps/core/static/components/angular-bootstrap/ui-bootstrap-tpls.js',
    'apps/core/static/components/jsdiff/diff.js',
    'apps/core/static/js/directives.js',
    'apps/core/static/js/filters.js',
    'apps/core/static/js/GameFactory.js',
    'apps/games/transcription/static/transcription/js/controllers.js',
    'apps/games/transcription/static/transcription/js/game.js',
  ])
  .pipe(concat('concat.js'))
  .pipe(gulp.dest('apps/games/transcription/static/transcription/js/'))
  .pipe(rename('uglify.js'))
  .pipe(uglify({ mangle: false }))
  .pipe(gulp.dest('apps/games/transcription/static/transcription/js/'));
});

gulp.task('default', function() {
  gulp.watch('apps/core/static/css/*.scss', ['styles']);

  gulp.watch([
    'apps/core/static/js/directives.js',
    'apps/core/static/js/GameFactory.js',
    'apps/games/vocabulary/static/vocabulary/js/controllers.js',
    'apps/games/vocabulary/static/vocabulary/js/game.js',
  ], ['minify-vocabulary']);

  gulp.watch([
    'apps/core/static/js/directives.js',
    'apps/core/static/js/filters.js',
    'apps/core/static/js/GameFactory.js',
    'apps/games/listening/static/listening/js/controllers.js',
    'apps/games/listening/static/listening/js/game.js',
  ], ['minify-listening']);

  gulp.watch([
    'apps/core/static/js/directives.js',
    'apps/core/static/js/filters.js',
    'apps/core/static/js/GameFactory.js',
    'apps/games/transcription/static/transcription/js/controllers.js',
    'apps/games/transcription/static/transcription/js/game.js',
  ], ['minify-transcription']);
});

gulp.task('init', ['styles', 'minify-vocabulary', 'minify-listening', 'minify-transcription']);
