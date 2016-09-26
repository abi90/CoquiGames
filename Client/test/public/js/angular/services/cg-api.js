app.factory('cgapi', ['$http', function($http) {
    return $http.get('http://0.0.0.0:5000/')
        .success(function(data) {
            return data;
        })
        .error(function(data) {
            return data;
        });
}]);