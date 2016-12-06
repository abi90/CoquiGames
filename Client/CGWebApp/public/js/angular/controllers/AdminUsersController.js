/**
 * Created by abi on 11/16/16.
 */
app.controller('AdminUsersController', ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchUser = '';

        // Get list of users from the WS API
        adminwsapi.getUsers(auth.uname, auth.token).then(
            function (response) {
                $scope.users = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.users = [];
            }
        );

        $scope.shoEditUserInfoModal = function() {
            //$scope.selectedUser = u;

            // Open a modal for admin to edit user info
            var modal = Popeye.openModal({
                controller: 'AdminUsersController',
                templateUrl: "js/angular/modals/edit-admin-user-info.html",
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

        $scope.shoAddAdminModal = function() {

            // Open a modal for admin to edit user info
            var modal = Popeye.openModal({
                controller: 'AdminUsersController',
                templateUrl: "js/angular/modals/add-admin-user.html",
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





    }]);
