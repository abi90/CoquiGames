app.controller('HomeController',
    ['$scope', 'storewsapi', 'authenticationSvc','userwsapi','$location', '$rootScope',
    function($scope, storewsapi, authenticationSvc,userwsapi, $location, $rootScope) {

        $scope.latest;
        $scope.specials;
        $scope.top;
        $scope.slides = [];
        $scope.myInterval = 5000;
        $scope.nowWrapSlides = true;
        $scope.active = 0;

        storewsapi.getLatestProducts().then(
            function(response) {
                $scope.latest = response.data;
            },
            function (error) {
                console.log(error.toString());
                $scope.latest = [];
            });

        storewsapi.getHomeAnnouncements().then(
            function(response){
                $scope.slides = response.data;
                $scope.active = 0;
            },
            function(error){
                console.log(error.toString());
                $scope.slides = [];
            }


        );

        storewsapi.getInOfferProducts().then(
            function(response) {
                $scope.specials = response.data;
            },
            function (error) {
                console.log(error.toString());
                $scope.specials = [];
            });

        storewsapi.topProducts().then(
            function(response) {
                $scope.top = response.data;
            },
            function (error) {
                console.log(error.toString());
                $scope.top = [];
            });

        $scope.addToCart = function (pid) {
            var userInfo = authenticationSvc.getUserInfo();
            if(userInfo){
                userwsapi.getUserCart(userInfo.uid,userInfo.uname, userInfo.upassword).then(
                    function (response) {
                        var i;
                        var cart = response.data;
                        var product;
                        for (i = 0; i < cart.length; i++) {
                            console.log(cart[i].pid);
                            if(cart[i].pid == pid)
                            {
                                product = cart[i];
                                product.pquantity = product.pquantity + 1;
                                userwsapi.putUserCart(userInfo.uid,userInfo.uname, userInfo.upassword, product)
                                    .then(function (response) {console.log(JSON.stringify(response));},function (err){});
                                break;
                            }
                        }
                        if(!product){
                            userwsapi.postUserCart(userInfo.uid,userInfo.uname, userInfo.upassword,{"pid":pid,"pquantity":1})
                                .then(function (response) {},function (err){});
                        }
                        $rootScope.$emit('uCart');
                    },
                    function () {
                        $location.path('/404.html');
                    }
                );
            }
            else{
                $location.path('/login.html');
            }
        };

    }]);