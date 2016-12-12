/**
 * Created by felix on 12/10/16.
 */

app.controller('AdminGenreController',
    ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye', 'authenticationSvc',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye, authenticationSvc){

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
                function () {
                    $scope.genres = [];
                    authenticationSvc.logout();
                    $rootScope.$broadcast('unLogin');
                    $location.path('/login.html');
                }
            );


        };


        //Deactivate a genre
        $scope.shoDeactivateGenre = function(genreid){
            adminwsapi.deactivateGenre(auth.uname, auth.token, genreid).then(
                function () {
                    getGenres();
                },
                function () {
                    getGenres();
                }
            );

        };

        //Activate a Genre
        $scope.shoActivateGenre = function(genreid){
            adminwsapi.activateGenre(auth.uname, auth.token, genreid).then(
                function () {
                    getGenres();
                },
                function () {
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
            modal.closed.then(function(genre) {
                if(genre){
                    adminwsapi.postGenre(auth.uname, auth.token, genre).then(
                        function () {
                            getGenres();
                        },
                        function () {
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
