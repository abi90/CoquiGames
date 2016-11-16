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






    }]);
