/**
 * Created by abi on 10/14/16.
 */
app.directive('mainHeader', function(){
    return {
        restrict: 'E',
        scope:{
            info: '='
        },
        templateUrl:
            'js/angular/directives/header.html'
    };
});