app.controller("PlatformController", ["$scope", "$location", "storewsapi", "platformId", function ($scope, $location, storewsapi, platformId) {

    $scope.platformId = platformId;

    var getPlatform = function () {

        storewsapi.getPlatform($scope.platformId)
            .then(function (responce) {
                try{
                    $scope.platform = responce.data;
                }
                catch(err) {
                    console.log(JSON.toString(err));
                    $location.path("/404.html");
                }

            }, function (error) {
                console.log(JSON.stringify(error));
                $location.path("/404.html");
            });
    };

    var getPlatformLatestProducts = function () {

        storewsapi.getPlatformLatest($scope.platformId)
            .then(function (responce) {
                try{
                    $scope.platformLatest = responce.data;
                }
                catch(err) {
                    console.log(JSON.toString(err));
                    $location.path("/404.html");
                }

            }, function (error) {
                console.log(JSON.toString(error));
                $location.path("/404.html");
            });
    };

    var getPlatformSpecialProducts = function () {

        storewsapi.getPlatformInOffer($scope.platformId)
            .then(function (responce) {
                try{
                    $scope.platformSpecials = responce.data;
                }
                catch(err) {
                    console.log(JSON.toString(err));
                    $location.path("/404.html");
                }

            }, function (error) {
                console.log(JSON.toString(error));
                $location.path("/404.html");
            });
    };

    getPlatform();
    getPlatformLatestProducts();
    getPlatformSpecialProducts();

}]);