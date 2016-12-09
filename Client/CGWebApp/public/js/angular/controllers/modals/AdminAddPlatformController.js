/**
 * Created by jesmarie on 12-08-16.
 */
/**
 * Created by jesmarie on 12-08-16.
 */
app.controller('AdminAddPlatformAnnouncementsController', ['$scope', 'authenticationSvc','$rootScope', 'Popeye', 'adminwsapi',
    function ($scope, authenticationSvc, $rootScope, Popeye, adminwsapi) {

        $scope.auth = authenticationSvc.getUserInfo();

        adminwsapi.getPlatforms($scope.auth.uname, $scope.auth.token).then(
            function (response) {
                $scope.platforms = response.data
            },
            function (err) {
                console.log(err.toString());
                $scope.platforms = [];
            }
        );

        var tempAnnouncement = {
            "a_title": null,
            "a_img": null,
            "active": false,
            "platformid": ''
        };

        $scope.selectedAnnouncement = tempAnnouncement;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.submit = function() {
            $scope.selectedAnnouncement = tempAnnouncement;
            return Popeye.closeCurrentModal($scope.selectedAnnouncement);
        };

        $scope.cancel = function () {
            $scope.selectedAnnouncement = tempAnnouncement;
            return Popeye.closeCurrentModal(null);
        };

    }]);