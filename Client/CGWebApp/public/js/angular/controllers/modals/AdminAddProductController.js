/**
 * Created by jesmarie on 12-05-16.
 */
/**
 * Created by jesmarie on 12-04-16.
 */
/**
 * Created by abi on 12/1/16.
 */
app.controller('AdminAddProductController', [ '$scope', 'authenticationSvc',  '$rootScope', 'Popeye', 'adminwsapi',
    function ($scope, authenticationSvc, $rootScope, Popeye, adminwsapi){

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
            "availability": false,
            "aditionalinfo": null,
            "category": null,
            "description": null,
            "esrb": null,
            "genre": null,
            "inoffer": false,
            "offerprice": null,
            "photolink": null,
            "pid": null,
            "platformid": null,
            "price": null,
            "rating": null,
            "release": null,
            "title": null,
            "productqty": 0,
            "offer_start_date": null,
            "offer_end_date": null,
            "active": false
        };


        $scope.selectedProduct = tempProduct;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.submit = function() {
            $scope.selectedProduct = tempProduct;
            return Popeye.closeCurrentModal($scope.selectedProduct);
        };

        $scope.cancel = function () {
            $scope.selectedProduct= tempProduct;
            return Popeye.closeCurrentModal(null);
        };

    }]);