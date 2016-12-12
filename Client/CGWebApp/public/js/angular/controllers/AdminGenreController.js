/**
 * Created by felix on 12/10/16.
 */

app.controller('AdminGenreController', ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye){

        // Defaults sort type, order adn default search filter
        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchProduct = '';
        $scope.messages = [];
        $scope.errors = [];

        var getGenres = function(){
            adminwsapi.getAllGenres(auth.name,auth.token).then(
            function (response) {
                $scope.genres = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.genres = [];
            }
            );


        };


        //Deactivate a genre
        $scope.shoDeactivateGenre = function(genreid){
            adminwsapi.deactivateGenre(auth.uname, auth.token, genreid).then(
                function (response) {
                    getGenres();
                },
                function (err) {
                    getGenres();
                }
            );

        };

        //Activate a Genre
        $scope.shoActivateGenre = function(genreid){
            adminwsapi.activateGenre(auth.uname, auth.token, genreid).then(
                function (response) {
                    getGenres();
                },
                function (err) {
                    getGenres();
                }
            );

        };


        //Add Platform Announcement
        $scope.shoAddGenre = function() {
            // Open a modal for admin to edit an order
            var modal = Popeye.openModal({
                controller: 'AdminAddGenreController',
                templateUrl: "js/angular/modals/add-admin-genre.html"
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(announcement) {
                if(announcement){
                    adminwsapi.postAnnouncement(auth.uname, auth.token, announcement).then(
                        function (response) {
                            getGenres();
                        },
                        function (err) {
                            getGenres();
                        }
                    );
                }

            });
        };







        $scope.closeErrorAlert= function(index){
            $scope.errors.splice(index,1);
        };

        $scope.closeMessageAlert= function(index){
            $scope.messages.splice(index,1);
        };







    getGenres();











    }]);
