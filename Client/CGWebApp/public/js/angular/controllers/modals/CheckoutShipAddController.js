/**
 * Created by abi on 12/5/16.
 */
app.controller('CheckoutShipAddController',
    [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', '$location', 'userwsapi',
        function ($scope, authenticationSvc, $rootScope, Popeye, $location, userwsapi){

            $scope.userShippingAddress = [];
            $scope.selection = {address: null};

            $scope.submit = function() {
                return Popeye.closeCurrentModal($scope.selection.address);
            };

            $scope.cancel = function () {
                return Popeye.closeCurrentModal(null);
            };

            var getUserAddress = function(){
                var userInfo = authenticationSvc.getUserInfo();
                if(!userInfo){
                    $rootScope.$emit('unLogin');
                    $location.path('/login.html');
                    return Popeye.closeCurrentModal(null);
                }
                userwsapi.getUserAddress(userInfo.uid, userInfo.uname, userInfo.token)
                    .then(
                        function (response) {
                            $scope.userShippingAddress = response.data;
                        },
                        function () {
                            $rootScope.$emit('unLogin');
                            $location.path('/login.html');
                            return Popeye.closeCurrentModal(null);
                        }
                    );
            };

            getUserAddress();

        }]);