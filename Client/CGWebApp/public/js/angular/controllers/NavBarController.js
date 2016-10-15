app.controller('NavBarController', ['$scope', '$rootScope', '$location', 'storewsapi', 'authenticationSvc', 'userwsapi',
    function($scope, $rootScope ,$location, storewsapi, authenticationSvc,userwsapi) {
        /*$scope.navbarOptions = [
         {
         platformId: "PS4",
         imglogo: 'images/product-images/ps4-logo.jpg',
         consoles: [{id: 0, name:"Deals"}, {id:1, name: "PS4 Pro"},{id: 2, name: "PS4 Slim"}],
         accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
         topgames:["Deals","Action", "Fighting", "VR Games", "Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
         },
         {
         platformId: "XBOX ONE",
         imglogo: 'images/product-images/xbox-one-logo.jpg',
         consoles: [{id: 0, name:"Deals"}, {id:1, name: "Xbox One S"},{id:2, name:"Xbox One"}],
         accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
         topgames:["Deals","Action", "Fighting", "Kinect Games", "Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
         },
         {
         platformId: "3DS",
         imglogo: 'images/product-images/3ds-logo.jpg',
         consoles: [{id: 0, name:"Deals"}, {id:1, name: "Nintendo 3DS XL"},{id:2, name: "Nintendo 3DS"},{id:3, name: "Nitendo 2DS"}],
         accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
         topgames:["Deals","Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
         },
         {
         platformId: "Wii U",
         imglogo: 'images/product-images/wii-u-logo.jpg',
         consoles: [{id: 0, name:"Deals"}, {id: 1, name: "Wii U"}],
         accesories: ["Deals","Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
         topgames:["Deals","Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
         }
         ];*/

        $scope.navbarOptions;
        $rootScope.Loggedin = false;
        $scope.user;
        $scope.CartSize;


        storewsapi.getPlatforms().then(
            function (response) {
                $scope.navbarOptions = response.data;
            },
            function (error) {
                console.log(error);
                $location.path("/404.html");
            }
        );

        $scope.redirect = function(){
            $location.url("search-grid");
        };

        var getUser = function(){
            $scope.user = authenticationSvc.getUserInfo();
            if ($scope.user)
            {
                $scope.Loggedin=true;
            }

        };

        $rootScope.$on('Login',function(){$scope.Loggedin=true; getCartLength();});

        $rootScope.$on('unLogin',function(){$scope.Loggedin=false});

        $scope.logoutUser = function () {
            authenticationSvc.logout();
            $scope.Loggedin=false;
        };

        var getCartLength =  function () {
            var auth = authenticationSvc.getUserInfo();
            userwsapi.getUserCart(auth.uid, auth.uname, auth.upassword).then(
                function (response) {
                    $scope.CartSize = response.data.length;
                },
                function (error) {
                    console.log("Error: " +error.statusCode);
                    $scope.CartSize =0;
                }
            )

            };

            $scope.goToCart = function () {
                $location.path("/cart.html");
            };




        getUser();
    }]);