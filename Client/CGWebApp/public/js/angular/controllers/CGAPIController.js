app.controller('CGAPIController', ['$scope', 'cgapi', '$routeParams', function($scope, cgapi, $routeParams) {
    cgapi.success(function(data) {
        $scope.testApi = data;
    });
    $http.get('https://cgwsapi.herokuapp.com/store/latestproduct')
        .success(function (data) {
            $scope.latest = data.LatestProducts;
        })
        .error(function () {
            return {error: '404'};
        });
}]);

