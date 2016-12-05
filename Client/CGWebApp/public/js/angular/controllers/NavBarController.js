app.controller('NavBarController',
    ['$scope', '$rootScope', '$location', 'storewsapi', 'authenticationSvc', 'userwsapi',
        function($scope, $rootScope ,$location, storewsapi, authenticationSvc, userwsapi) {

            $scope.navbarOptions;
            $rootScope.platforms;
            $rootScope.Loggedin = false;
            $scope.user;
            $scope.CartSize;
            $scope.title = '';


            storewsapi.getPlatforms().then(
                function (response) {
                    $scope.navbarOptions = response.data;
                    $rootScope.platforms = response.data;
                },
                function (error) {
                    console.log(error);
                    $location.path("/404.html");
                }
            );

            $scope.redirect = function(){
                $location.url("search/"+$scope.title);
            };

            var getUser = function(){
                $scope.user = authenticationSvc.getUserInfo();
                if ($scope.user)
                {
                    $scope.Loggedin=true;
                }

            };

            $rootScope.$on('Login',function(){$scope.Loggedin=true; getCartLength(); getUser();});

            $rootScope.$on('unLogin',function(){$scope.Loggedin=false});

            $rootScope.$on('uCart',function () {getCartLength();});

            $scope.logoutUser = function () {
                authenticationSvc.logout();
                $scope.Loggedin=false;
            };

            var getCartLength =  function () {
                var auth = authenticationSvc.getUserInfo();
                userwsapi.getUserCart(auth.uid, auth.uname, auth.token).then(
                    function (response) {
                        $scope.CartSize = response.data.length;
                    },
                    function () {
                        $scope.CartSize =0;
                    }
                );

            };

            $scope.goToCart = function () {
                getCartLength();
                $location.path("/cart.html");
            };

            $scope.adSearch = function(platformid, genre, category) {

                var data = {'platformid': platformid,
                    'genre': genre,
                    'category' : category};
                console.log(JSON.stringify(data));

                storewsapi.adSearch(data).then(
                    function (){
                        $location.path("/advanced_search/"+platformid+"/"+genre+"/"+category+"/");
                    },
                    function(){

                    }
                );

            };


            getUser();
        }]);