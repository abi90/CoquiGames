/**
 * Created by abi on 11/16/16.
 */
app.controller('AdminProductsController', ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchProduct = '';
        //$scope.getAllProducts = getAllProducts();

        // Get list of products from the WS API
        adminwsapi.getAllProducts(auth.uname, auth.token).then(
            function (response) {
                $scope.products = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.products = [];
            }
        );

        $scope.shoAddNewProductModal = function() {
            // Open a modal for admin to add a new product
            var modal = Popeye.openModal({
                controller: 'AdminProductsController',
                templateUrl: "js/angular/modals/add-admin-product.html",
                resolve: {
                    auth: function ($q, authenticationSvc) {
                        var userInfo = authenticationSvc.getUserInfo();
                        if (userInfo) {
                            return $q.when(userInfo);
                        } else {
                            return $q.reject({authenticated: false});
                        }
                    }
                }
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function() {

            });
        };

        $scope.shoEditNewProductModal = function() {
            // Open a modal for admin to add a new product
            var modal = Popeye.openModal({
                controller: 'AdminProductsController',
                templateUrl: "js/angular/modals/edit-admin-product.html",
                resolve: {
                    auth: function ($q, authenticationSvc) {
                        var userInfo = authenticationSvc.getUserInfo();
                        if (userInfo) {
                            return $q.when(userInfo);
                        } else {
                            return $q.reject({authenticated: false});
                        }
                    }
                }
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function() {

            });
        };



    }]);
