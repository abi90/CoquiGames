/**
 * Created by abi on 10/14/16.
 */
/**
 * Created by abi on 10/12/16.
 */
app.controller('CartController',
    ['$scope', '$location', 'auth', 'authenticationSvc', 'userwsapi', '$rootScope',
    function ($scope, $location,auth,authenticationSvc, userwsapi, $rootScope) {

        $rootScope.userCart = [];
        $scope.cartTotal = 0;

        var getUserCart= function () {
            var auth = authenticationSvc.getUserInfo();
            if (auth){
                userwsapi.getUserCart(auth.uid, auth.uname, auth.upassword).then(
                    function (response) {
                        $scope.userCart = response.data;
                    },
                    function () {
                        $rootScope.$emit('unLogin');
                        authenticationSvc.logout();
                    }
                )
            }
        };

        $scope.getSubTotal = function(){
            if( $scope.userCart){
                var subtotal = 0;
                for(var i = 0; i < $scope.userCart.length; i++){
                    var product = $scope.userCart[i];
                    if (product.inoffer) {
                        subtotal += (product.offerprice * product.pquantity);
                    }
                    else{
                        subtotal += (product.pprice * product.pquantity);
                    }
                }
                $scope.cartTotal = subtotal + $scope.shippmentFee;
                return subtotal;
            }

        };

        $scope.changeProductQty = function(product){
            if(product.pquantity>0 || product.pquantity < 99){
                var auth = authenticationSvc.getUserInfo();
                userwsapi.putUserCart(auth.uid,auth.uname,auth.upassword,product).then(
                    function(){
                        $rootScope.$emit('uCart');
                        getUserCart();
                    },
                    function(){
                        $rootScope.$emit('uCart');
                        getUserCart()
                    });
            }
        };

        $scope.removeProduct = function(pid) {
            var auth = authenticationSvc.getUserInfo();
            userwsapi.delUserCart(auth.uid,auth.uname,auth.upassword,pid).then(
                function(){
                    getUserCart();
                    $rootScope.$emit('uCart');
                },
                function(){
                    $rootScope.$emit('uCart');
                    getUserCart();
                }
            );
        };

        getUserCart();

    }]);