app.controller('HomeController', ['$scope', 'storewsapi', 'authenticationSvc',
    function($scope, storewsapi, authenticationSvc) {

        $scope.latest;
        $scope.specials;
        $scope.user;

        storewsapi.getLatestProducts().then(function(responce) {
            $scope.latest = responce.data;
        });

        storewsapi.getInOfferProducts().then(function(responce) {
            $scope.specials = responce.data;
        });

        var getUser = function(){

            if (authenticationSvc.getUserInfo())
            {
                $scope.user = authenticationSvc.getUserInfo();
            }

        };

        getUser();

    }]);