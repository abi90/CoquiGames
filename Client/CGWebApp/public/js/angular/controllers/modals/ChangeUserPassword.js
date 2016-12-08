/**
 * Created by abi on 12/7/16.
 */
app.controller('ChangeUserPassword',
    ['$scope', 'authenticationSvc', '$rootScope', 'Popeye', '$location', 'user',
        function ($scope, authenticationSvc, $rootScope, Popeye, $location, user){

            $scope.new_password = {password1: '', password2: ''};

            $scope.regex = {pattern: '[a-zA-Z\\d]+'};

            $scope.validPassword = function () {
                return angular.equals($scope.new_password.password1, $scope.new_password.password2);
            };

            $scope.submit = function()
            {
                user.password = $scope.new_password.password1;
                return Popeye.closeCurrentModal(user);
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