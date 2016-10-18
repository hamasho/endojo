var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('styles', function() {
  gulp.src('apps/core/static/css/*.scss')
      .pipe(sass().on('error', sass.logError))
      .pipe(gulp.dest('apps/core/static/css/'));
});

gulp.task('default', function() {
  gulp.watch('apps/core/static/css/*.scss', ['styles']);
});
