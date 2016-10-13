app.controller("PlatformController", ["$scope", "$location", "storewsapi", "platformId", function ($scope, $location, storewsapi, platformId) {

    $scope.platformId = platformId;

    var getPlatform = function () {

        storewsapi.getPlatform($scope.platformId)
            .then(function (responce) {
                try{
                    $scope.platform = responce.data;
                }
                catch(err) {
                    console.log(err);
                    $location.path("/");
                }

            }, function (error) {
                console.log(error);
                $location.path("/");
            });
    };

    var getPlatformLatestProducts = function () {

        storewsapi.getPlatformLatest($scope.platformId)
            .then(function (responce) {
                try{
                    $scope.platformLatest = responce.data.Latest;
                }
                catch(err) {
                    console.log(JSON.stringify(err));
                    $location.path("/");
                }

            }, function (error) {
                console.log(JSON.stringify(error));
                $location.path("/");
            });
    };

    var getPlatformSpecialProducts = function () {

        storewsapi.getPlatformInOffer($scope.platformId)
            .then(function (responce) {
                try{
                    $scope.platformSpecials = responce.data.Specials;
                }
                catch(err) {
                    console.log(JSON.stringify(err));
                    $location.path("/");
                }

            }, function (error) {
                console.log(JSON.stringify(error));
                $location.path("/");
            });
    };
    getPlatform();
    getPlatformLatestProducts();
    getPlatformSpecialProducts();

}]);