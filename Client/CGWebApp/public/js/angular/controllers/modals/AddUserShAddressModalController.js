/**
 * Created by abi on 12/9/16.
 */
app.controller('AddUserShAddressModalController',
    [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', '$location',
        function ($scope, authenticationSvc, $rootScope, Popeye, $location){

            $scope.selectedAddress = {
                "aaddress1": '',
                "aaddress2": '',
                "acity": '',
                "acountry": 'USA',
                "afullname": '',
                "acurrent": '',
                "aid": '',
                "astate": '',
                "atype": 'shipping',
                "azip": '',
                "apreferred": false
            };

            $scope.patterns = {
                bigText: '[a-zA-Z\\d\\.\\:\\,\\;\\s\\-]+',
                cvc: '\\d{3}',
                postal: '\\d{5,6}'
            };

            $scope.close = function() {
                return Popeye.closeCurrentModal($scope.selectedAddress);
            };

            $scope.cancel = function () {
                return Popeye.closeCurrentModal(null);
            };

            var getUser = function(){
                var userInfo = authenticationSvc.getUserInfo();
                if(!userInfo){
                    $rootScope.$emit('unLogin');
                    $location.path('/login.html');
                    return Popeye.closeCurrentModal(null);
                }
            };

            getUser();

        }]);