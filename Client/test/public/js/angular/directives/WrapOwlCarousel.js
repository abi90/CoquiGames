app.directive("owlCarousel", function() {
    return {
        restrict: 'E',
        transclude: false,
        link: function (scope) {
            scope.initCarousel = function(element) {
                // provide any default options you want
                var defaultOptions = {
                };
                //var customOptions = scope.$eval($(element).attr('data-options'));
                var customOptions = {
                    autoPlay: false, //Set AutoPlay to 3 seconds
                    items : 3,
                    stopOnHover : true,
                    navigation : true, // Show next and prev buttons
                    pagination : false,
                    navigationText : ["<span class='glyphicon glyphicon-chevron-left'></span>","<span class='glyphicon glyphicon-chevron-right'></span>"]
                };
                // combine the two options objects
                for(var key in customOptions) {
                    defaultOptions[key] = customOptions[key];
                }
                // init carousel
                $(element).owlCarousel(defaultOptions);
            };
        }
    };
})
.directive('owlCarouselItem', [function() {
    return {
        restrict: 'A',
        transclude: false,
        link: function(scope, element) {
            // wait for the last item in the ng-repeat then call init
            if(scope.$last) {
                scope.initCarousel(element.parent());
            }
        }
    };
}]);