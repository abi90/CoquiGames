/**
 * Created by abi on 10/14/16.
 */
app.directive('mainFooter', function(){
    return {
        restrict: 'E',
        scope:{
            info: '='
        },
        templateUrl:
            'js/angular/directives/footer.html'
    };
});