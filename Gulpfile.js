var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('styles', function() {
  gulp.src('core/static/css/*.scss')
      .pipe(sass().on('error', sass.logError))
      .pipe(gulp.dest('core/static/css/'));
});

gulp.task('default', function() {
  gulp.watch('core/static/css/*.scss', ['styles']);
});
