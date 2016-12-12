/**
 * Created by abi on 12/5/16.
 */
/**
 * Created by abi on 10/12/16.
 */
app.controller('UserCheckoutController', ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope', 'Popeye',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope, Popeye){

        $scope.selection = {fee: null};

        // Local Functions
        var logout = function () {

            authenticationSvc.logout()
                .then(function () {
                    $rootScope.$emit('unLogin');
                    $location.path("/login.html");
                }, function () {
                    $rootScope.$emit('unLogin');
                    $location.path("/login.html");
                });
        };

        var getUserCart= function () {
            userwsapi.getUserCart(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userCart = response.data;
                    $rootScope.$emit('uCart');
                },
                function () {
                    logout();
                }
            )
        };

        var getUserPreferences= function () {
            userwsapi.getUserPreferences(auth.uid, auth.uname, auth.token).then(
                function (response) {
                    $scope.userPreferences = response.data;
                    $scope.selectedPayment = $scope.userPreferences.payment_method;
                    $scope.selectedShAddress = $scope.userPreferences.shipping_address;
                },
                function () {
                    logout();
                }
            )
        };

        var getShipmentFees= function () {
            userwsapi.getShipmentFees().then(
                function (response) {
                    $scope.shipmentFees = response.data;
                },
                function () {
                    logout();
                }
            )
        };

        var getUserPayments = function () {
          userwsapi.getUserPayment(auth.uid, auth.uname, auth.token)
              .then(
                function (response) {
                    $scope.userPayments = response.data;
                },
                  function () {
                      logout();
                  }
              );
        };

        // Scope Functions (Can be called from de html)
        $scope.getSubTotal = function(){
            var subtotal = 0;
            try {
                for (var i = 0; i < $scope.userCart.length; i++) {
                    var product = $scope.userCart[i];
                    if (product.inoffer) {
                        subtotal += (product.offerprice * product.pquantity);
                    }
                    else{
                        subtotal += (product.pprice * product.pquantity);
                    }
                }
            }catch (err){
                subtotal = 0;
            }
            return subtotal;
        };

        $scope.placeOrder = function () {

            var order = {
                "shipment_feeid": $scope.selection.fee.shipment_feeid,
                "aid": $scope.selectedShAddress.aid,
                "cid": $scope.selectedPayment.cid
            };

            userwsapi.postUserOrder(auth.uid, auth.uname, auth.token, order).then(
                function () {
                    $location.path('/account-orders')
                },
                function () {
                    logout();
                }
            );
        };

        $scope.changePayment= function(payment){
            $scope.selectedPayment = payment;
        };

        // Modals functions:
        $scope.shoPreferredShpAddModal = function() {

            // Open a modal to show the user address
            var modal = Popeye.openModal({
                controller: 'CheckoutShipAddController',
                templateUrl: "js/angular/modals/change_shipping_address_modal.html"
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(response) {
                if(response){
                    $scope.selectedShAddress = response;
                }
            });
        };


        // Get User Data on startup
        getUserPreferences();
        getShipmentFees();
        getUserCart();
        getUserPayments();

    }]);