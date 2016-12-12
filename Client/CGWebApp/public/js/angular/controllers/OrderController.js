/**
 * Created by jesmarie on 10-12-16.
 */
app.controller('OrderController', ['$scope', '$location', 'userwsapi','orderId', 'authenticationSvc',function($scope, $location, userwsapi, orderId, authenticationSvc)
{
    $scope.orderId = orderId;
    $scope.userOrder = {};
    $scope.Loading = false;

    var getOrderDetail = function() {
        $scope.Loading = true;
        var auth = authenticationSvc.getUserInfo();
        if(auth) {
            userwsapi.getUserOrders(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    for(var i in response.data)
                    {
                        if(orderId == response.data[i].oid)
                        {
                            $scope.userOrder = response.data[i];
                        }
                    }
                    if(!orderId){
                        $location.path("/login.html");
                    }
                },
                function () {
                    $location.path("/login.html");
                }
            );
        }
        else {
            $location.path("/login.html");
        }
        $scope.Loading = false;
    };

    getOrderDetail();

}]);