serviceURL = 'http://cgwsapi.herokuapp.com';

app.factory('storewsapi', ['$http',
    function($http) {
        var storeServiceURL = serviceURL + '/store';
        var storewsapi = {};
        storewsapi.getPlatforms =
            function()
            {
                return $http.get(storeServiceURL+'/platforms')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };
        storewsapi.getHomeAnnouncements =
            function (){
                return $http.get(storeServiceURL+'/announcements')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            }
        storewsapi.getLatestProducts =
            function()
            {
                return $http.get(storeServiceURL + '/latestproduct')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            }
        storewsapi.getInOfferProducts =
            function ()
            {
                return $http.get(storeServiceURL+'/specialproduct')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };
        storewsapi.getProduct =
            function (id)
            {
                return $http.get(storeServiceURL+'/'+id)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };
        storewsapi.getPlatformAnnouncements =
            function (id)
            {
                return $http.get(storeServiceURL+'/announcements/'+id)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };
        storewsapi.getPlatformInOffer =
            function (id)
            {
                return $http.get(storeServiceURL+'/special/'+id)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };
        storewsapi.getPlatformLatest =
            function (id)
            {
                return $http.get(storeServiceURL+'/latest/'+id)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };
        return storewsapi;
    }]);

app.factory('userwsapi', ['$http', function($http) {

    var userServiceURL = serviceURL + '/user'
    var userwsapi = {};

    userwsapi.getCustomer = function (id) {
        return $http.get(userServiceURL + '/' + id)
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.insertCustomer = function (cust) {
        return $http.post(userServiceURL, cust);
    };

    userwsapi.updateCustomer = function (cust) {
        return $http.put(userServiceURL + '/' + cust.ID, cust)
    };

    userwsapi.deleteCustomer = function (id) {
        return $http.delete(userServiceURL + '/' + id);
    };

    userwsapi.getOrders = function (id) {
        return $http.get(userServiceURL + '/' + id + '/orders');
    };

    return userwsapi;
}]);

app.factory("authenticationSvc", ["$http","$q","$window",function ($http, $q, $window) {
    var userInfo;

    function login(uname, upassword) {
        var deferred = $q.defer();

        $http.post(serviceURL +"/user/login", { uname: uname, upassword: upassword })
            .then(function (result) {
                userInfo = {
                    accessToken: result.data.access_token,
                    uname: result.data.uname
                };
                $window.sessionStorage["userInfo"] = JSON.stringify(userInfo);
                deferred.resolve(userInfo);
            }, function (error) {
                deferred.reject(error);
            });

        return deferred.promise;
    }

    function logout() {
        var deferred = $q.defer();

        try {
            userInfo = null;
            $window.sessionStorage["userInfo"] = null;
            deferred.resolve();
        }
        catch(err) {
            deferred.reject(err);
            console.log(JSON.toString(err))
        }

        return deferred.promise;
    }

    function getUserInfo() {
        return userInfo;
    }

    function init() {
        if ($window.sessionStorage["userInfo"]) {
            userInfo = JSON.parse($window.sessionStorage["userInfo"]);
        }
    }
    init();

    return {
        login: login,
        logout: logout,
        getUserInfo: getUserInfo
    };
}]);