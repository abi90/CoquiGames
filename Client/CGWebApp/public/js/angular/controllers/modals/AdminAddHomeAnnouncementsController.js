/**
 * Created by jesmarie on 12-08-16.
 */
app.controller('AdminAddHomeAnnouncementsController', ['$scope', 'authenticationSvc','$rootScope', 'Popeye', 'adminwsapi',
    function ($scope, authenticationSvc, $rootScope, Popeye, adminwsapi) {

        $scope.auth = authenticationSvc.getUserInfo();

        var tempAnnouncement = {
            "a_title": null,
            "a_img": null,
            "active": false,
            "platformid": 0
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