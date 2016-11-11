/**
 * Created by jesmarie on 10-12-16.
 */
app.controller('OrderController', ['$scope', '$location', 'userwsapi','orderId', 'authenticationSvc',function($scope, $location, userwsapi, orderId, authenticationSvc)
{
    $scope.orderId = orderId;
    $scope.auth;
    $scope.userOrder;

    var getOrderDetail = function() {
        $scope.auth = authenticationSvc.getUserInfo();
        if($scope.auth) {
            userwsapi.getUserOrders($scope.auth.uid, $scope.auth.uname, $scope.auth.upassword).then(
                function (response) {
                    for(var i in response.data)
                    {
                        if(orderId == response.data[i].oid)
                        {
                            $scope.userOrder = response.data[i];
                        }
                    }
                },
                function (error) {
                    console.log("Error: " + error.statusCode);
                    $location.path("/404.html");
                }
            )
        }
        else {
            $location.path("/");
        }
    };

    getOrderDetail();

}]);