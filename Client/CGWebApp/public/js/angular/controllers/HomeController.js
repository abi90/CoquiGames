app.controller('HomeController', ['$scope', '$http', 'storewsapi',function($scope, $http, storewsapi) {
    storewsapi.getLatestProducts().then(function(responce) {
        $scope.latest = responce.data.LatestProducts;
    });
    storewsapi.getInOfferProducts().then(function(responce) {
        $scope.specials = responce.data.SpecialProducts;
    });
    storewsapi.getProduct(1).then(function(responce) {
        $scope.product = responce.data;
    });

}]);