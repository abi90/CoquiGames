/**
 * Created by abi on 11/16/16.
 */
app.controller('AdminProductsController', ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchProduct = '';

        $scope.esrbRating = {esrb_rate: "Everyone", esrbid: 1};
        $scope.esrb_ratings = [{esrb_rate: "Everyone", esrbid: 1}, {esrb_rate: "Teen", esrbid: 2}];

        // Get list of products from the WS API
        var getProducts = function() {
            adminwsapi.getAllProducts(auth.uname, auth.token).then(
                function (response) {
                    $scope.products = response.data
                },
                function (err) {
                    console.log(err.toString());
                    $scope.products = [];
                }
            );
        };

        $scope.shoEditNewProductModal = function(product) {
            // Open a modal for admin to edit a new product
            var modal = Popeye.openModal({
                controller: 'AdmingEditProductController',
                templateUrl: "js/angular/modals/edit-admin-product.html",
                resolve: {
                    product: function () {
                        return product;
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

        $scope.shoAddNewProductModal = function() {
            // Open a modal for admin to add a new product
            var modal = Popeye.openModal({
                controller: 'AdminAddProductController',
                templateUrl: "js/angular/modals/add-admin-product.html",
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(product) {

                adminwsapi.postAdminProduct(auth.uname, auth.token, product).then(
                    function (response) {
                        getProducts()
                    },
                    function (err) {
                        getProducts()
                    }
                );


            });
        };

        getProducts();




    }]);
