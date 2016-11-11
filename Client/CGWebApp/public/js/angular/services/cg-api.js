serviceURL = 'https://cgwsapi.herokuapp.com';

app.factory('storewsapi', ['$http',
    function($http) {
        var storeServiceURL = serviceURL + '/store';
        var storewsapi = {};
        storewsapi.getPlatforms =
            function()
            {
                return $http.get(storeServiceURL + '/platforms')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getHomeAnnouncements =
            function (){
                return $http.get(storeServiceURL+'/announcements')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getLatestProducts =
            function()
            {
                return $http.get(storeServiceURL + '/latestproduct')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getInOfferProducts =
            function ()
            {
                return $http.get(storeServiceURL + '/specialproduct')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getProduct =
            function (id)
            {
                return $http.get(storeServiceURL+'/product/'+id)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getPlatformAnnouncements =
            function (id)
            {
                return $http.get(storeServiceURL+'/platform/'+id+'/announcements')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getPlatformInOffer =
            function (id)
            {
                return $http.get(storeServiceURL+'/platform/'+id+'/special')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getPlatformLatest =
            function (id)
            {
                return $http.get(storeServiceURL+'/platform/'+id+'/latest')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getPlatform =
            function (id)
            {
                return $http.get(storeServiceURL+'/platform/'+id)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        return storewsapi;
    }]);

app.factory('userwsapi', ['$http','$base64', function($http, $base64) {

    var userServiceURL = serviceURL + '/user';

    var userwsapi = {};

    userwsapi.getUser = function (id, username, password) {
        return $http.get(userServiceURL + '/' + id, { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.getUserCart = function (id, username, password) {
        return $http.get(userServiceURL + '/' + id +'/cart', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.getUserWishlist = function (id, username, password) {
        return $http.get(userServiceURL + '/' + id +'/wishlist', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };


    userwsapi.getUserAddress = function (id, username, password) {
        return $http.get(userServiceURL + '/' + id +'/address', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.getUserOrders = function (id, username, password) {
        return $http.get(userServiceURL + '/' + id +'/order', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };


    userwsapi.getUserPayment = function (id, username, password) {
        return $http.get(userServiceURL + '/' + id +'/payment', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };


    userwsapi.getUserAddressById = function (uid, aid, username, password) {
        return $http.get(userServiceURL + '/' + uid + '/address/' + aid, { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    return userwsapi;
}]);

app.factory("authenticationSvc", ["$http","$q","$window", '$rootScope',function ($http, $q, $window, $rootScope) {
    var userInfo;

    function login(uname, upassword) {
        var deferred = $q.defer();

        $http.post(serviceURL +"/user/login", { uname: uname, upassword: upassword })
            .then(function (result) {
               userInfo = {
                    uid: result.data.uid,
                    uname: uname,
                    upassword: upassword
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