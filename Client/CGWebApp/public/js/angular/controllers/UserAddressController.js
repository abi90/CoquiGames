/**
 * Created by abi on 12/5/16.
 */
/**
 * Created by abi on 10/12/16.
 */
app.controller('UserAddressController',
    ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope', 'Popeye',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope, Popeye){

        $scope.uname = auth.uname;
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
        $scope.shoEditAddModal = function(address) {

            // Open a modal to edit ship add
            var modal = Popeye.openModal({
                controller: 'EditUserAddressModalController',
                templateUrl: "js/angular/modals/user-address.html",
                resolve: {address: function () {return address;}}
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(value) {
                if(value){
                    userwsapi.putUserAddress(auth.uid, auth.uname, auth.token, value)
                        .then(function () {
                            getUserShippingAddress();
                            getUserBillingAddress();
                        }, function () {
                            getUserShippingAddress();
                            getUserBillingAddress();
                        });
                }
            });
        };

        $scope.shoAddShpAddModal = function() {

            // Open a modal to add a ship add
            var modal = Popeye.openModal({
                controller: 'AddUserShAddressModalController',
                templateUrl: "js/angular/modals/user-address.html"
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Post user address after modal is closed
            modal.closed.then(function(new_address) {
                if(new_address){
                    userwsapi.postUserAddress(auth.uid, auth.uname, auth.token, new_address)
                        .then(function () {
                            getUserShippingAddress();
                            getUserBillingAddress();
                        }, function () {
                            getUserShippingAddress();
                            getUserBillingAddress();
                        });
                }

            });
        };

        $scope.shoAddBilAddModal = function() {

            // Open a modal to add a bil address
            var modal = Popeye.openModal({
                controller: 'AddUserBlAddressModalController',
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

            // Post user address after modal is closed
            modal.closed.then(function(new_address) {
                if(new_address){
                    userwsapi.postUserAddress(auth.uid, auth.uname, auth.token, new_address)
                        .then(function () {
                            getUserShippingAddress();
                            getUserBillingAddress();
                        }, function (err) {
                            console.log(JSON.stringify(err.data));
                            console.log(JSON.stringify(new_address));
                            getUserShippingAddress();
                            getUserBillingAddress();
                        });
                }

            });
        };

        $scope.deactivateAddress = function (address) {
            userwsapi.deleteAddress(auth.uid, auth.uname, auth.token, address.aid)
                .then(
                    function () {
                        getUserShippingAddress();
                        getUserBillingAddress();
                    },
                    function (err) {
                        console.log(JSON.stringify(err));
                        getUserShippingAddress();
                        getUserBillingAddress();
                    }
                );
        };

        // Get User Data on startup
        getUserBillingAddress();
        getUserShippingAddress();


    }]);