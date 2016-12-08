/**
 * Created by abi on 12/5/16.
 */

app.controller('UserInfoController', ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope', 'Popeye',
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
                controller: 'ChangeUserPassword',
                templateUrl: "js/angular/modals/change-password.html",
                resolve: {
                    user: function ($q, authenticationSvc) {
                        var userInfo = authenticationSvc.getUserInfo();
                        if (userInfo) {
                            return $q.when($scope.userData);
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
            modal.closed.then(function(passwords) {
                if(passwords){
                    $scope.messages[$scope.messages.length]= "Your Password was updated!";
                    getUser();
                }
            });
        };

        $scope.shoEditPersonalInfoModal = function() {

            // Open a modal to edit user info
            var modal = Popeye.openModal({
                controller: 'EditUserAccountInfoController',
                templateUrl: "js/angular/modals/edit-personal-info.html",
                resolve: {
                    account: function ($q, authenticationSvc) {
                        var userInfo = authenticationSvc.getUserInfo();
                        if (userInfo) {
                            console.log(JSON.stringify($scope.userData));
                            return $q.when($scope.userData);
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
            modal.closed.then(function(value){
                if(value){
                    userwsapi.putUser(auth.uid, auth.uname, auth.token, value)
                        .then(
                            function (response){
                                $scope.messages[$scope.messages.length]= "Your Information was updated!";
                                getUser();

                            },
                            function (err) {
                                $scope.errors[$scope.errors.length]= err.data;
                                    getUser();
                            });
                }
            });
        };

        $scope.closeErrorAlert= function(index){
            $scope.errors.splice(index,1);
        };

        $scope.closeMessageAlert= function(index){
            $scope.messages.splice(index,1);
        };

        // Get User Data on startup
        getUser();

    }]);