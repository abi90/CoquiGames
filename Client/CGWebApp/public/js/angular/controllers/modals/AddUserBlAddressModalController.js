/**
 * Created by abi on 12/9/16. AddUserBlAddressModalController
 */
app.controller('AddUserBlAddressModalController',
    [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', '$location', 'userwsapi',
        function ($scope, authenticationSvc, $rootScope, Popeye, $location, userwsapi){

            $scope.selectedAddress = {
                "aaddress1": '',
                "aaddress2": '',
                "acity": '',
                "acountry": 'USA',
                "afullname": '',
                "acurrent": '',
                "aid": '',
                "astate": '',
                "atype": 'billing',
                "azip": '',
                "apreferred": false,
                "pid": 0,
                "cnumber": ''
            };

            $scope.validPayment = false;

            $scope.userPayments = [];

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

            $scope.setPayment = function (payment) {
                $scope.selectedAddress.pid = payment.cid;
                $scope.selectedAddress.cnumber = payment.cnumber;
                $scope.validPayment = true;
            };

            $scope.cardSelected=function () {
              return ($scope.selectedAddress.pid  > 0 && $scope.selectedAddress.cnumber);
            };

            var getUser = function(){
                var userInfo = authenticationSvc.getUserInfo();
                if(!userInfo){
                    $rootScope.$emit('unLogin');
                    $location.path('/login.html');
                    return Popeye.closeCurrentModal(null);
                }
                userwsapi.getUserPayment(userInfo.uid, userInfo.uname, userInfo.token)
                    .then(
                        function (response) {
                            $scope.userPayments = response.data;
                        },
                        function () {
                            $rootScope.$emit('unLogin');
                            $location.path('/login.html');
                            return Popeye.closeCurrentModal(null);
                        }
                    );
            };

            getUser();

        }]);