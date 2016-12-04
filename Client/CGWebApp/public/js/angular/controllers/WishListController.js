/**
 * Created by abi on 12/4/16.
 */
app.controller('WishListController',['$scope', '$location', 'auth', 'authenticationSvc','userwsapi', '$rootScope',
    function ($scope, $location, auth, authenticationSvc, userwsapi, $rootScope) {
        var getWishList = function(){
            return userwsapi.getUserWishlist(auth.uid, auth.uname, auth.token)
                .then(
                    function (response) {
                        $scope.userWishlist = response.data;
                    },
                    function () {
                        $location.path("/404.html");
                        $scope.logout();
                    }
                );
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

        $scope.deleteFromWishList = function (pid) {
            var userInfo = authenticationSvc.getUserInfo();
            if(userInfo){
                userwsapi.delUserWishList(userInfo.uid, userInfo.uname, userInfo.upassword, pid)
                    .then(
                        function (){
                            getWishList();
                        },
                        function () {
                            $location.path("/404.html");
                            $scope.logout();
                        }
                    );
            }
            else{
                $location.path('/login.html');
            }
        };

        getWishList();


    }]);