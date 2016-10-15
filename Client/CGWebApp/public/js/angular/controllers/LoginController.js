/**
 * Created by abi on 10/12/16.
 */
app.controller("LoginController", ["$scope", '$rootScope',"$location", "$window", "authenticationSvc",function ($scope, $rootScope,$location, $window, authenticationSvc) {
    $scope.userInfo = null;
    //$rootScope.$emit('unLogin');
    $scope.login = function () {
        authenticationSvc.login($scope.userName, $scope.password)
            .then(function (result) {
                $scope.userInfo = result;
                $rootScope.$emit('Login');
                $location.path("/");
            }, function (error) {
                $window.alert("Invalid credentials");
                $rootScope.$emit('unLogin');
                console.log(error);
            });
    };

    $scope.cancel = function () {
        $scope.userName = "";
        $scope.password = "";
    };
}]);