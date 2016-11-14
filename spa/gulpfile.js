var gulp = require('gulp');
var sass = require('gulp-sass');
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
    .pipe(gulp.dest('./js'));
});

gulp.task('sass', function() {
  gulp
    .src('./sass/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./css'));
});

function templateName(filepath) {
    return 'render' + path.basename(filepath).replace('.js', '');
}
