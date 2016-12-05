/**
 * Created by abi on 12/5/16.
 */

app.controller('UserInfoController', ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope', 'Popeye',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope, Popeye){

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

        var getUser = function () {
            userwsapi.getUser(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userData = response.data;
                },
                function () {
                    logout();
                }
            );
        };

        // Modals functions:
        $scope.shoChangePassModal = function() {

            // Open a modal to change user password
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/change-password.html",
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

        $scope.shoEditPersonalInfoModal = function() {

            // Open a modal to edit user info
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/edit-personal-info.html",
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
        getUser();

    }]);