app.controller("PlatformController",
    ["$scope", "$location", "storewsapi", "platformId", 'authenticationSvc', 'userwsapi',
        function ($scope, $location, storewsapi, platformId, authenticationSvc, userwsapi) {

            $scope.platformId = platformId;
            $scope.slides = [];
            $scope.myInterval = 5000;
            $scope.nowWrapSlides = true;
            $scope.active = 0;

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
                    $scope.active = 0;
                },
                function(){
                    $scope.slides = [];
                    $scope.active = 0;
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

            $scope.addToCart = function (pid) {
                var userInfo = authenticationSvc.getUserInfo();
                if(userInfo){
                    userwsapi.getUserCart(userInfo.uid,userInfo.uname, userInfo.upassword).then(
                        function (response) {
                            var i;
                            var cart = response.data;
                            var product;
                            for (i = 0; i < cart.length; i++) {
                                console.log(cart[i].pid);
                                if(cart[i].pid == pid)
                                {
                                    product = cart[i];
                                    product.pquantity = product.pquantity + 1;
                                    userwsapi.putUserCart(userInfo.uid,userInfo.uname, userInfo.upassword, product)
                                        .then(function (response) {console.log(JSON.stringify(response));},function (err){});
                                    break;
                                }
                            }
                            if(!product){
                                userwsapi.postUserCart(userInfo.uid,userInfo.uname, userInfo.upassword,{"pid":pid,"pquantity":1})
                                    .then(function (response) {},function (err){});
                            }
                            $rootScope.$emit('uCart');
                        },
                        function () {
                            $location.path('/404.html');
                        }
                    );
                }
                else{
                    $location.path('/login.html');
                }
            };




            getPlatform();
            getPlatformLatestProducts();
            getPlatformSpecialProducts();
            getPlatformTopProducts();

        }]);