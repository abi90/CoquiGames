/**
 * Created by abi on 12/7/16.
 */
app.controller('EditUserAccountInfoController',
    ['$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'account', '$location',
        function ($scope, authenticationSvc, $rootScope, Popeye, account, $location){

            var tempAccount = {
                ufirstname: account.ufirstname,
                ulastname: account.ulastname,
                uemail: account.uemail,
                uphone: account.uphone,
                udob: account.udob,
                uname: account.uname
            };

            $scope.patterns = {
                bigText: '[a-zA-Z\\d\\.\\:\\,\\;\\s\\-]+',
                email: /(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/g,
                phone: /^(\d{3})([-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})$/g,
                userName: '[a-zA-Z]+[\\da-zA-Z]+'
            };

            $scope.new_password = tempAccount;

            $scope.userDOB = new Date(account.udob);

            $scope.close = function() {
                $scope.new_password.udob = $filter('date')(new Date($scope.userDOB),'yyyy-MM-dd');;
                return Popeye.closeCurrentModal($scope.new_password);
            };

            $scope.cancel = function () {
                $scope.new_password = account;
                return Popeye.closeCurrentModal(account);
            };

            var getUser = function(){
                $scope.userInfo = authenticationSvc.getUserInfo();
                if(!$scope.userInfo){
                    $rootScope.$emit('unLogin');
                    $location.path('/login.html');
                    return Popeye.closeCurrentModal(account);
                }
            };

            getUser();

        }]);