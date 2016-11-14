app.controller("PlatformController", ["$scope", "$location", "storewsapi", "platformId", function ($scope, $location, storewsapi, platformId) {

    $scope.platformId = platformId;

    var getPlatform = function () {

        storewsapi.getPlatform($scope.platformId).then(
            function (response) {
                $scope.platform = response.data;
            },
            function (error) {
                console.log(error.toString());
                $location.path("/404.html");
            });
    };

    var getPlatformLatestProducts = function () {

        storewsapi.getPlatformLatest($scope.platformId).then(
            function (response) {
                $scope.platformLatest = response.data;
            },
            function (error) {
                console.log(error.toString());
                $scope.platformLatest = [];
            });
    };

    var getPlatformSpecialProducts = function () {

        storewsapi.getPlatformInOffer($scope.platformId)
            .then(function (response) {
                $scope.platformSpecials = response.data;

            }, function (error) {
                console.log(error.toString());
                $scope.platformSpecials = [];
            });
    };

    var getPlatformTopProducts = function () {

        storewsapi.topPlatProducts($scope.platformId)
            .then(function (response) {
                $scope.platformTop = response.data;

            }, function (error) {
                console.log(error.toString());
                $scope.platformTop = [];
            });
    };


    getPlatform();
    getPlatformLatestProducts();
    getPlatformSpecialProducts();
    getPlatformTopProducts();

}]);