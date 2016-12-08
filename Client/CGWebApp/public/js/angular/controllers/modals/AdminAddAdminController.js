/**
 * Created by jesmarie on 12-07-16.
 */
app.controller('AdminAddAdminController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye',
    function ($scope, authenticationSvc, $rootScope, Popeye){
        $scope.regexs = {
            email: /(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/g,
            phone: /^(\d{3})([-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})$/g,
            userName: '[a-zA-Z]+[\\da-zA-Z]+',
            password: '[a-zA-Z\\d]+',
            bigText: '[a-zA-Z\\d\\.\\:\\,\\;\\s\\-]+'
        };

        $scope.selectedAdmin = {};
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.validAdminPassword = function (){
            return angular.equals($scope.selectedAdmin.upassword, $scope.selectedAdmin.upassword2);
        };

        $scope.submit = function() {
            return Popeye.closeCurrentModal($scope.selectedAdmin);
        };

        $scope.cancel = function () {
            return Popeye.closeCurrentModal(null);
        };

    }]);