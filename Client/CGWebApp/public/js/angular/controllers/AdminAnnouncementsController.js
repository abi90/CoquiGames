/**
 * Created by Abisai on 11/29/16.
 */
app.controller('AdminAnnouncementsController', ['$scope', '$location', 'adminwsapi', 'auth', '$rootScope', 'Popeye', 'authenticationSvc',
    function ($scope, $location, adminwsapi, auth, $rootScope, Popeye, authenticationSvc) {

        $scope.sortType = 'active';
        $scope.sortReverse = false;
        $scope.searchAnnouncements = '';
        $scope.Loading = false;


        // Get list of announcements from the WS API
        var getAllAnnouncements = function() {
            $scope.Loading = true;
            adminwsapi.getAnnouncements(auth.uname, auth.token).then(
                function (response) {
                    $scope.announcements = response.data
                },
                function () {
                    $scope.announcements = [];
                    authenticationSvc.logout();
                    $rootScope.$broadcast('unLogin');
                    $location.path('/login.html');

                }
            );
            $scope.Loading = false;
        };

        getAllAnnouncements();

        //Add Home Announcement
        $scope.shoAddHomeAnnouncement = function() {
            // Open a modal for admin to edit an order
            var modal = Popeye.openModal({
                controller: 'AdminAddHomeAnnouncementsController',
                templateUrl: "js/angular/modals/add-admin-home-announcement.html"
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
                        function () {
                            getAllAnnouncements()
                        },
                        function () {
                            getAllAnnouncements()
                        }
                    );
                }

            });
        };

        //Add Platform Announcement
        $scope.shoAddPlatformAnnouncement = function() {
            // Open a modal for admin to edit an order
            var modal = Popeye.openModal({
                controller: 'AdminAddPlatformAnnouncementsController',
                templateUrl: "js/angular/modals/add-admin-platform-announcement.html"
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
                        function () {
                            getAllAnnouncements()
                        },
                        function () {
                            getAllAnnouncements()
                        }
                    );
                }

            });
        };

        //Edit Home Announcement
        $scope.shoEditHomeAnnouncement = function(announcement) {
            // Open a modal for admin to edit an order
            var modal = Popeye.openModal({
                controller: 'AdminEditAnnouncementsController',
                templateUrl: "js/angular/modals/edit-admin-home-announcement.html",
                resolve: {
                    announcement: function () {
                        return announcement;
                    }
                }
            });

            // Show a spinner while modal is resolving dependencies
            $scope.showLoading = true;
            modal.resolved.then(function() {
                $scope.showLoading = false;
            });

            // Update user selected address after modal is closed
            modal.closed.then(function(announcement) {
                if(announcement){
                    adminwsapi.updateAnnouncement(auth.uname, auth.token, announcement).then(
                        function () {
                            getAllAnnouncements()
                        },
                        function () {
                            getAllAnnouncements()
                        }
                    );
                }

            });
        };

        $scope.shoDeactivateAnnouncement = function(announcement){
            adminwsapi.deactivateAnnouncement(auth.uname, auth.token, announcement).then(
                function () {
                    getAllAnnouncements()
                },
                function () {
                    getAllAnnouncements()
                }
            );
        };

    }]);