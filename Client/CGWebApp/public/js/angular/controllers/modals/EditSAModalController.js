/**
 * Created by abi on 12/1/16.
 */
app.controller('EditSAMoController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'shipping_address',
    function ($scope, authenticationSvc, $rootScope, Popeye, shipping_address){

        var tempAddress = {
            "aaddress1": shipping_address.aaddress1,
            "aaddress2": shipping_address.aaddress2,
            "acity": shipping_address.acity,
            "acountry": shipping_address.acountry,
            "afullname": shipping_address.afullname,
            "acurrent": shipping_address.acurrent,
            "aid": shipping_address.aid,
            "astate": shipping_address.astate,
            "atype": shipping_address.atype,
            "azip": shipping_address.azip,
            "apreferred": shipping_address.apreferred
        };

        $scope.selectedShippingAddress = tempAddress;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.close = function() {
            $scope.selectedShippingAddress = tempAddress;
            return Popeye.closeCurrentModal($scope.selectedShippingAddress);
        };

        $scope.cancel = function () {
            $scope.selectedShippingAddress = shipping_address;
            return Popeye.closeCurrentModal(shipping_address);
        };



}]);