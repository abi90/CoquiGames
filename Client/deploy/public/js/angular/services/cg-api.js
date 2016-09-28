app.factory('cgapi', ['$http', function($http) {
    return $http.get('http://www.w3schools.com/angular/customers.php')
        .success(function(data) {
            return data;
        })
        .error(function() {
            return {error: '404'};
        });
}]);