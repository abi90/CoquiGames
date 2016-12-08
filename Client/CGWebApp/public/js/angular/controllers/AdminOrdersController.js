/**
 * Created by Abisai on 11/29/16.
 */
app.controller('AdminOrdersController', ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchOrders = '';

        // Get list of orders from the WS API
        adminwsapi.getOrders(auth.uname, auth.token).then(
            function (response) {
                $scope.orders = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.orders = [];
            }
        );

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
            modal.closed.then(function() {

            });
        };

    }]);
