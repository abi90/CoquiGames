/**
 * Created by jesmarie on 10-12-16.
 */
app.controller('ProductController',
    ['$scope', '$location', 'storewsapi', 'authenticationSvc', 'userwsapi','productId', '$rootScope',
    function($scope, $location, storewsapi, authenticationSvc, userwsapi, productId, $rootScope) {

        $scope.productId = productId;
        $scope.Loading = false;

        var getProduct = function () {
            $scope.Loading = true;
            storewsapi.getProduct($scope.productId).then(
                function (response) {
                    $scope.product = response.data;
                },
                function (error) {
                    console.log(error.toString());
                    $location.path("/404.html");
                });

            storewsapi.relatedProducts($scope.productId).then(
                function (response) {
                    $scope.relatedPrds = response.data;
                },
                function (error) {
                    console.log(error.toString());
                    $scope.relatedPrds = [];
                }
            );
            $scope.Loading = false;
        };

        storewsapi.getProductAltImg($scope.productId).then(
            function (response){
                $scope.altImgs = response.data;
            },
            function (err)
            {
                console.log(err.data.toString());
                $scope.altImgs = [];
            });

        $scope.addProductToCart = function () {
            var userInfo = authenticationSvc.getUserInfo();
            if(userInfo){
                userwsapi.getUserCart(userInfo.uid, userInfo.uname, userInfo.upassword)
                    .then(
                        function (response) {
                            var i;
                            var cart = response.data;
                            var product;
                            for (i = 0; i < cart.length; i++) {
                                console.log(cart[i].pid);
                                if(cart[i].pid == $scope.productId)
                                {
                                    product = cart[i];
                                    product.pquantity = product.pquantity + 1;
                                    userwsapi.putUserCart(userInfo.uid,userInfo.uname, userInfo.upassword, product)
                                        .then(function (response) {console.log(JSON.stringify(response));},
                                            function (err){});
                                    break;
                                }
                            }
                            if(!product){
                                userwsapi.postUserCart(userInfo.uid,userInfo.uname,
                                    userInfo.upassword,{"pid": $scope.productId,"pquantity":1})
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

        $scope.addRelatedProductToCart = function (pid) {
            var userInfo = authenticationSvc.getUserInfo();
            if(userInfo){
                userwsapi.getUserCart(userInfo.uid, userInfo.uname, userInfo.upassword)
                    .then(
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
                                        .then(function (response) {console.log(JSON.stringify(response));},
                                            function (err){});
                                    break;
                                }
                            }
                            if(!product){
                                userwsapi.postUserCart(userInfo.uid,userInfo.uname,
                                    userInfo.upassword,{"pid": pid,"pquantity":1})
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

        $scope.addProductToWishList = function () {
            var userInfo = authenticationSvc.getUserInfo();
            if(userInfo){
                userwsapi.getUserWishlist(userInfo.uid, userInfo.uname, userInfo.upassword)
                    .then(
                        function (response) {
                            var i;
                            var wishList = response.data;
                            var product;
                            for (i = 0; i < wishList.length; i++) {
                                if(wishList[i].pid == $scope.productId)
                                {
                                    product = wishList[i];
                                    break;
                                }
                            }
                            if(!product){
                                userwsapi.postUserWishList(userInfo.uid,userInfo.uname,
                                    userInfo.upassword, $scope.productId)
                                    .then(
                                        function (response) {
                                            console.log(JSON.toString(response.data));
                                        },
                                        function (err){console.log(JSON.toString(err))});
                            }
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

        $scope.addRelatedProductToWishList = function (pid) {
            var userInfo = authenticationSvc.getUserInfo();
            if(userInfo){
                userwsapi.getUserCart(userInfo.uid, userInfo.uname, userInfo.upassword)
                    .then(
                        function (response) {
                            var i;
                            var cart = response.data;
                            var product;
                            for (i = 0; i < cart.length; i++) {
                                console.log(cart[i].pid);
                                if(cart[i].pid == pid)
                                {
                                    product = cart[i];
                                    break;
                                }
                            }
                            if(!product){
                                userwsapi.postUserCart(userInfo.uid,userInfo.uname,
                                    userInfo.upassword, pid)
                                    .then(function (response) {},function (err){});
                            }
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

        getProduct();
    }]);