app.controller("PlatformController",
    ["$scope", "$location", "storewsapi", "platformId", 'addToUserCart', 'addToWishList',
        function ($scope, $location, storewsapi, platformId, addToUserCart, addToWishList) {

            $scope.platformId = platformId;
            $scope.platform = {};
            $scope.slides = [];
            $scope.myInterval = 5000;
            $scope.nowWrapSlides = true;
            $scope.active = 0;
            $scope.platformTop = [];
            $scope.platformSpecials = [];
            $scope.platformLatest = [];

            var getPlatform = function () {

                storewsapi.getPlatform($scope.platformId).then(
                    function (response) {
                        $scope.platform = response.data;
                    },
                    function (){
                        $location.path("/404.html");
                    });
            };

            var getPlatformLatestProducts = function () {

                storewsapi.getPlatformLatest($scope.platformId).then(
                    function (response) {
                        $scope.platformLatest = response.data;
                    },
                    function () {
                        $scope.platformLatest = [];
                    });
            };


            var getPlatformAnnouncements = function () {
                storewsapi.getPlatformAnnouncements($scope.platformId).then(
                    function(response){
                        $scope.slides = response.data;
                        $scope.active = 0;
                    },
                    function(){
                        $scope.slides = [];
                        $scope.active = 0;
                    }
                );
            };

            var getPlatformSpecialProducts = function () {

                storewsapi.getPlatformInOffer($scope.platformId)
                    .then(function (response) {
                        $scope.platformSpecials = response.data;

                    }, function () {
                        $scope.platformSpecials = [];
                    });
            };

            var getPlatformTopProducts = function () {
                if($scope.platformLatest.length <= 2 || $scope.platformSpecials.length <= 2)
                {
                    storewsapi.topPlatProducts($scope.platformId)
                        .then(function (response) {
                            $scope.platformTop = response.data;

                        }, function (error) {
                            console.log(error.toString());
                            $scope.platformTop = [];
                        });
                }
            };

            $scope.addToCart = function (pid) {
                if(addToUserCart.addProductWithQty(pid, 1)){
                    $rootScope.$broadcast('uCart');
                }
            };

            $scope.addProductToWishList = function (pid) {
                addToWishList.addProductToWishList(pid);
            };

            getPlatform();
            getPlatformAnnouncements();
            getPlatformLatestProducts();
            getPlatformSpecialProducts();
            getPlatformTopProducts();

        }]);