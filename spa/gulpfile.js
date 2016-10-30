var gulp = require('gulp');
var jade = require('gulp-jade');
var concat = require('gulp-concat');
var path = require('path');

gulp.task('default', ['templates']);

gulp.task('templates', function() {
  gulp
    .src('./templates/*.jade')
    .pipe(jade({
      client: true,
      callbackName: templateName
    }))
    .pipe(concat('template.js'))
    .pipe(gulp.dest('./js'))
});

function templateName(filepath) {
    return 'render' + path.basename(filepath).replace('.js', '');
}