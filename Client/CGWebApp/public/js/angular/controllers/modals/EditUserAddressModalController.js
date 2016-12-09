/**
 * Created by abi on 12/1/16.
 */
app.controller('EditUserAddressModalController',
    [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'address', '$location',
    function ($scope, authenticationSvc, $rootScope, Popeye, address, $location){

        var tempAddress = {
            "aaddress1": address.aaddress1,
            "aaddress2": address.aaddress2,
            "acity": address.acity,
            "acountry": address.acountry,
            "afullname": address.afullname,
            "acurrent": address.acurrent,
            "aid": address.aid,
            "astate": address.astate,
            "atype": address.atype,
            "azip": address.azip,
            "apreferred": address.apreferred
        };

        $scope.selectedAddress = tempAddress;


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