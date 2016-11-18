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
            console.log(error.toString());
            $location.path("/404.html");
        });
    storewsapi.relatedProducts($scope.productId ).then(
        function(response) {
            $scope.relatedPrds = response.data;
        },
        function (error) {
            console.log(error.toString());
            $scope.relatedPrds = [];
        }
    );
    storewsapi.getProductAltImg($scope.productId).then(
        function (response){
            $scope.altImgs = response.data;
        },
        function (err)
        {
            console.log(err.data.toString());
            $scope.altImgs = [];
        });
}]);