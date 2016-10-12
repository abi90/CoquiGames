app.controller('CGAPIController', ['$scope', 'storewsapi', '$routeParams', function($scope, storewsapi, $routeParams) {
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

