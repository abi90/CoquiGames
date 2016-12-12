/**
 * Created by jesmarie on 10-12-16.
 */
app.controller('ProductController',
    ['$scope', '$location', 'storewsapi','productId', '$rootScope', 'addToWishList', 'addToUserCart',
    function($scope, $location, storewsapi, productId, $rootScope, addToWishList, addToUserCart) {

        $scope.productId = productId;
        $scope.qty = 1;
        $scope.Loading = false;
        $scope.prange = [];

        var getProduct = function () {
            $scope.Loading = true;
            storewsapi.getProduct($scope.productId).then(
                function (response) {
                    $scope.product = response.data;
                },
                function (error) {
                    console.log(error.toString());
                    $location.path("/404.html");
                });

            storewsapi.relatedProducts($scope.productId).then(
                function (response) {
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
                function ()
                {
                    $scope.altImgs = [];
                });

            var i;
            for(i=0; i<30; i++){
                $scope.prange[i] = i+1;
            }
            $scope.Loading = false;
        };


        $scope.addProductToCart = function () {
            addToUserCart.addProductWithQty(productId, $scope.qty);
        };

        $scope.addRelatedProductToCart = function (pid) {
            addToUserCart.addProductWithQty(pid, 1);
        };

        $scope.addProductToWishList = function () {
            addToWishList.addProductToWishList($scope.productId);
        };

        $scope.addRelatedProductToWishList = function (pid) {
            addToWishList.addProductToWishList(pid);
        };

        getProduct();

    }]);