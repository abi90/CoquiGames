/**
 * Created by abi on 10/14/16.
 */
app.directive('cartDropDownUl', ['authenticationSvc', function(){
    return {
        restrict: 'E',
        scope:{
            info: '='
        },
        controller: 'CartController',
        templateUrl: 'js/angular/directives/cart-drop.html',

    };
}]);