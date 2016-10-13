/**
 * Created by abi on 10/12/16.
 */
app.controller('AccountController', ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi',
    function ($scope, $location, authenticationSvc, auth, userwsapi) {
        $scope.userInfo = auth;
        $scope.userData;
        $scope.userAddress;
        $scope.userOrder;
        $scope.userPayment;

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
                    $scope.userPayment = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        getUser(auth);
        getUserAddress(auth);
        getUserOrder(auth);
        getUserPayments(auth);
        getUserCart(auth);
    }]);