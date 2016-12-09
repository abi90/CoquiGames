/**
 * Created by jesmarie on 12-05-16.
 */
/**
 * Created by jesmarie on 12-04-16.
 */
/**
 * Created by abi on 12/1/16.
 */
app.controller('AdminEditOrderController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'order', 'adminwsapi', '$location',
    function ($scope, authenticationSvc, $rootScope, Popeye, order, adminwsapi, $location){
        var auth = authenticationSvc.getUserInfo();
        adminwsapi.getOrderStatus(auth.uname, auth.token).then(
            function (response) {
                $scope.status = response.data;
            },
            function () {
                $scope.status = [];
                $rootScope.$emit('unLogin');
                $location.path('/login.html');
                $scope.cancel();
            }
        );
        console.log(JSON.stringify(order));

        var tempOrder = order.order_statusid;
        $scope.selectedOrder = tempOrder;

        $scope.submit = function(){
            return Popeye.closeCurrentModal({orderid: order.orderid, status: $scope.selectedOrder});
        };

        $scope.cancel = function () {
            return Popeye.closeCurrentModal(null);
        };

    }]);