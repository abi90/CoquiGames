/**
 * Created by jesmarie on 12-05-16.
 */
/**
 * Created by jesmarie on 12-04-16.
 */
/**
 * Created by abi on 12/1/16.
 */
app.controller('AdmingEditOrderController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'order', 'adminwsapi',
    function ($scope, authenticationSvc, $rootScope, Popeye, order, adminwsapi){

        $scope.auth = authenticationSvc.getUserInfo();

        adminwsapi.getOrderStatus($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.status = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.status = [];
            }
        );

        var tempOrder = {
            "order_status_name": order.order_status_name
        };


        $scope.selectedOrder = tempProduct;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.close = function() {
            $scope.selectedOrder = tempOrder;
            return Popeye.closeCurrentModal($scope.selectedOrder);
        };

        $scope.cancel = function () {
            $scope.selectedOrder= order;
            return Popeye.closeCurrentModal(order);
        };

    }]);