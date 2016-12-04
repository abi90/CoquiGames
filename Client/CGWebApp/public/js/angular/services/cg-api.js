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
        storewsapi.getGenres =
            function () {
                return $http.get(storeServiceURL+'/genres')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.searchByTitle =
            function (title)
            {
                return $http.post(storeServiceURL+'/search', {title: title})
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.adSearch =
            function (data)
            {
                return $http.post(storeServiceURL+'/advanced_search', data)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.search =
            function (data)
            {
                return $http.post(storeServiceURL+'/search', data)
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };


        storewsapi.relatedProducts =
            function (pid) {
                return $http.get(storeServiceURL+'/product/'+pid+'/related')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };


        storewsapi.topPlatProducts =
            function (pid) {
                return $http.get(storeServiceURL+'/platform/'+pid+'/top')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };


        storewsapi.topProducts =
            function () {
                return $http.get(storeServiceURL+'/top')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.getProductAltImg =
            function (id)
            {
                return $http.get(storeServiceURL+'/product/'+id+'/altimgs')
                    .success(function (data) {return data;})
                    .error(function (error) {return error;});
            };

        storewsapi.putProductRating=
            function (id, rating)
            {
                return $http.put(storeServiceURL+'/product/'+id+'/rating', rating)
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


    userwsapi.getUserPreferences= function (uid, username, password) {
        return $http.get(userServiceURL + '/' + uid + '/preferences', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };


    userwsapi.getUserBillingAddress= function (uid, username, password) {
        return $http.get(userServiceURL + '/' + uid + '/billing_address', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };


    userwsapi.getUserShippingAddress= function (uid, username, password) {
        return $http.get(userServiceURL + '/' + uid + '/shipping_address', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };


    userwsapi.getShipmentFees= function () {
        return $http.get(userServiceURL + '/shipmentfees')
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.putUserAddress= function (uid, username, password, address) {
        return $http({
            method: 'PUT',
            url: userServiceURL + '/' + uid + '/address/' + address.aid,
            dataType: 'json',
            data: address,
            headers: {'Content-Type': 'application/json',
                'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.postUserCart= function (uid, username, password, product) {
        return $http({
            method: 'POST',
            url: userServiceURL + '/' + uid + '/cart/' + product.pid,
            dataType: 'json',
            data: product,
            headers: {'Content-Type': 'application/json',
                'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.putUserCart= function (uid, username, password, product) {
        return $http({
            method: 'PUT',
            url: userServiceURL + '/' + uid + '/cart/' + product.pid,
            dataType: 'json',
            data: product,
            headers: {'Content-Type': 'application/json',
                'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.postUserOrder = function(uid,username,password,order){
        return $http({
            method:'POST',
            url: userServiceURL + '/' +uid+'/order',
            dataType: 'json',
            data: order,
            headers: {'Content-Type': 'application/json',
                'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.delUserCart= function (uid, username, password, pid) {
        return $http({
            method: 'DELETE',
            url: userServiceURL + '/' + uid + '/cart/' + pid,
            headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.postUserWishList= function (uid, username, password, pid) {
        return $http({
            method: 'POST',
            url: userServiceURL + '/' + uid + '/wishlist/' + pid,
            dataType: 'json',
            data: product,
            headers: {'Content-Type': 'application/json',
                'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    userwsapi.delUserWishList= function (uid, username, password, pid) {
        return $http({
            method: 'DELETE',
            url: userServiceURL + '/' + uid + '/wishlist/' + pid,
            headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
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
                    upassword: result.data.token,
                    token: result.data.token,
                    roleid: result.data.roleid
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

app.factory('adminwsapi', ['$http','$base64', function($http, $base64) {

    var adminServiceURL = serviceURL + '/admin';

    var adminwsapi = {};

    adminwsapi.getUsers= function (username, password) {
        return $http.get(adminServiceURL + '/users', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };
    adminwsapi.getAllProducts= function (username, password) {
        return $http.get(adminServiceURL + '/products', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    adminwsapi.getOrders= function (username, password) {
        return $http.get(adminServiceURL + '/orders', { headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password) } })
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    adminwsapi.postAdminUser= function (username, password, newUser) {
        return $http({
            method: 'POST',
            url: adminServiceURL + '/',
            dataType: 'json',
            data: newUser,
            headers: {'Content-Type': 'application/json',
                'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    adminwsapi.deactivateUser= function (username, password, uid) {
        return $http({
            method: 'PUT',
            url: adminServiceURL + '/account/' + uid + '/deactivate',
            headers: {'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };

    adminwsapi.changeUserPassword= function (username, password, uid, upassword) {
        return $http({
            method: 'PUT',
            url: adminServiceURL + '/account/' + uid + '/password',
            dataType: 'json',
            data: {"upasword": upassword},
            headers: {'Content-Type': 'application/json',
                'Authorization': 'Basic '+ $base64.encode( username + ':' + password)}})
            .success(function (data) {return data;})
            .error(function (error) {return error;});
    };



    return adminwsapi;
}]);