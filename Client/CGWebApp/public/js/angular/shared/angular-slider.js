angular.module('ui.bootstrap.demo', ['ngAnimate', 'ngSanitize', 'ui.bootstrap']);
angular.module('ui.bootstrap.demo').controller('CarouselDemoCtrl', function ($scope) {
    $scope.myInterval = 5000;
    $scope.noWrapSlides = false;
    $scope.active = 0;
    var slides = $scope.slides = [];
    var currIndex = 0;

    $scope.addSlide = function() {
        var imgCounter = currIndex +1;
        slides.push({
            image: 'images/slider-imgs/slide'+ imgCounter +'-img.jpg',
            text: ['Promo 1','Promo 2'][slides.length % 2],
            id: currIndex++
        });
    };
    var size = 4;
    for (var i = 0; i < size; i++) {
        $scope.addSlide();
    }

});
