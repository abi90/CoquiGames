app.controller('HomeController', ['$scope', '$http', 'storewsapi',
    function($scope, $http, storewsapi) {
    storewsapi.getLatestProducts().then(function(responce) {
        $scope.latest = responce.data.LatestProducts;
    });
    storewsapi.getInOfferProducts().then(function(responce) {
        $scope.specials = responce.data.SpecialProducts;
    });
    storewsapi.getProduct(1).then(function(responce) {
        $scope.product = responce.data;
    });

    //$scope.userInfo = auth;
/*
    $scope.logout = function () {

        authenticationSvc.logout()
            .then(function (result) {
                $scope.userInfo = null;
                $location.path("/login.html");
            }, function (error) {
                console.log(error);
            });
    };*/

}]);