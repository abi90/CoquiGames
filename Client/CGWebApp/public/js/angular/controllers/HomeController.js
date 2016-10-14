app.controller('HomeController', ['$scope', 'storewsapi',
    function($scope, storewsapi) {

        $scope.latest;
        $scope.specials;

        storewsapi.getLatestProducts().then(function(responce) {
            $scope.latest = responce.data;
        });

        storewsapi.getInOfferProducts().then(function(responce) {
            $scope.specials = responce.data;
        });



    }]);