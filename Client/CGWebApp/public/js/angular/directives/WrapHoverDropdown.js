/**
 * Created by abi on 10/12/16.
 */
app.directive("dropdownHover", function() {
    return {
        restrict: 'E',
        transclude: false,
        link: function (scope) {
            scope.initHoverDrop = function(element) {
                var defaultOptions = {
                    delay: 10, //Set AutoPlay to 3 seconds
                    instantlyCloseOthers: true,
                    hoverDelay: 10
                };
                // init dropdown
                $(element).dropdownHover(defaultOptions);
            };
        }
    };
})