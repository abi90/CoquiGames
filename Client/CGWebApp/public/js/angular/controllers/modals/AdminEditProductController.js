/**
 * Created by jesmarie on 12-04-16.
 */
/**
 * Created by abi on 12/1/16.
 */
app.controller('AdmingEditProductController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'product', 'adminwsapi',
    function ($scope, authenticationSvc, $rootScope, Popeye, product, adminwsapi){

        $scope.auth = authenticationSvc.getUserInfo();

        adminwsapi.getESRBRating($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.ratings = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.ratings = [];
            }
        );

        adminwsapi.getCategories($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.categories = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.categories = [];
            }
        );

        adminwsapi.getPlatforms($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.platforms = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.platforms = [];
            }
        );

        adminwsapi.getGenres($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.genres = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.genres = [];
            }
        );


        var tempProduct = {
            "availability": product.availability,
            "aditionalinfo": product.aditionalinfo,
            "category": product.category,
            "description": product.description,
            "esrb": product.esrb,
            "genre": product.genre,
            "inoffer": product.inoffer,
            "offerprice": product.offerprice,
            "photolink": product.photolink,
            "pid": product.pid,
            "platformid": product.platformid,
            "price": product.price,
            "rating": product.rating,
            "release": product.release,
            "title": product.title,
            "productqty": product.productqty,
            "offer_start_date": product.offer_start_date,
            "offer_end_date": product.offer_end_date,
            "active": product.active,
            "offerid": product.offerid
        };


        $scope.selectedProduct = tempProduct;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.submit = function() {
            return Popeye.closeCurrentModal($scope.selectedProduct);
        };

        $scope.cancel = function () {
            return Popeye.closeCurrentModal(null);
        };



    }]);