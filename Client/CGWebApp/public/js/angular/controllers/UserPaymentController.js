/**
 * Created by abi on 12/5/16.
 */
app.controller('UserPaymentController',
    ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope', 'Popeye',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope, Popeye){

        // Local Functions
        var logout = function () {
            authenticationSvc.logout()
                .then(function () {
                    $location.path("/login.html");
                }, function () {
                    $location.path("/login.html");
                });
        };

        var getUserPayments = function () {
            userwsapi.getUserPayment(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userPayment = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                    logout();
                }
            )
        };


        // Modals functions:
        $scope.shoAddPaymentModal = function() {

            // Open a modal to show the let the user add a Payment Method
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/add-payment.html",
                resolve: {
                    auth: function ($q, authenticationSvc) {
                        var userInfo = authenticationSvc.getUserInfo();
                        if (userInfo) {
                            return $q.when(userInfo);
                        } else {
                            return $q.reject({authenticated: false});
                        }
                    }
                }
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user payments after modal is closed
            modal.closed.then(function(){

            });
        };

        // Get User Data on startup
        getUserPayments();

    }]);