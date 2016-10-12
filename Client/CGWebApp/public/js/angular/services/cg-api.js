serviceURL = 'http://cgwsapi.herokuapp.com';
storeServiceURL = serviceURL +'/store';

app.factory('cgapi', ['$http',
    function($http) {
    return {
        getLatestProducts: $http.get(storeServiceURL+'/latestproduct')
            .success(function (data) {
                return data;
            })
            .error(function () {
                return {error: '404'};
            }),
        getInOfferProducts: $http.get(storeServiceURL+'/specialproduct')
            .success(function (data) {
                return data;
            })
            .error(function () {
                return {error: '404'};
            })
    };
}]);