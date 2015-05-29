var gulp = require('gulp'),
    clean = require('gulp-clean');

// 清理静态资源库
gulp.task('clean-lib', function(done) {
    gulp.src('./app/assets/lib')
        .pipe(clean());

    setTimeout(done, 100);
});

// 复制静态资源库
gulp.task('copy-lib', ['clean-lib'], function(done) {
    gulp.src('./bower_components/jquery/dist/**/*')
        .pipe(gulp.dest('./app/assets/lib/jquery/'));
    gulp.src('./bower_components/bootstrap/dist/**/*')
       .pipe(gulp.dest('./app/assets/lib/bootstrap/'));
    gulp.src('./bower_components/jquery-validation/dist/**/*')
       .pipe(gulp.dest('./app/assets/lib/jquery.validate/'));
    gulp.src('./bower_components/font-awesome/css/*')
        .pipe(gulp.dest('./app/assets/lib/font-awesome/css/'));
    gulp.src('./bower_components/font-awesome/fonts/**/*')
        .pipe(gulp.dest('./app/assets/lib/font-awesome/fonts/'));

    setTimeout(done, 100);
});

// 清除发布目录
gulp.task('clean-dist', function(done) {
    gulp.src('./dist/*')
        .pipe(clean());

    setTimeout(done, 100);
});

// 发布应用文件
gulp.task('dist', ['copy-lib', 'clean-dist'], function() {
    gulp.src(['requirements.txt', 'wsgi.py', './deploy/gunicorn.conf'])
        .pipe(gulp.dest('./dist/'));
    gulp.src('./app/**/*')
        .pipe(gulp.dest('./dist/app/'));
    gulp.src('./config/**/*')
        .pipe(gulp.dest('./dist/config/'));
});

// 默认任务
gulp.task('default', ['dist'], function() {
    console.log('Run dist task');
});