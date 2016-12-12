/**
 * Created by Abisai on 11/29/16.
 */
app.controller('AdminOrdersController',
    ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye', 'authenticationSvc',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye, authenticationSvc){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchOrders = '';
        $scope.Loading = false;

        // Get list of orders from the WS API
        var getAnyOrders = function() {
            $scope.Loading = true;
            adminwsapi.getOrders(auth.uname, auth.token).then(
                function (response) {
                    $scope.orders = response.data
                },
                function () {
                    $scope.orders = [];
                    authenticationSvc.logout();
                    $rootScope.$broadcast('unLogin');
                    $location.path('/login.html');
                }
            );
            $scope.Loading = false;
        };

        $scope.shoEditOrderModal = function(order) {
            // Open a modal for admin to edit an order
            var modal = Popeye.openModal({
                controller: 'AdminEditOrderController',
                templateUrl: "js/angular/modals/edit-admin-order.html",
                resolve: {
                    order: function () {
                        return order;
                    }
                }
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(order_response) {
                if(order_response){
                    adminwsapi.updateOrder(auth.uname, auth.token, order_response.status, order_response.orderid).then(
                        function (response) {
                            getAnyOrders()
                        },
                        function () {
                            getAnyOrders()
                        }
                    );
                }

            });
        };

        getAnyOrders();
    }]);
