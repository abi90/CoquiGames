/**
 * Created by abi on 12/1/16.
 */
app.controller('EditSAModalController',
    [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'shipping_address', '$location',
    function ($scope, authenticationSvc, $rootScope, Popeye, shipping_address, $location){

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

        $scope.new_password = tempAddress;


        $scope.close = function() {
            $scope.new_password = tempAddress;
            return Popeye.closeCurrentModal($scope.new_password);
        };

        $scope.cancel = function () {
            $scope.new_password = shipping_address;
            return Popeye.closeCurrentModal(shipping_address);
        };

        $scope.userInfo = authenticationSvc.getUserInfo();

        var getUser = function(){
            if(!$scope.userInfo){
                $rootScope.$emit('unLogin');
                $location.path('/login.html');
                return Popeye.closeCurrentModal(shipping_address);
            }
        };

        getUser();

}]);