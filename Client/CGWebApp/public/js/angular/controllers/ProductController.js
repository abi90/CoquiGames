/**
 * Created by jesmarie on 10-12-16.
 */
app.controller('ProductController', ['$scope', '$location', 'storewsapi','productId',function($scope, $location, storewsapi, productId)
{
    $scope.productId = productId;
    storewsapi.getProduct($scope.productId).then(
        function(response) {
            $scope.product = response.data;
        },
        function (error) {
            console.log(JSON.stringify(error));
            $location.path("/404.html");
        });
}]);