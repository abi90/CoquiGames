/**
 * Created by abi on 12/5/16.
 */
/**
 * Created by abi on 10/12/16.
 */
app.controller('UserAddressController',
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

        var getUserBillingAddress= function () {
            userwsapi.getUserBillingAddress(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userBillingAddress = response.data;
                },
                function () {
                    $scope.userBillingAddress = [];
                    logout();
                }
            )

        };

        var getUserShippingAddress= function () {
            userwsapi.getUserShippingAddress(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userShippingAddress = response.data;
                },
                function () {
                    $scope.userShippingAddress = [];
                    logout();
                }
            )

        };

        // Modals functions:
        $scope.shoPreferredShpAddModal = function() {

            // Open a modal to show the user address
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/change_shipping_address_modal.html",
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

            // Update user selected address after modal is closed
            modal.closed.then(function() {

            });
        };

        $scope.shoEditShpAddModal = function(shipping_address) {

            // Open a modal to edit ship add
            var modal = Popeye.openModal({
                controller: 'EditSAModalController as modalCtrl',
                templateUrl: "js/angular/modals/edit-shipping-address.html",
                resolve: {
                    shipping_address: function () {
                        return shipping_address;
                    }
                }
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(value) {
                console.log(JSON.stringify(value));
                var changed = shipping_address===value;
                if(!changed){
                    userwsapi.putUserAddress(auth.uid, auth.uname, auth.token, value)
                        .then(function (response) {

                        }, function (error) {

                        });
                }
                getUserShippingAddress();
                getUserBillingAddress();
            });
        };

        $scope.shoAddShpAddModal = function() {

            // Open a modal to add a ship add
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/add-shipping-address.html",
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

            // Update user selected address after modal is closed
            modal.closed.then(function() {

            });
        };

        $scope.shoAddBilAddModal = function() {

            // Open a modal to add a bil address
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/add-billing-address.html",
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

            // Update user selected address after modal is closed
            modal.closed.then(function() {

            });
        };

        $scope.shoEditBilAddModal = function() {

            // Open a modal to edit user bil add
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/edit-billing-address.html",
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

            // Update user selected address after modal is closed
            modal.closed.then(function() {

            });
        };

        // Get User Data on startup
        getUserBillingAddress();
        getUserShippingAddress();


    }]);