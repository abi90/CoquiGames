/**
 * Created by jesmarie on 12-08-16.
 */
/**
 * Created by jesmarie on 12-08-16.
 */
app.controller('AdminEditAnnouncementsController', ['$scope', 'authenticationSvc','$rootScope', 'Popeye', 'adminwsapi', 'announcement',
    function ($scope, authenticationSvc, $rootScope, Popeye, adminwsapi, announcement) {

        $scope.auth = authenticationSvc.getUserInfo();

        var tempEditAnnouncement = {
            "a_title": announcement.a_title,
            "a_img": announcement.a_img,
            "active": announcement.active,
            "platformid": announcement.platformid,
            "aid": announcement.aid
        };

        $scope.selectedEditAnnouncement = tempEditAnnouncement;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.submit = function() {
            $scope.selectedEditAnnouncement = tempEditAnnouncement;
            return Popeye.closeCurrentModal($scope.selectedEditAnnouncement);
        };

        $scope.cancel = function () {
            $scope.selectedEditAnnouncement = tempEditAnnouncement;
            return Popeye.closeCurrentModal(null);
        };

    }]);