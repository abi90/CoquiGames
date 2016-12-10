/**
 * Created by abi on 12/7/16.
 */
app.controller('EditUserAccountInfoController',
    ['$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'account', '$location', '$filter',
        function ($scope, authenticationSvc, $rootScope, Popeye, account, $location, $filter){

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

            $scope.new_info = tempAccount;

            $scope.userDOB = new Date(account.udob);

            $scope.submit = function() {
                $scope.new_info.udob = $filter('date')(new Date($scope.userDOB),'yyyy-MM-dd');
                var result = {};
                for(x in $scope.new_info){
                    if(account[x] !== $scope.new_info[x]){
                        result[x] = $scope.new_info[x];
                    }
                }
                return Popeye.closeCurrentModal(result);
            };

            $scope.cancel = function () {
                $scope.new_info = account;
                return Popeye.closeCurrentModal(null);
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