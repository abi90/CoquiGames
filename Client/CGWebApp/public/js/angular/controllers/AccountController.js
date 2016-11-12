/**
 * Created by abi on 10/12/16.
 */
app.controller('AccountController', ['$scope', '$location', 'authenticationSvc', 'auth', 'userwsapi', '$rootScope', 'Popeye',
    function ($scope, $location, authenticationSvc, auth, userwsapi, $rootScope, Popeye){

        // Scope Variables
        $scope.userData;
        $scope.userAddress;
        $scope.userOrder;
        $scope.userPayment;
        $scope.userWishlist;
        $rootScope.userCart;
        $scope.shippmentFees;
        $scope.shipmentFee;
        $scope.shipmentFeeId = 0;
        $scope.selectedPayment = {};
        $scope.userPreferences;

        // Local Functions
        var getUserAddress = function (auth) {
            userwsapi.getUserAddress(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userAddress = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUser = function (auth) {
            userwsapi.getUser(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userData = response.data;
                },
                function (error) {
                    console.log("Error: " + error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserOrder = function (auth) {
            userwsapi.getUserOrders(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userOrder = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserPayments = function (auth) {
            userwsapi.getUserPayment(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userPayment = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserCart= function (auth) {
            userwsapi.getUserCart(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userCart = response.data;
                    $rootScope.$emit('Login');
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getUserPreferences= function (auth) {
            userwsapi.getUserPreferences(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userPreferences = response.data;
                    $scope.selectedPayment = $scope.userPreferences.payment_method;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    //$location.path("/404.html");
                }
            )
        };

        var getUserWishList= function (auth) {
            userwsapi.getUserWishlist(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userWishlist = response.data;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $location.path("/404.html");
                }
            )
        };

        var getShipmentFees= function () {
               userwsapi.getShipmentFees().then(
                   function (response) {
                       $scope.shippmentFees = response.data;
                       $scope.shipmentFee = $scope.shippmentFees[0];
                   },
                   function (error) {
                       console.log("Error: " +error.statusCode);
                       $location.path("/404.html");
                   }
               )
        };

        var getUserBillingAddress= function (auth) {
            userwsapi.getUserBillingAddress(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userBillingAddress = response.data;
                },
                function (error) {
                    console.log(error);
                    console.log("Error: " + response.data);
                    $scope.userBillingAddress = [];
                }
            )

        };

        var getUserShippingAddress= function (auth) {
            userwsapi.getUserShippingAddress(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.userShippingAddress = response.data;
                },
                function (error) {
                    console.log("Error: " + error.statusCode);
                    $scope.userShippingAddress = [];
                }
            )

        };

        // Scope Functions (Can be called from de html)
        $scope.logout = function () {

            authenticationSvc.logout()
                .then(function (result) {
                    $scope.userInfo = null;
                    $location.path("/login");
                }, function (error) {
                    console.log(error);
                });
        };

        $scope.getSubTotal = function(){
            var subtotal = 0;
            try {
                for (var i = 0; i < $scope.userCart.length; i++) {
                    var product = $scope.userCart[i];
                    subtotal += (product.pprice * product.pquantity);
                }
            }catch (err){
                subtotal = 0;
            }
            return subtotal;
        };

        $scope.init = function (auth) {
            $scope.userInfo = auth;
        };

        $scope.getShipmentFee = function () {
            try {
                for (var i = 0; i < $scope.shippmentFees.length; i++) {
                    if ($scope.shipmentFeeId == $scope.shippmentFees[i].shipment_feeid) {
                        $scope.shipmentFee = $scope.shippmentFees[i];
                        return $scope.shipmentFee;
                    }
                }
                return $scope.shipmentFee;
            }catch (err){
                console.log("Error while updating shipment fee.");
                return $scope.shipmentFee;
            }
        };

        $scope.shoPreferredShpAddModal = function() {

            // Open a modal to show the user address
            var modal = Popeye.openModal({
                controller: 'AccountController',
                templateUrl: "js/angular/modals/change_shipping_address_modal.html",
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


        // Get User Data on startup
        getUser(auth);
        getUserAddress(auth);
        getUserOrder(auth);
        getUserPayments(auth);
        getUserCart(auth);
        getUserWishList(auth);
        getShipmentFees();
        getUserPreferences(auth);
        getUserShippingAddress(auth);
        getUserBillingAddress(auth);

    }]);