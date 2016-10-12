app.controller('HomeController', ['$scope', '$http', 'cgapi',function($scope,$http, cgapi) {
    cgapi.getLatestProducts.then(function(data) {
        $scope.latest = data.data.LatestProducts;
    });
    cgapi.getInOfferProducts.then(function(data) {
        $scope.specials = data.data.SpecialProducts;
    });

}]);