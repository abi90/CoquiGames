app.controller('HomeController', ['$scope', 'storewsapi',
    function($scope, storewsapi) {

        $scope.latest;
        $scope.specials;
        $scope.top;

        storewsapi.getLatestProducts().then(
            function(response) {
                $scope.latest = response.data;
            },
            function (error) {
                console.log(error.toString());
                $scope.latest = [];
            });

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

    }]);