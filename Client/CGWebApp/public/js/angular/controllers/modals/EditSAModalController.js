/**
 * Created by abi on 12/1/16.
 */
app.controller('EditSAModalController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'shipping_address',
    function ($scope, authenticationSvc, $rootScope, Popeye, shipping_address){

        $scope.selectedShippingAddress = shipping_address;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.close = function() {
            return Popeye.closeCurrentModal($scope.selectedShippingAddress);
        };



}]);