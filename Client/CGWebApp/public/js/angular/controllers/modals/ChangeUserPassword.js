/**
 * Created by abi on 12/7/16.
 */
app.controller('ChangeUserPassword',
    ['$scope', 'authenticationSvc', '$rootScope', 'Popeye', '$location',
        function ($scope, authenticationSvc, $rootScope, Popeye, $location){

            $scope.new_password = {password1: '', password2: ''};

            $scope.regex = {pattern: '[a-zA-Z\\d]+'};

            $scope.validPassword = function () {
                return angular.equals($scope.new_password.password1, $scope.new_password.password2);
            };

            $scope.submit = function()
            {
                return Popeye.closeCurrentModal($scope.new_password);
            };

            $scope.cancel = function () {
                return Popeye.closeCurrentModal(null);
            };

            var getUser = function(){
                $scope.userInfo = authenticationSvc.getUserInfo();
                if(!$scope.userInfo){
                    $rootScope.$emit('unLogin');
                    $location.path('/login.html');
                    return Popeye.closeCurrentModal(null);
                }
            };

            getUser();

        }]);