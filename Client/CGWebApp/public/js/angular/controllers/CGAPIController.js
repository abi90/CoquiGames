app.controller('CGAPIController', ['$scope', 'cgapi', '$routeParams', function($scope, cgapi, $routeParams) {
    cgapi.success(function(data) {
        $scope.testApi = data;
    });
}]);

