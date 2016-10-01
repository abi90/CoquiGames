app.directive('myAccountNav', function(){
    return {
        restrict: 'E',
        scope:{
            info: '='
        },
        templateUrl:
            'js/angular/directives/accountNav.html'
    };
});