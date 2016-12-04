/**
 * Created by jesmarie on 12-04-16.
 */
/**
 * Created by abi on 12/1/16.
 */
app.controller('AdmingEditProductController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'product',
    function ($scope, authenticationSvc, $rootScope, Popeye, product){

        adminwsapi.getESRBRating(auth.uname, auth.token).then(
            function (response) {
                $scope.ratings = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.ratings = [];
            }
        );

        var tempProduct = {
            "aditionalinfo": product.product_additonal_info,
            "availability": product.availability,
            "category": product.category,
            "description": product.product_description,
            "esrb": product.genre,
            "genre": product.genre,
            "inoffer": product.inoffer,
            "offerprice": product.offeprice,
            "photolink": product.photolink,
            "pid": product.pid,
            "platformid": product.palformid,
            "price": product.product_price,
            "rating": product.rating,
            "release": product.release_date,
            "title": product.product_title
        };


        $scope.selectedProduct = tempProduct;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.close = function() {
            $scope.selectedProduct = tempProduct;
            return Popeye.closeCurrentModal($scope.selectedProduct);
        };

        $scope.cancel = function () {
            $scope.selectedProduct= product;
            return Popeye.closeCurrentModal(product);
        };

    }]);