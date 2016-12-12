/**
 * Created by abi on 12/11/16.
 */
app.directive('loading',   ['$http' ,function ($http) {
    return {
        restrict: 'E',
        replace:true,
        template: '<div><h1 class="loading text-center">LOADING</h1></div>',
        link: function (scope, element) {
            scope.$watch('Loading', function (val) {
                if (val)
                    $(element).show();
                else
                    $(element).hide();
            });
        }
    }

}]);