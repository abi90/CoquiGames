/**
 * Created by felix on 12/11/16.
 */

app.controller('AdminAddGenreController', ['$scope', 'authenticationSvc','$rootScope', 'Popeye',
    function ($scope, authenticationSvc, $rootScope, Popeye) {

        $scope.auth = authenticationSvc.getUserInfo();

        var tempGenre = {
            "genre": '',
            "active": false
        };

        $scope.selectedGenre = tempGenre;
        $scope.userInfo = authenticationSvc.getUserInfo();

        $scope.submit = function() {
            return Popeye.closeCurrentModal($scope.selectedGenre);
        };

        $scope.cancel = function () {
            return Popeye.closeCurrentModal(null);
        };

    }]);