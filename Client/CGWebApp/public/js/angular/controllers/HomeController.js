app.controller('HomeController',
    ['$scope', 'storewsapi', 'addToUserCart', '$rootScope',
    function($scope, storewsapi, addToUserCart, $rootScope) {

        $scope.slides = [];
        $scope.myInterval = 5000;
        $scope.nowWrapSlides = true;
        $scope.active = 0;
        $scope.tops = [];
        $scope.latest = [];
        $scope.specials = [];
        $scope.Loading = true;

        var getLatestProducts = function () {
            storewsapi.getLatestProducts().then(
                function(response) {
                    $scope.latest = response.data;
                },
                function (error) {
                    console.log(error.toString());
                    $scope.latest = [];
                });
        };

        var getHomeAnnouncements = function () {
            storewsapi.getHomeAnnouncements().then(
                function(response){
                    $scope.slides = response.data;
                    $scope.active = 0;
                },
                function(){
                    $scope.slides = [];
                }

            );
        };

        var getSpecialProducts = function () {
            storewsapi.getInOfferProducts().then(
                function(response) {
                    $scope.specials = response.data;
                },
                function () {
                    $scope.specials = [];
                });
        };

        var getTopProducts = function() {
            if ($scope.specials.length == 0 || $scope.latest.length == 0) {
                storewsapi.topProducts().then(
                    function (response) {
                        $scope.tops = response.data;
                    },
                    function () {
                        $scope.tops = [];
                    });
            }
        };

        var init = function () {
            $scope.Loading = true;
            getHomeAnnouncements();
            getLatestProducts();
            getSpecialProducts();
            getTopProducts();
            $scope.Loading = false;
        };

        $scope.addToCart = function (pid) {
            if(addToUserCart.addProductWithQty(pid, 1)){
                $rootScope.$broadcast('uCart');
            }
        };

        init();

    }]);