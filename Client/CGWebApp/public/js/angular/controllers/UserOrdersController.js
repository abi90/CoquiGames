/**
 * Created by abi on 12/5/16.
 */
/**
 * Created by abi on 10/12/16.
 */
app.controller('UserOrdersController', ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope){

        // Scope Variables
        $scope.userData = auth;
        $scope.userOrder = [];

        var logout = function () {

            authenticationSvc.logout()
                .then(function () {
                    $rootScope.$emit('unLogin');
                    $location.path("/login.html");
                }, function () {
                    $rootScope.$emit('unLogin');
                    $location.path("/login.html");
                });
        };

        var getUserOrder = function () {
            userwsapi.getUserOrders(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userOrder = response.data;
                },
                function () {
                    logout();
                }
            )
        };

        // Get User Data on startup
        getUserOrder();

    }]);