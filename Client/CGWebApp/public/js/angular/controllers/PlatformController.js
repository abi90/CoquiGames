app.controller("PlatformController", ["$scope", "$location", "storewsapi", "platformId", function ($scope, $location, storewsapi, platformId) {

    $scope.platformId = platformId;
    $scope.slides = [];
    $scope.myInterval = 5000;
    $scope.nowWrapSlides = true;
    $scope.active ;

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

    storewsapi.getPlatformAnnouncements($scope.platformId).then(
        function(response){
            $scope.slides = response.data;
            $scope.active =0;
        },
        function(error){
            console.log(error.toString());
            $scope.slides = [];
        }


    );

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