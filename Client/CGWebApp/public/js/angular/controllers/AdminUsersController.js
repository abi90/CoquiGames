/**
 * Created by abi on 11/16/16.
 */
app.controller('AdminUsersController', ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye','$filter',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye, $filter){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchUser = '';

        // Get list of users from the WS API
        var getUsers = function() {
            adminwsapi.getUsers(auth.uname, auth.token).then(
                function (response) {
                    $scope.users = response.data
                },
                function (err) {
                    $rootScope.$emit("unLogin");
                    $location.path("/login.html");
                    $scope.users = [];
                }
            );
        };

        //Edit User Info
        $scope.shoEditUserInfoModal = function(user) {

            // Open a modal for admin to edit user info
            var modal = Popeye.openModal({
                controller: 'ChangeUserPassword',
                templateUrl: "js/angular/modals/change-password.html",
                resolve: {
                    user: function ($q, authenticationSvc) {
                        var userInfo = authenticationSvc.getUserInfo();
                        if (userInfo) {
                            return $q.when(user);
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
            modal.closed.then(function(value) {
                if(value){

                    adminwsapi.changeUserPassword(auth.uname, auth.token, value.accountid, {upassword: value.password}).then(
                        function (response) {
                            $scope.messages = ["Password change for " + value.accountid + " was succesful"];
                            getUsers()
                        },
                        function (err) {
                            console.log(JSON.stringify(err.data));
                            getUsers()
                        }
                    );
                }
            });
        };

        $scope.closeAlert = function(index){
            $scope.messages.splice(index, 1);
        };

        //Deactivate User Account
        $scope.shoDeactivateUser = function(user) {

            // Deactivate user account
            adminwsapi.deactivateUser(auth.uname, auth.token, user.accountid).then(
                function (response) {
                    getUsers()
                },
                function (err) {
                    console.log(JSON.stringify(err));
                    getUsers()
                }
            );
        };


        //Add New Admin User
        $scope.shoAddAdminModal = function() {

            // Open a modal for admin to edit user info
            var modal = Popeye.openModal({
                controller: 'AdminAddAdminController',
                templateUrl: "js/angular/modals/add-admin-user.html",
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(user) {
                user.udob = $filter('date')(new Date(user.udob),'yyyy-MM-dd');

                adminwsapi.postAdminUser(auth.uname, auth.token, user).then(
                    function (response) {
                        getUsers()
                    },
                    function (err) {
                        console.log(JSON.stringify(err));
                        getUsers()
                    }
                );


            });

        };

        getUsers();
    }]);
