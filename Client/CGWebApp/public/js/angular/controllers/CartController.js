/**
 * Created by abi on 10/14/16.
 */
/**
 * Created by abi on 10/12/16.
 */
app.controller('CartController', ['$scope', '$location', 'auth', 'authenticationSvc', 'userwsapi', '$rootScope',
    function ($scope, $location,auth,authenticationSvc, userwsapi, $rootScope) {

        $rootScope.userCart;
        $scope.cartTotal;
        console.log("mierda");

        var getUserCart= function () {
            var auth = authenticationSvc.getUserInfo();
            if (auth){
                userwsapi.getUserCart(auth.uid, auth.uname, auth.upassword).then(
                    function (response) {
                        $scope.userCart = response.data;
                    },
                    function (error) {
                        console.log("Error: " + error.statusCode);
                        $location.path("/404.html");
                    }
                )
            }
        };

        $scope.getSubTotal = function(){
            if( $scope.userCart){
                var subtotal = 0;
                for(var i = 0; i < $scope.userCart.length; i++){
                    var product = $scope.userCart[i];
                    subtotal += (product.pprice * product.pquantity);
                }
                $scope.cartTotal = subtotal + subtotal * 0.1105 + $scope.shippmentFee;
                return subtotal;
            }

        };

        $scope.changeProductQty = function(product){
            if(product.pquantity>0 || product.pquantity < 99){
                var auth = authenticationSvc.getUserInfo();
                userwsapi.putUserCart(auth.uid,auth.uname,auth.upassword,product).then(
                    function(response){
                        getUserCart();
                    },
                    function(error){
                        getUserCart()
                    });
            }
            console.log(JSON.stringify(product));

        };

        $scope.removeProduct = function(pid) {
            var auth = authenticationSvc.getUserInfo();
            userwsapi.delUserCart(auth.uid,auth.uname,auth.upassword,pid).then(

                function(response){
                    getUserCart();
                },
                function(error){
                    getUserCart();
                }

            );
        }

        getUserCart();


    }]);