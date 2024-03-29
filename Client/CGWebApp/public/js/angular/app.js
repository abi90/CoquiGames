var app = angular.module('MainApp', ['ngRoute','ui.bootstrap.demo','ngAnimate', 'ngSanitize','$base64', 'ngFileUpload',
    'pathgather.popeye', 'ui.bootstrap', 'fancyboxplus', 'cloudinary']);

app.config(['$httpProvider', '$routeProvider', 'cloudinaryProvider', function ($httpProvider, $routeProvider, cloudinaryProvider) {

    // Configuration to access Flask
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = false;
    delete $httpProvider.defaults.headers.common["X-Requested-With"];
    $httpProvider.defaults.headers.common["Accept"] = "application/json";
    $httpProvider.defaults.headers.common["Content-Type"] = "application/json";

    cloudinaryProvider
        .set("cloud_name", "coquigames-herokuapp-com")
        .set("upload_preset", "o6kned8u");

    $routeProvider
        .when('/', {
            controller: 'HomeController',
            templateUrl: 'views/home.html'
        })
        .when('/platform-home/:platformId', {
            controller: 'PlatformController',
            templateUrl: 'views/platform-home.html',
            resolve: {
                platformId: ['$route', function($route){
                    var params = $route.current.params;
                    return params.platformId;
                }]
            }
        })
        .when('/search/:title', {
            controller: 'SearchController',
            templateUrl: 'views/search-list.html',
            resolve: {
                title: ['$route', function($route){
                    var params = $route.current.params;
                    return params.title;
                }]
            }
        })

        .when('/advanced_search/:platformid/:genre/:category', {
            controller: 'AdvancedSearchController',
            templateUrl: 'views/advanced-search.html',
            resolve: {
                search_data: ['$route', function($route){
                    var params = $route.current.params;
                    return params.search_data =  {"platformid": params.platformid, "genre": params.genre, "category": params.category};
                }]
            }
        })

        .when('/404.html', {
            controller: '',
            templateUrl: 'views/404.html'
        })
        .when('/index.html', {
            controller: 'HomeController',
            templateUrl: 'views/home.html'
        })
        .when('/about.html', {
            controller: 'HomeController',
            templateUrl: 'views/about.html'
        })
        .when('/cart.html', {
            controller: 'CartController',
            templateUrl: 'views/cart.html',
            resolve: {
                auth: function ($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }
        })
        .when('/contact.html', {
            controller: 'HomeController',
            templateUrl: 'views/contact.html'
        })
        .when('/login.html', {
            controller: 'LoginController',
            templateUrl: 'views/login.html'
        })
        .when('/product.html/:productId', {
            controller: 'ProductController',
            templateUrl: 'views/product.html',
            resolve: {
                productId: ['$route', function($route) {
                    var params = $route.current.params;
                    return params.productId;
                }]
            }

        })
        .when('/register.html', {
            controller: 'RegisterController',
            templateUrl: 'views/register.html',
            resolve:{
                auth: function ($q, $location,authenticationSvc)
                {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        $location.path('/account-info');
                    }
                }
            }
        })
        .when('/wishlist', {
            controller: 'WishListController',
            templateUrl: 'views/wishlist.html',
            resolve: {
                auth:
                    function ($q, authenticationSvc)
                    {
                        var userInfo = authenticationSvc.getUserInfo();
                        if (userInfo) {
                            return $q.when(userInfo);
                        } else {
                            return $q.reject({ authenticated: false });
                        }
                    }
            }
        })
        .when('/account-info', {
            controller: 'UserInfoController',
            templateUrl: 'views/account-info.html',
            resolve: {
                auth: function ($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }
        })
        .when('/account-orders', {
            controller: 'UserOrdersController',
            templateUrl: 'views/account-orders.html',
            resolve: {
                auth: function ($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }
        })
        .when('/account-orderdetails.html/:orderId', {
            controller: 'OrderController',
            templateUrl: 'views/account-orderdetails.html',
            resolve: {
                orderId: ['$route', '$q', 'authenticationSvc', function($route, $q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        var params = $route.current.params;
                        return $q.when(params.orderId);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }]
            }

        })
        .when('/account-payment', {
            controller: 'UserPaymentController',
            templateUrl: 'views/account-payment.html',
            resolve: {
                auth: function ($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }
        })
        .when('/checkout', {
            controller: 'UserCheckoutController',
            templateUrl: 'views/checkout.html',
            resolve: {
                auth: function ($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }
        })
        .when('/account-address', {
            controller: 'UserAddressController',
            templateUrl: 'views/account-address.html',
            resolve: {
                auth: function ($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo) {
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }
        })
        .when('/admin-users', {
            controller: 'AdminUsersController',
            templateUrl: 'views/admin-users.html',
            resolve: {
                auth:  function($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo.roleid === 3){
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }

        })
        .otherwise({
            redirectTo: '/'
        })
    .when('/admin-orders', {
        controller: 'AdminOrdersController',
        templateUrl: 'views/admin-orders.html',
        resolve: {
            auth:  function($q, authenticationSvc) {
                var userInfo = authenticationSvc.getUserInfo();
                if (userInfo.roleid === 3){
                    return $q.when(userInfo);
                } else {
                    return $q.reject({ authenticated: false });
                }
            }
        }

    })
        .when('/admin-products', {
            controller: 'AdminProductsController',
            templateUrl: 'views/admin-products.html',
            resolve: {
                auth:  function($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo.roleid === 3){
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }

        })

        .when('/admin-genres', {
            controller: 'AdminGenreController',
            templateUrl: 'views/admin-genres.html',
            resolve: {
                auth:  function($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo.roleid === 3){
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }
        })

        .when('/admin-announcements', {
            controller: 'AdminAnnouncementsController',
            templateUrl: 'views/admin-announcements.html',
            resolve: {
                auth:  function($q, authenticationSvc) {
                    var userInfo = authenticationSvc.getUserInfo();
                    if (userInfo.roleid === 3){
                        return $q.when(userInfo);
                    } else {
                        return $q.reject({ authenticated: false });
                    }
                }
            }

        })
        .otherwise({
            redirectTo: '/'
        });

}]);


app.run(["$rootScope", "$location", function ($rootScope, $location) {
    $rootScope.$on("$routeChangeError", function (event, current, previous, eventObj) {
        if (eventObj.authenticated === false) {
            $location.path("/login.html");
        }
    });
}]);

app.filter('html',function($sce){
    return function(input){
        return $sce.trustAsHtml(input);
    }
});
