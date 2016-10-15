/**
 * Created by abi on 10/12/16.
 */
app.controller('AccountController', ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope) {
        $scope.userInfo = auth;
        $scope.userData;
        $scope.userAddress;
        $scope.userOrder;
        $scope.userPayment;
        $scope.userWishlist;
        $rootScope.userCart;
        $scope.shippmentFee = 10;
        $scope.cartTotal = 0;

        $scope.logout = function () {

            authenticationSvc.logout()
                .then(function (result) {
                    $scope.userInfo = null;
                    $location.path("/login");
                }, function (error) {
                    console.log(error);
                });
        };

        var getUserAddress = function (auth) {
            userwsapi.getUserAddress(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userAddress = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUser = function (auth) {
            userwsapi.getUser(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userData = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserOrder = function (auth) {
            userwsapi.getUserOrders(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userOrder = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserPayments = function (auth) {
            userwsapi.getUserPayment(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userPayment = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserCart= function (auth) {
            userwsapi.getUserCart(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userCart = response.data;
                    $rootScope.$emit('Login');
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserWishlist= function (auth) {
            userwsapi.getUserWishlist(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userWishlist = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        $scope.getSubTotal = function(){
            var subtotal = 0;
            for(var i = 0; i < $scope.userCart.length; i++){
                var product = $scope.userCart[i];
                subtotal += (product.pprice * product.pquantity);
            }
            $scope.cartTotal = subtotal + subtotal * 0.1105 + $scope.shippmentFee;
            return subtotal;
        };
        $scope.init = function (auth) {
            $scope.userInfo = auth;
        }


        getUser(auth);
        getUserAddress(auth);
        getUserOrder(auth);
        getUserPayments(auth);
        getUserCart(auth);
        getUserWishlist(auth);

    }]);