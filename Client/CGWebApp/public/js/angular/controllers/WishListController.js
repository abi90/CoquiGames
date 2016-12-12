/**
 * Created by abi on 12/4/16.
 */
app.controller('WishListController',
    ['$rootScope','$scope', '$location', 'auth', 'authenticationSvc','userwsapi', 'addToUserCart',
        function ($rootScope, $scope, $location, auth, authenticationSvc, userwsapi, addToUserCart) {

            $scope.Loading = false;

            var getWishList = function(){
                $scope.Loading = true;
                userwsapi.getUserWishlist(auth.uid, auth.uname, auth.token)
                    .then(
                        function (response) {
                            $scope.userWishlist = response.data;
                        },
                        function () {
                            $location.path("/404.html");
                            $rootScope.$emit('unLogin');
                        }
                    );
                $scope.Loading = false;
            };

            $scope.addToCartFromWishList = function (pid) {
                $rootScope.$broadcast('uCart');
                addToUserCart.addProductWithQty(pid, 1);
                $rootScope.$broadcast('uCart');
            };

            $scope.deleteFromWishList = function (pid) {
                var userInfo = authenticationSvc.getUserInfo();
                if(userInfo){
                    userwsapi.delUserWishList(userInfo.uid, userInfo.uname, userInfo.upassword, pid)
                        .then(
                            function (){
                                getWishList();
                            },
                            function () {
                                $location.path("/404.html");
                                $scope.$emit('unLogin');
                            }
                        );
                }
                else{
                    $location.path('/login.html');
                }
            };

            getWishList();


        }]);