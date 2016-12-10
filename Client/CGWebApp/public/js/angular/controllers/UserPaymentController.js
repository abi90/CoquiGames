/**
 * Created by abi on 12/5/16.
 */
app.controller('UserPaymentController',
    ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope', 'Popeye',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope, Popeye){

        $scope.errors = [];
        $scope.messages = [];

        // Local Functions
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

        var getUserPayments = function () {
            userwsapi.getUserPayment(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userPayment = response.data;
                },
                function () {
                    logout();
                }
            )
        };


        // Modals functions:
        $scope.shoAddPaymentModal = function() {

            // Open a modal to show the let the user add a Payment Method
            var modal = Popeye.openModal({
                controller: 'AddPaymentMethodModalController',
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
            modal.closed.then(function(response){
                if(response){
                    userwsapi.postUserPayment(auth.uid, auth.uname, auth.token, response)
                        .then(
                            function () {
                                $scope.messages[$scope.messages.length]= "Your Card was added!";
                                getUserPayments();
                            },
                            function (err) {
                                if(err.data.Errors){
                                    $scope.errors = err.data.Errors;
                                }
                                else if(err.data.Error){
                                    $scope.errors = [err.data.Error];
                                }
                                else{
                                    $scope.errors = ['Unknown Error. Please verify your internet connection.'];
                                }
                                getUserPayments();
                            }
                        );
                }
            });
        };

        $scope.removePayment = function(payment){

            userwsapi.deletePayment(auth.uid, auth.uname, auth.token, payment.cid)
                .then(
                    function () {
                        getUserPayments();
                    },
                    function (err){
                        console.log(JSON.stringify(err));
                        getUserPayments();
                    }
                );
        };

        $scope.closeErrorAlert= function(index){
            $scope.errors.splice(index,1);
        };

        $scope.closeMessageAlert= function(index){
            $scope.messages.splice(index,1);
        };

        // Get User Data on startup
        getUserPayments();

    }]);