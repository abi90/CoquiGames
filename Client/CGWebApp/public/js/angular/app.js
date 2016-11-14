var app = angular.module('MainApp', ['ngRoute','ui.bootstrap.demo','ngAnimate', 'ngSanitize','$base64', 'pathgather.popeye', 'ui.bootstrap',]);

app.config(['$httpProvider', '$routeProvider', function ($httpProvider, $routeProvider) {

    // Configuration to access Flask
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = false;
    delete $httpProvider.defaults.headers.common["X-Requested-With"];
    $httpProvider.defaults.headers.common["Accept"] = "application/json";
    $httpProvider.defaults.headers.common["Content-Type"] = "application/json";

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
                    return params.platformId =  params.platformId;
                }]
            }
        })
        .when('/search/:title', {
            controller: 'SearchController',
            templateUrl: 'views/search-list.html',
            resolve: {
                title: ['$route', function($route){
                    var params = $route.current.params;
                    return params.title =  params.title;
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
            controller: 'AccountController',
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
                    return params.productId = params.productId;
                }]
            }

        })
        .when('/register.html', {
            controller: 'HomeController',
            templateUrl: 'views/register.html'
        })
        .when('/wishlist', {
            controller: 'AccountController',
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
            controller: 'AccountController',
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
            controller: 'AccountController',
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
                orderId: ['$route', function($route) {
                    var params = $route.current.params;
                    return params.orderId = params.orderId;
                }]
            }

        })
        .when('/account-payment', {
            controller: 'AccountController',
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
            controller: 'AccountController',
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
            controller: 'AccountController',
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
        .otherwise({
            redirectTo: '/'
        });

}]);

app.run(["$rootScope", "$location", function ($rootScope, $location) {

    $rootScope.$on("$routeChangeSuccess", function (userInfo) {
        console.log(JSON.toString(userInfo));
    });

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
})
