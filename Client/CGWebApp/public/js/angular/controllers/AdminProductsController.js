/**
 * Created by abi on 11/16/16.
 */
app.controller('AdminProductsController',
    ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye', 'authenticationSvc',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye, authenticationSvc){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchProduct = '';
        $scope.messages = [];
        $scope.errors = [];
        $scope.Loading = false;
        $scope.esrbRating = {esrb_rate: "Everyone", esrbid: 1};
        $scope.esrb_ratings = [{esrb_rate: "Everyone", esrbid: 1}, {esrb_rate: "Teen", esrbid: 2}];

        // Get list of products from the WS API
        var getProducts = function() {
            $scope.Loading = true;
            adminwsapi.getAllProducts(auth.uname, auth.token).then(
                function (response) {
                    $scope.products = response.data
                },
                function () {
                    authenticationSvc.logout();
                    $rootScope.$broadcast('unLogin');
                    $location.path('/login.html');
                }
            );
            $scope.Loading = false;
        };

        //NOT TESTED FOR ACTUAL EDITING. JUST PULLS INFORMATION
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
            modal.closed.then(function(product) {

                if(product){
                    adminwsapi.updateProduct(auth.uname, auth.token, product).then(
                        function () {
                            $scope.messages[$scope.messages.length]= "Product "+product.pid +" was updated!";
                            getProducts()
                        },
                        function (err) {
                            $scope.errors[$scope.errors.length]= err.data;
                            getProducts()
                        }
                    );
                }

            });
        };


        // Deactivate a product
        $scope.shoDeactivateProduct = function(pid){
            adminwsapi.deactivateProduct(auth.uname, auth.token, pid).then(
                function () {
                    $scope.messages[$scope.messages.length]= "Product "+pid +" was deactivated!";
                    getProducts()
                },
                function (err) {
                    $scope.errors[$scope.errors.length]= err.data;
                    getProducts()
                }
            );

        };

        // Add A New Product
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
                if(product){
                    adminwsapi.postAdminProduct(auth.uname, auth.token, product).then(
                        function (response) {
                            $scope.messages[$scope.messages.length]= "Product "+response.data.pid+" was created!";
                            getProducts()
                        },
                        function (err) {
                            $scope.errors[$scope.errors.length]= err.data;
                            getProducts()
                        }
                    );

                }

            });
        };

        $scope.closeErrorAlert= function(index){
            $scope.errors.splice(index,1);
        };

        $scope.closeMessageAlert= function(index){
            $scope.messages.splice(index,1);
        };

        getProducts();

    }]);
