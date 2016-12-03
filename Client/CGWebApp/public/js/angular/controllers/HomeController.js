app.controller('HomeController', ['$scope', 'storewsapi',
    function($scope, storewsapi) {

        $scope.latest;
        $scope.specials;
        $scope.top;
        $scope.slides = [];
        $scope.myInterval = 5000;
        $scope.nowWrapSlides = true;
        $scope.active ;


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

    }]);